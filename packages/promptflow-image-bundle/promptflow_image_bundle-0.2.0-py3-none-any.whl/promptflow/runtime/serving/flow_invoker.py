import json
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional, Tuple

from promptflow._internal import (
    AbstractCacheManager,
    BuiltinsManager,
    DefaultToolInvoker,
    RunTracker,
    ToolInvoker,
    convert_multimedia_data_to_base64,
    inject_openai_api,
    load_json,
)
from promptflow.contracts.flow import Flow
from promptflow.contracts.run_info import FlowRunInfo
from promptflow.contracts.run_info import RunInfo as NodeRunInfo
from promptflow.contracts.tool import ToolType
from promptflow.exceptions import ValidationException
from promptflow.executor.flow_executor import FlowExecutor
from promptflow.runtime._errors import ConnectionDataInvalidError
from promptflow.runtime.constants import DEFAULT_FLOW_YAML_FILE
from promptflow.runtime.serving._errors import ToolLoadError, ToolNotFoundInFlow, ToolTypeNotSupported
from promptflow.runtime.serving.flow_request_validator import FlowRequestValidator
from promptflow.runtime.serving.utils import normalize_connection_name
from promptflow.runtime.storage.run_storage import AbstractRunStorage
from promptflow.runtime.utils import logger
from promptflow.runtime.utils._utils import decode_dict


@dataclass
class FlowResult:
    """The result of a flow call."""

    output: Mapping[str, Any]  # The output of the line.
    run_info: FlowRunInfo  # The run info of the line.
    node_run_infos: Mapping[str, NodeRunInfo]  # The run info of the nodes in the line.


class ConnectionLoadingType(Enum):
    Workspace = "workspace"
    Environment = "environment"


class FlowInvoker:
    """The invoker of a flow."""

    def __init__(
        self,
        flow_file: Path,
        stream_required: Callable[[], bool],
        conn_loading_type: ConnectionLoadingType,
        **kwargs: Any,
    ):
        self._flow_loaded = False
        self._flow_file = flow_file

        self._builtins_manager = BuiltinsManager()
        self._cache_manager = AbstractCacheManager.init_from_env()
        self._run_tracker = RunTracker(AbstractRunStorage.init_from_env())

        # Inject OpenAI API to make sure traces and headers injection works and
        # update OpenAI API configs from environment variables.
        inject_openai_api()
        ToolInvoker.activate(DefaultToolInvoker())
        self.try_import_builtins()

        self._executor: FlowExecutor = None
        self._stream_required = stream_required
        self._conn_loading_type = conn_loading_type
        self._subscription_id = kwargs.get("subscription_id", None)
        self._resource_group = kwargs.get("resource_group", None)
        self._workspace_name = kwargs.get("workspace_name", None)
        try:
            self._try_load()
        except Exception as e:
            logger.warn(f"Flow invoker load flow failed: {e}")

    @staticmethod
    def try_import_builtins():
        """Try to import builtins to make sure they are available in the current environment.

        This is only required for legacy environment where the tool is resolved by builtins dictionary.
        """
        from promptflow._internal import register_builtins
        from promptflow.tools import SerpAPI  # noqa: F401

        register_builtins(SerpAPI)

    def load_success(self) -> bool:
        return self._flow_loaded

    def invoke(self, data, run_id=None, allow_generator_output=False) -> FlowResult:
        """Invoke the flow with the given data."""
        if not self._flow_loaded:
            self._try_load()
        result = self._executor.exec_line(data, run_id=run_id, allow_generator_output=allow_generator_output)
        # Get base64 for multi modal object
        resolved_outputs = self._convert_multimedia_data_to_base64(result)
        return FlowResult(
            output=resolved_outputs or {},
            run_info=result.run_info,
            node_run_infos=result.node_run_infos,
        )

    def _convert_multimedia_data_to_base64(self, invoke_result):
        resolved_outputs = {
            k: convert_multimedia_data_to_base64(v, with_type=True, dict_type=True)
            for k, v in invoke_result.output.items()
        }
        return resolved_outputs

    @property
    def flow(self) -> Flow:
        if not self._flow_loaded:
            self._try_load()
        return self._executor._flow

    def _try_load(self):
        logger.info("Try loading connections...")
        connections = self._load_connection(self._flow_file)
        logger.info("Loading flow...")
        # TODO: change to FlowExecutor.create() once the old contract is not supported
        self._executor = self.create_flow_executor_by_model(flow_file=self._flow_file, connections=connections)
        self._executor._raise_ex = False
        self._executor.enable_streaming_for_llm_flow(self._stream_required)
        self._flow_loaded = True
        logger.info("Flow loaded successfully.")

    def _load_connection(self, flow_file: Path):
        if self._conn_loading_type == ConnectionLoadingType.Workspace:
            logger.info("Promptflow serving runtime start getting connections from workspace...")
            connections = _prepare_workspace_connections(
                flow_file, self._subscription_id, self._resource_group, self._workspace_name
            )
        else:
            connections = _prepare_env_connections()
        logger.info(f"Promptflow serving runtime get connections successfully. keys: {connections.keys()}")
        return connections

    def create_flow_executor_by_model(
        self,
        flow_file: Path,
        connections: dict,
        node_overrides: Optional[Dict[str, str]] = None,
    ):
        """Here we assume all the tools are in the same directory as the flow file."""
        flow_file = self._resolve_flow_file(flow_file)
        if flow_file.suffix == ".json":
            # For backward compatibility to support json flow file
            return self._create_flow_executor_by_json(flow_file, connections, node_overrides=node_overrides)
        return FlowExecutor.create(flow_file, connections, raise_ex=False, node_override=node_overrides)

    def _create_flow_executor_by_json(self, flow_file: Path, connections: dict, node_overrides):
        model_dir = flow_file.resolve().parent
        flow = Flow.deserialize(load_json(flow_file))
        flow = flow._apply_node_overrides(node_overrides)
        # Connection required modules will be imported after ensure flow valid
        flow = FlowRequestValidator.ensure_flow_valid(flow, connections)
        self._assign_node_type_according_to_tool_type(flow)

        for tool in flow.tools:
            if tool.source and not tool.code:
                tool.code = (model_dir / tool.source).read_text(encoding="utf-8")
        return self.create_flow_executor(flow, connections, raise_ex=True)

    def create_flow_executor(self, flow: Flow, connections: dict, raise_ex=False):
        loaded_tools = self._load_tools_and_update_node_inputs(flow)
        return FlowExecutor(
            flow=flow,
            connections=connections,
            run_tracker=self._run_tracker,
            cache_manager=self._cache_manager,
            loaded_tools=loaded_tools,
            raise_ex=raise_ex,
        )

    def _load_tools_and_update_node_inputs(self, flow: Flow) -> Mapping[str, Callable]:
        loaded_tools = {}
        tool_metas = {tool.name: tool for tool in flow.tools}
        for node in flow.nodes:
            if node.tool not in tool_metas:
                msg = f"Node '{node.name}' references tool '{node.tool}' which is not in the flow '{flow.name}'."
                raise ToolNotFoundInFlow(message=msg)
            # We may also load other non python tools here
            tool = tool_metas[node.tool]
            if BuiltinsManager.is_custom_python(tool):
                continue  # Here we skip custom python tools, they will be loaded later

            api_name = f"{node.provider}.{node.api}"
            try:
                # There are some class init input in node inputs so we need to pass them
                loaded_tool, init_inputs = self._load_tool(tool, api_name, node.inputs)
                loaded_tools[node.name] = loaded_tool
            except ValidationException as e:
                raise e
            except Exception as e:
                raise ToolLoadError(
                    message=f"Failed to load tool '{tool.name}' for node '{node.name}' due to '{e}'."
                ) from e
            # Remove init inputs from node inputs, keep function inputs only
            node.inputs = {k: v for k, v in node.inputs.items() if k not in init_inputs}
        return loaded_tools

    def _load_tool(self, tool, api_name, node_inputs) -> Tuple[Callable, dict]:
        builtins_manager = BuiltinsManager()
        if BuiltinsManager.is_builtin(tool) or tool.type is ToolType._ACTION:
            return builtins_manager.load_builtin(tool, node_inputs)
        elif tool.type is ToolType.LLM:
            api = builtins_manager.load_tool_by_api_name(api_name)
            return builtins_manager.load_prompt_with_api(tool, api, node_inputs)
        elif tool.type is ToolType.PROMPT:
            return builtins_manager.load_prompt_rendering(tool), {}
        else:
            raise ToolTypeNotSupported(message=f"Unsupported tool {tool.name}.")

    @staticmethod
    def _assign_node_type_according_to_tool_type(flow: Flow):
        """
        Assign correct value to node.type.

        The new contract added `type` property to `node`.
        This method sets the type for each node according to the tool type to align with the new contract.
        """
        for node in flow.nodes:
            tool = flow.get_tool(node.tool)
            if not tool:
                raise ToolNotFoundInFlow(
                    message_format="Unable update `node.type` due to tool '{tool_name}' not found.",
                    tool_name=node.tool,
                )
            node.type = tool.type

    @staticmethod
    def _resolve_flow_file(flow_file: Path):
        flow_file = Path(flow_file)
        if flow_file.is_dir():
            if (flow_file / DEFAULT_FLOW_YAML_FILE).exists():
                flow_file = flow_file / DEFAULT_FLOW_YAML_FILE
            # For backward compatibility to support json flow file, will be deprecated
            elif (flow_file / "flow.json").exists():
                flow_file = flow_file / "flow.json"
            else:
                raise FileNotFoundError(f"Cannot find flow file in {flow_file}")
        return flow_file


def _prepare_workspace_connections(flow_file, subscription_id, resource_group, workspace_name):
    flow_file = Path(flow_file)
    # Resolve connection names from flow.
    logger.info("Reading flow from model ...")
    flow = Flow.from_yaml(flow_file)
    logger.info("Getting connection names for flow ...")
    connection_names = flow.get_connection_names()
    # add connection override support. PF serving supports two kinds of connection override:
    # 1. name override, name override only supports overriding with connection in the same workspace.
    # sample: <connection_name_in_flow>=<new_connection_name_in_ws>
    # 2. data override with MIR secret injection. This way we will get the whole connection data directly.
    # sample: <connection_name_in_flow>=${{azureml://connections/<conn_name>}}
    from promptflow.runtime.connections import build_connection_dict, build_connection_dict_from_rest_object
    from promptflow.runtime.models import WorkspaceConnectionPropertiesV2BasicResource

    connections = {}
    connections_to_fetch = []
    connections_name_overrides = {}
    for connection_name in connection_names:
        # replace " " with "_" in connection name
        normalized_name = normalize_connection_name(connection_name)
        if normalized_name in os.environ:
            override_conn = os.environ[normalized_name]
            data_override = False
            # try load connection as a json, for case 2 we will directly get a connection json string
            try:
                # data override
                conn_data = json.loads(override_conn)
                data_override = True
            except ValueError:
                # name override
                logger.info(f"Connection value is not json format, enable name override for {connection_name}.")
                connections_name_overrides[override_conn] = connection_name
                connections_to_fetch.append(override_conn)
            if data_override:
                try:
                    conn_data = WorkspaceConnectionPropertiesV2BasicResource.deserialize(conn_data)
                    connections[connection_name] = build_connection_dict_from_rest_object(connection_name, conn_data)
                except Exception as e:
                    error_msg = f"Override connection {connection_name} with invalid connection data."
                    raise ConnectionDataInvalidError(message=error_msg) from e
        else:
            connections_to_fetch.append(connection_name)

    if len(connections_name_overrides) > 0:
        logger.info(f"Connection name overrides: {connections_name_overrides}")
    if len(connections) > 0:
        logger.info(f"Connections data overrides: {connections.keys()}")

    logger.info(f"Getting connection from workspace... connection names: {connections_to_fetch}")
    # Get workspace connection and return as a dict.
    fetched_connections = build_connection_dict(connections_to_fetch, subscription_id, resource_group, workspace_name)
    for name, conn in fetched_connections.items():
        if name in connections_name_overrides:
            connections[connections_name_overrides[name]] = conn
        else:
            connections[name] = conn
    return connections


def _prepare_env_connections():
    # TODO: support loading from environment once secret injection is ready
    # For local test app connections will be set.
    env_connections = os.getenv("PROMPTFLOW_ENCODED_CONNECTIONS", None)
    if not env_connections:
        logger.info("Promptflow serving runtime received no connections from environment!!!")
        connections = {}
    else:
        connections = decode_dict(env_connections)
    return connections
