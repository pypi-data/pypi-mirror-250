import copy
import os
from typing import Any, Dict, List, Mapping, Optional

from promptflow._internal import BuiltinsManager, ConnectionManager, builtins
from promptflow.contracts.flow import Flow, InputAssignment, InputValueType, Node
from promptflow.contracts.tool import ConnectionType, Tool, ToolType, ValueType
from promptflow.exceptions import ErrorTarget
from promptflow.executor.flow_validator import FlowValidator
from promptflow.runtime._errors import ConnectionNotSet
from promptflow.runtime.serving._errors import (
    ConnectionNotFound,
    InvalidConnectionType,
    NodeInputValidationError,
    NodeOfVariantNotFound,
    ToolNotFound,
    ToolNotFoundInFlow,
    ToolOfVariantNotFound,
    UnexpectedValueError,
    ValueTypeUnresolved,
)


class FlowRequestValidator:
    @staticmethod
    def load_api_or_tool_by_name(api_name: str = None, tool_func_name: str = None) -> Tool:
        # This is for legacy code tool loading
        result = None
        if api_name:
            result = BuiltinsManager.load_tool_by_api_name(api_name)
        if tool_func_name:
            result = FlowRequestValidator.load_tool_by_legacy_func_name(tool_func_name)
        return result

    @staticmethod
    def load_tool_by_legacy_func_name(tool_func_name: str) -> Tool:
        if tool_func_name is None:
            return None
        result = builtins.get(tool_func_name)
        if result is None:
            raise ToolNotFound(
                message=f"The tool '{tool_func_name}' is not found.",
                target=ErrorTarget.EXECUTOR,
            )
        return result

    @classmethod
    def resolve_node_llm_connection(cls, tool: Tool, node: Node, connection_manager: ConnectionManager) -> Node:
        # LLM connection is a separate field, the function will add it into node inputs.
        # The method is setup for legacy code compatible

        results = {}
        if not node.connection or tool.type != ToolType.LLM:
            # Return if no connection. For example, python tool
            return node
        # 1. ensure connection provided is available in the connection manager.
        connection = connection_manager.get(node.connection)

        # 2. Load provider/legacy tool, to check connection type is valid for the node.
        api_name = f"{node.provider}.{node.api}" if node.provider else None
        # Below is for legacy tool like Bing.Search
        tool_func_name = f"{tool.class_name}.{tool.function}" if tool.class_name else None
        # a. Get provider api for llm tool
        # or b. Get new definition of legacy python tool, as the old one doesn't have connection input

        tool_def = FlowRequestValidator.load_api_or_tool_by_name(api_name=api_name, tool_func_name=tool_func_name)
        # 3. Validate connection type: find the connection and get type class from inputs definition
        connection_type, key_name = None, None
        for key, input in tool_def.inputs.items():
            if not isinstance(input.type, List) or len(input.type) == 0:
                raise UnexpectedValueError(
                    message_format="Input Type is not specified in List for Node:{node_name}, input name:{input_name}",
                    node_name=node.name,
                    input_name=key,
                )
            typ = input.type[0]
            connection_type = ConnectionType.get_connection_class(typ)
            key_name = key
            if connection_type:
                break
        if not connection_type:
            raise InvalidConnectionType(
                message_format="Connection type can not be resolved for tool {tool_name}", tool_name=tool.name
            )
        if type(connection).__name__ not in tool_def.inputs[key_name].type:
            msg = (
                f"Invalid connection '{node.connection}' type {type(connection).__name__!r} "
                f"for node '{node.name}', valid types {tool_def.inputs[key_name].type}."
            )
            raise InvalidConnectionType(message=msg)
        # 4. Add connection to node inputs if it's valid
        results[key_name] = InputAssignment(value=connection)
        updated_node = copy.deepcopy(node)
        updated_node.inputs.update(results)
        return updated_node

    @classmethod
    def resolve_llm_connections(cls, flow: Flow, connections: dict) -> Flow:
        tools = {tool.name: tool for tool in flow.tools}
        connection_manager = ConnectionManager(connections)
        # Todo: confirm if we need flow copy here?
        updated_nodes = [
            cls.resolve_node_llm_connection(tools[node.tool], node, connection_manager) for node in flow.nodes
        ]
        updated_flow = copy.deepcopy(flow)
        updated_flow.nodes = updated_nodes
        return updated_flow

    @classmethod
    def _resolve_connections(cls, connections: dict) -> dict:
        connections = {k: v for k, v in connections.items()} if connections else {}
        connections_in_env = cls._get_connections_in_env()
        connections.update(connections_in_env)  # For local test
        return connections

    @classmethod
    def ensure_flow_valid(cls, flow: Flow, connections: dict) -> Flow:
        connections = cls._resolve_connections(connections)
        flow = cls.resolve_llm_connections(flow, connections)
        flow = cls._ensure_nodes_valid(flow, connections)
        flow.outputs = FlowValidator._ensure_outputs_valid(flow)
        return flow

    @classmethod
    def ensure_batch_inputs_type(
        cls,
        flow: Flow,
        batch_inputs: List[Dict[str, Any]],
    ) -> List[Mapping[str, Any]]:
        return [FlowValidator.ensure_flow_inputs_type(flow, inputs, idx) for idx, inputs in enumerate(batch_inputs)]

    @classmethod
    def ensure_variants_valid(
        cls,
        variants: Optional[Mapping[str, List[Node]]],
        variants_tools: Optional[List[Tool]],
        flow: Flow,
        connections,
    ) -> Mapping[str, List[Node]]:
        if not variants:
            return {}
        connections = cls._resolve_connections(connections)
        tools_mapping = {tool.name: tool for tool in flow.tools}
        if variants_tools:
            tools_mapping.update({tool.name: tool for tool in variants_tools})
        node_names = set(node.name for node in flow.nodes)
        updated_variants = {}
        for variant_id, nodes in variants.items():
            for node in nodes:
                if node.name not in node_names:
                    msg = f"Node '{node.name}' of variant '{variant_id}' is not in the flow."
                    raise NodeOfVariantNotFound(message=msg)
                if node.tool not in tools_mapping:
                    msg = (
                        f"Node '{node.name}' of variant '{variant_id}' references tool '{node.tool}' "
                        "which is not provided."
                    )
                    raise ToolOfVariantNotFound(message=msg)
            updated_variants[variant_id] = [
                FlowRequestValidator.ensure_node_inputs_type(tools_mapping[node.tool], node, connections)
                for node in nodes
            ]
        return updated_variants

    @staticmethod
    def _get_connections_in_env() -> dict:
        if "PROMPTFLOW_CONNECTIONS" in os.environ:
            return ConnectionManager.init_from_env().to_connections_dict()

        return dict()

    @staticmethod  # noqa: C901
    def _ensure_nodes_valid(flow: Flow, connections):  # noqa: C901
        flow = FlowValidator._validate_nodes_topology(flow)
        updated_nodes = []
        tools = {tool.name: tool for tool in flow.tools}
        for node in flow.nodes:
            if node.tool not in tools:
                msg = f"Node '{node.name}' references tool '{node.tool}' " + f"which is not in the flow '{flow.name}'."
                raise ToolNotFoundInFlow(message=msg)
            if tools[node.tool].type == ToolType.LLM and not node.api:
                msg = f"Please select connection for LLM node '{node.name}'."
                raise ConnectionNotSet(message=msg, target=ErrorTarget.EXECUTOR)
            updated_nodes.append(FlowRequestValidator.ensure_node_inputs_type(tools[node.tool], node, connections))
        flow = copy.copy(flow)
        flow.nodes = updated_nodes
        return flow

    @classmethod
    def resolve_llm_connection_to_input(cls, tool: Tool, node: Node, connection_manager: ConnectionManager):
        """LLM connection is a separate field, the function will add it into node inputs."""
        results = {}
        if not node.connection or tool.type != ToolType.LLM:
            # For LLM tool, the node.connections is not None; None for other tool types
            return results
        # Check if inputs already has resolved connection. If so, return without further processing.
        for key, value in node.inputs.items():
            if isinstance(value, InputAssignment) and ConnectionType.is_connection_value(value.value):
                results[key] = InputAssignment(value=value.value)
                return results
        # 1. ensure connection provided is available in the connection manager.
        connection = connection_manager.get(node.connection)
        if connection is None:
            raise ConnectionNotFound(
                message=f"Connection {node.connection!r} not found, available connection keys "
                f"{connection_manager._connections.keys()}.",
                target=ErrorTarget.EXECUTOR,
            )
        # 2. Load provider/legacy tool, to check connection type is valid for the node.
        api_name = f"{node.provider}.{node.api}" if node.provider else None
        # Get provider api for llm tool
        tool_def = BuiltinsManager.load_tool_by_api_name(api_name=api_name)
        # 3. Validate connection type: find the connection and get type class from inputs definition
        connection_type, key_name = None, None
        for key, input in tool_def.inputs.items():
            if not isinstance(input.type, List) or len(input.type) == 0:
                raise UnexpectedValueError(
                    message_format="Input Type is not specified in List for Node:{node_name}, input name:{input_name}",
                    node_name=node.name,
                    input_name=key,
                )
            typ = input.type[0]
            connection_type = ConnectionType.get_connection_class(typ)
            key_name = key
            if connection_type:
                break
        if not connection_type:
            raise InvalidConnectionType(
                message_format="Connection type can not be resolved for tool {tool_name}", tool_name=tool.name
            )
        if type(connection).__name__ not in tool_def.inputs[key_name].type:
            msg = (
                f"Invalid connection '{node.connection}' type {type(connection).__name__!r} "
                f"for node '{node.name}', valid types {tool_def.inputs[key_name].type}."
            )
            raise InvalidConnectionType(message=msg)
        # 4. Add connection to node inputs if it's valid
        results[key_name] = InputAssignment(value=connection)
        return results

    @classmethod
    def ensure_node_inputs_type(cls, tool: Tool, node: Node, connections):
        # Create connection manager for connection dict
        # prerequisite modules will be imported here
        connection_manager = ConnectionManager(connections)
        #  Remove null values include empty string and null
        updated_inputs = {
            k: v
            for k, v in node.inputs.items()
            if (v.value is not None and v.value != "") or v.value_type != InputValueType.LITERAL
        }
        # LLM connection is a separate field, the function will add it into node inputs.
        # Note: Add this before load provider, because init provider class requires connection.
        connection_input = FlowRequestValidator.resolve_llm_connection_to_input(tool, node, connection_manager)
        api_tool = None
        if BuiltinsManager.is_llm(tool):
            api_name = f"{node.provider}.{node.api}"
            # Get provider api for llm tool
            api_tool = BuiltinsManager.load_tool_by_api_name(api_name=api_name)
        for k, v in updated_inputs.items():
            if k not in tool.inputs and (not api_tool or api_tool and k not in api_tool.inputs):
                continue
            if v.value_type != InputValueType.LITERAL:
                continue
            tool_input = tool.inputs.get(k)
            if tool_input is None and api_tool:
                tool_input = api_tool.inputs.get(k)
            value_type = tool_input.type[0]
            updated_inputs[k] = copy.deepcopy(v)
            if ConnectionType.is_connection_class_name(value_type):
                connection_value = connection_manager.get(v.value)
                if not connection_value:
                    raise ConnectionNotFound(f"Connection {v.value} not found for node {node.name!r} input {k!r}.")
                # value is a connection
                updated_inputs[k].value = connection_value
                # Check if type matched
                if not any(type(connection_value).__name__ == typ for typ in tool_input.type):
                    msg = (
                        f"Input '{k}' for node '{node.name}' of type {type(connection_value).__name__!r}"
                        f" is not supported, valid types {tool_input.type}."
                    )
                    raise NodeInputValidationError(message=msg)
            elif isinstance(value_type, ValueType):
                try:
                    updated_inputs[k].value = value_type.parse(v.value)
                except Exception as e:
                    msg = f"Input '{k}' for node '{node.name}' of value {v.value} is not type {value_type}."
                    raise NodeInputValidationError(message=msg) from e
            else:
                # The value type is in ValueType enum or is connection type. null connection has been handled before.
                raise ValueTypeUnresolved(
                    f"Unresolved input type {value_type!r}, please check if it is supported in current version.",
                    target=ErrorTarget.EXECUTOR,
                )
        updated_inputs.update(connection_input)
        updated_node = copy.copy(node)
        updated_node.inputs = updated_inputs
        return updated_node
