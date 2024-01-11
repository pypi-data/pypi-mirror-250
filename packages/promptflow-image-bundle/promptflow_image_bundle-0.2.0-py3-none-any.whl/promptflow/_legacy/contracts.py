import copy
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Union

from promptflow.contracts.flow import Flow, Node, Tool
from promptflow.contracts.run_mode import RunMode


@dataclass
class BaseFlowRequest:
    flow: Optional[Flow]
    connections: Dict[str, Dict[str, str]]


BASELINE_VARIANT_ID = "variant0"


@dataclass
class BatchFlowRequest(BaseFlowRequest):
    batch_inputs: List[Dict[str, Any]]
    name: str = ""
    description: str = ""
    tags: Mapping[str, str] = None

    baseline_variant_id: str = ""
    variants: Dict[str, List[Node]] = None
    variants_tools: List[Tool] = None
    variants_codes: Dict[str, str] = None
    variants_runs: Dict[str, str] = None

    bulk_test_id: Optional[str] = None

    eval_flow: Optional[Flow] = None
    eval_flow_run_id: Optional[str] = None
    eval_flow_inputs_mapping: Optional[Mapping[str, str]] = None

    @staticmethod
    def deserialize(data: dict) -> "BatchFlowRequest":
        return BatchFlowRequest(
            flow=Flow.deserialize(data["flow"]) if "flow" in data else None,
            connections=data.get("connections", {}),
            batch_inputs=data.get("batch_inputs", []),
            name=data.get("name", ""),
            description=data.get("description", ""),
            tags=data.get("tags", {}),
            baseline_variant_id=data.get("baseline_variant_id", ""),
            variants={
                variant_id: [Node.deserialize(node) for node in nodes]
                for variant_id, nodes in data.get("variants", {}).items()
            },
            variants_tools=[Tool.deserialize(t) for t in data.get("variants_tools", [])],
            variants_runs=data.get("variants_runs", {}),
            variants_codes=data.get("variants_codes", {}),
            bulk_test_id=data.get("bulk_test_id", None),
            eval_flow=Flow.deserialize(data["eval_flow"]) if data.get("eval_flow", None) else None,
            eval_flow_run_id=data.get("eval_flow_run_id"),
            eval_flow_inputs_mapping=data.get("eval_flow_inputs_mapping", {}),
        )


@dataclass
class NodesRequest(BaseFlowRequest):
    node_name: str
    node_inputs: Dict[str, Any]
    variants: Dict[str, List[Node]] = None
    variants_tools: List[Tool] = None
    variants_codes: Dict[str, str] = None

    @staticmethod
    def deserialize(data: dict) -> "NodesRequest":
        return NodesRequest(
            Flow.deserialize(data["flow"]) if "flow" in data else None,
            data.get("connections", {}),
            data["node_name"],
            data["node_inputs"],
            variants={
                variant_id: [Node.deserialize(node) for node in nodes]
                for variant_id, nodes in data.get("variants", {}).items()
            },
            variants_tools=[Tool.deserialize(t) for t in data.get("variants_tools", [])],
            variants_codes=data.get("variants_codes", {}),
        )

    @staticmethod
    def get_node_name_from_node_inputs_key(k: str) -> str:
        """
        Node input keys might have the format: {node name}.output
        Strip .output and return node name in this case.
        """
        if k.endswith(".output"):
            return k[: -len(".output")]
        return k

    def get_node_connection_names(self, run_mode):
        # Get the connection name from node_input(Python) and connection field(LLM) for current node.
        node = next((n for n in self.flow.nodes if n.name == self.node_name), None)
        if node is None:
            raise ValueError(f"Node name {self.node_name} not found in flow nodes.")
        # Create a new flow, leave node to execute only and update the inputs.
        new_flow = copy.deepcopy(self.flow)
        node_idx, node = next(
            ((_idx, n) for _idx, n in enumerate(new_flow.nodes) if n.name == self.node_name), (None, None)
        )
        from promptflow._legacy.contracts import LegacyRunMode

        # If run_mode is SingleNode, only keep the node to execute, if is FromNode then nodes after it.
        if run_mode == LegacyRunMode.SingleNode:
            new_flow.nodes = [node]
        elif run_mode == LegacyRunMode.FromNode:
            new_flow.nodes = new_flow.nodes[node_idx:]
        else:
            raise NotImplementedError(f"Run mode {run_mode} is not supported in current version.")
        return new_flow.get_connection_names()


@dataclass
class EvalRequest(BaseFlowRequest):
    bulk_test_inputs: List[Mapping[str, Any]]
    bulk_test_flow_run_ids: List[str]
    bulk_test_flow_id: str
    bulk_test_id: str
    inputs_mapping: Optional[Mapping[str, str]] = None

    @staticmethod
    def deserialize(data: dict) -> "EvalRequest":
        return EvalRequest(
            Flow.deserialize(data["flow"]) if "flow" in data else None,
            connections=data.get("connections", {}),
            bulk_test_inputs=data.get("bulk_test_inputs", []),
            bulk_test_flow_run_ids=data["bulk_test_flow_run_ids"],
            bulk_test_flow_id=data["bulk_test_flow_id"],
            bulk_test_id=data["bulk_test_id"],
            inputs_mapping=data.get("inputs_mapping"),
        )


class LegacyRunMode(int, Enum):
    Flow = 0
    SingleNode = 1
    FromNode = 2
    BulkTest = 3
    Eval = 4

    @classmethod
    def parse(cls, value: Union[str, int]):
        """Parse string to LegacyRunMode."""
        if isinstance(value, int):
            return LegacyRunMode(value)
        if not isinstance(value, str):
            raise ValueError(f"Invalid value type to parse: {type(value)}")
        if value == "SingleNode":
            return LegacyRunMode.SingleNode
        elif value == "FromNode":
            return LegacyRunMode.FromNode
        elif value == "BulkTest":
            return LegacyRunMode.BulkTest
        elif value == "Eval":
            return LegacyRunMode.Eval
        else:
            return LegacyRunMode.Flow

    def get_executor_run_mode(self) -> RunMode:
        """Convert LegacyRunMode to RunMode."""
        if self == LegacyRunMode.SingleNode:
            return RunMode.SingleNode
        elif self == LegacyRunMode.FromNode:
            return RunMode.SingleNode
        elif self == LegacyRunMode.BulkTest:
            return RunMode.Batch
        elif self == LegacyRunMode.Eval:
            return RunMode.Batch
        else:
            return RunMode.Test
