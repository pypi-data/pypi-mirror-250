# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from enum import Enum
from typing import Dict, Sequence, Set, List, Any

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import MetricReader
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, SumAggregation, View

from promptflow._internal import ErrorResponse, get_logger
from promptflow.contracts.run_info import FlowRunInfo, RunInfo, Status

_logger = get_logger(__name__)

# define metrics dimension keys
FLOW_KEY = "flow"
RUN_STATUS_KEY = "run_status"
NODE_KEY = "node"
LLM_ENGINE_KEY = "llm_engine"
TOKEN_TYPE_KEY = "token_type"
RESPONSE_CODE_KEY = "response_code"
EXCEPTION_TYPE_KEY = "exception"
STREAMING_KEY = "streaming"
API_CALL_KEY = "api_call"
RESPONSE_TYPE_KEY = "response_type"  # firstbyte, lastbyte, default


class ResponseType(Enum):
    # latency from receving the request to sending the first byte of response, only applicable to streaming flow
    FirstByte = "firstbyte"
    # latency from receving the request to sending the last byte of response, only applicable to streaming flow
    LastByte = "lastbyte"
    # latency from receving the request to sending the whole response, only applicable to non-streaming flow
    Default = "default"


class LLMTokenType(Enum):
    PromptTokens = "prompt_tokens"
    CompletionTokens = "completion_tokens"


# define meter
meter = metrics.get_meter_provider().get_meter("Promptflow Standard Metrics")

# define metrics
token_consumption = meter.create_counter("Token_Consumption")
flow_latency = meter.create_histogram("Flow_Latency")
node_latency = meter.create_histogram("Node_Latency")
flow_request = meter.create_counter("Flow_Request")
remote_api_call_latency = meter.create_histogram("RPC_Latency")
remote_api_call_request = meter.create_counter("RPC_Request")
node_request = meter.create_counter("Node_Request")
# metrics for streaming
streaming_response_duration = meter.create_histogram("Flow_Streaming_Response_Duration")

HISTOGRAM_BOUNDARIES: Sequence[float] = (
    1.0,
    5.0,
    10.0,
    25.0,
    50.0,
    75.0,
    100.0,
    250.0,
    500.0,
    750.0,
    1000.0,
    2500.0,
    5000.0,
    7500.0,
    10000.0,
    25000.0,
    50000.0,
    75000.0,
    100000.0,
    300000.0,
)

# define metrics views
# token view
token_view = View(
    instrument_name="Token_Consumption",
    description="",
    attribute_keys={FLOW_KEY, NODE_KEY, LLM_ENGINE_KEY, TOKEN_TYPE_KEY},
    aggregation=SumAggregation(),
)
# latency view
flow_latency_view = View(
    instrument_name="Flow_Latency",
    description="",
    attribute_keys={FLOW_KEY, RESPONSE_CODE_KEY, STREAMING_KEY, RESPONSE_TYPE_KEY},
    aggregation=ExplicitBucketHistogramAggregation(boundaries=HISTOGRAM_BOUNDARIES),
)
node_latency_view = View(
    instrument_name="Node_Latency",
    description="",
    attribute_keys={FLOW_KEY, NODE_KEY, RUN_STATUS_KEY},
    aggregation=ExplicitBucketHistogramAggregation(boundaries=HISTOGRAM_BOUNDARIES),
)
flow_streaming_response_duration_view = View(
    instrument_name="Flow_Streaming_Response_Duration",
    description="during between sending the first byte and last byte of the response, only for streaming flow",
    attribute_keys={FLOW_KEY},
    aggregation=ExplicitBucketHistogramAggregation(boundaries=HISTOGRAM_BOUNDARIES),
)
# request view
request_view = View(
    instrument_name="Flow_Request",
    description="",
    attribute_keys={FLOW_KEY, RESPONSE_CODE_KEY, STREAMING_KEY, EXCEPTION_TYPE_KEY},
    aggregation=SumAggregation(),
)
node_request_view = View(
    instrument_name="Node_Request",
    description="",
    attribute_keys={FLOW_KEY, NODE_KEY, RUN_STATUS_KEY, EXCEPTION_TYPE_KEY},
    aggregation=SumAggregation(),
)
# Remote API call view
remote_api_call_latency_view = View(
    instrument_name="RPC_Latency",
    description="",
    attribute_keys={FLOW_KEY, NODE_KEY, API_CALL_KEY},
    aggregation=ExplicitBucketHistogramAggregation(boundaries=HISTOGRAM_BOUNDARIES),
)
remote_api_call_request_view = View(
    instrument_name="RPC_Request",
    description="",
    attribute_keys={FLOW_KEY, NODE_KEY, API_CALL_KEY, EXCEPTION_TYPE_KEY},
    aggregation=SumAggregation(),
)


class MetricsRecorder(object):
    """OpenTelemetry Metrics Recorder"""

    def __init__(self, extra_reader: MetricReader = None, common_dimensions: Dict[str, str] = None) -> None:
        """initialize metrics recorder

        :param extra_reader: extra metric reader
        :param common_dimensions: common dimensions for all metrics
        """
        self.common_dimensions = common_dimensions or {}
        self.extra_reader = extra_reader
        dimension_keys = {key for key in common_dimensions}
        config_common_monitor(dimension_keys, extra_reader)

    def record_flow_request(self, flow_id: str, response_code: int, exception: str, streaming: bool):
        try:
            flow_request.add(
                1,
                {
                    FLOW_KEY: flow_id,
                    RESPONSE_CODE_KEY: str(response_code),
                    EXCEPTION_TYPE_KEY: exception,
                    STREAMING_KEY: str(streaming),
                    **self.common_dimensions,
                },
            )
        except Exception as e:
            _logger.warning("failed to record flow request metrics: %s", e)

    def record_flow_latency(
        self, flow_id: str, response_code: int, streaming: bool, response_type: str, duration: float
    ):
        try:
            flow_latency.record(
                duration,
                {
                    FLOW_KEY: flow_id,
                    RESPONSE_CODE_KEY: str(response_code),
                    STREAMING_KEY: str(streaming),
                    RESPONSE_TYPE_KEY: response_type,
                    **self.common_dimensions,
                },
            )
        except Exception as e:
            _logger.warning("failed to record flow latency metrics: %s", e)

    def record_flow_streaming_response_duration(self, flow_id: str, duration: float):
        try:
            streaming_response_duration.record(duration, {FLOW_KEY: flow_id, **self.common_dimensions})
        except Exception as e:
            _logger.warning("failed to record streaming duration metrics: %s", e)

    def record_tracing_metrics(self, flow_run: FlowRunInfo, node_runs: Dict[str, RunInfo]):
        try:
            for _, run in node_runs.items():
                flow_id = flow_run.flow_id if flow_run is not None else "default"
                if len(run.system_metrics) > 0:
                    duration = run.system_metrics.get("duration", None)
                    if duration is not None:
                        duration = duration * 1000
                        node_latency.record(
                            duration,
                            {
                                FLOW_KEY: flow_id,
                                NODE_KEY: run.node,
                                RUN_STATUS_KEY: run.status.value,
                                **self.common_dimensions,
                            },
                        )
                    # openai token metrics
                    inputs = run.inputs or {}
                    engine = inputs.get("deployment_name") or ""
                    for token_type in [LLMTokenType.PromptTokens.value, LLMTokenType.CompletionTokens.value]:
                        count = run.system_metrics.get(token_type, None)
                        if count:
                            token_consumption.add(
                                count,
                                {
                                    FLOW_KEY: flow_id,
                                    NODE_KEY: run.node,
                                    LLM_ENGINE_KEY: engine,
                                    TOKEN_TYPE_KEY: token_type,
                                    **self.common_dimensions,
                                },
                            )
                # record node request metric
                err = None
                if run.status != Status.Completed:
                    err = "unknown"
                    if isinstance(run.error, dict):
                        err = self.get_exact_error(run.error)
                    elif isinstance(run.error, str):
                        err = run.error

                node_request.add(
                    1,
                    {
                        FLOW_KEY: flow_id,
                        NODE_KEY: run.node,
                        RUN_STATUS_KEY: run.status.value,
                        EXCEPTION_TYPE_KEY: err,
                        **self.common_dimensions,
                    },
                )

                if run.api_calls and len(run.api_calls) > 0:
                    for api_call in run.api_calls:
                        # since first layer api_call is the node call itself, we ignore them here
                        api_calls: List[Dict[str, Any]] = api_call.get("children", None)
                        if api_calls is None:
                            continue
                        self.record_api_call_metrics(flow_id, run.node, api_calls)
        except Exception as e:
            _logger.warning(f"failed to record metrics: {e}, flow_run: {flow_run}, node_runs: {node_runs}")

    def get_exact_error(self, err: Dict):
        error_response = ErrorResponse.from_error_dict(err)
        return error_response.innermost_error_code

    def record_api_call_metrics(self, flow_id, node, api_calls: List[Dict[str, Any]], prefix: str = None):
        if api_calls and len(api_calls) > 0:
            for api_call in api_calls:
                cur_name = api_call.get("name")
                api_name = "_".join(prefix, cur_name) if prefix else cur_name
                # api-call latency metrics
                # sample data: {"start_time":1688462182.744916, "end_time":1688462184.280989}
                start_time = api_call.get("start_time", None)
                end_time = api_call.get("end_time", None)
                if start_time and end_time:
                    api_call_latency_ms = (end_time - start_time) * 1000
                    remote_api_call_latency.record(
                        api_call_latency_ms,
                        {
                            FLOW_KEY: flow_id,
                            NODE_KEY: node,
                            API_CALL_KEY: api_name,
                            **self.common_dimensions,
                        },
                    )
                # remote api call request metrics
                err = api_call.get("error") or {}
                if isinstance(err, dict):
                    exception_type = self.get_exact_error(err)
                else:
                    exception_type = err
                remote_api_call_request.add(
                    1,
                    {
                        FLOW_KEY: flow_id,
                        NODE_KEY: node,
                        API_CALL_KEY: api_name,
                        EXCEPTION_TYPE_KEY: exception_type,
                        **self.common_dimensions,
                    },
                )
                child_api_calls = api_call.get("children", None)
                if child_api_calls:
                    self.record_api_call_metrics(flow_id, node, child_api_calls, api_name)


# configure monitor, by default only expose prometheus metrics
def config_common_monitor(common_keys: Set[str] = {}, extra_reader: MetricReader = None):
    prometheus_reader = PrometheusMetricReader()
    metrics_views = [
        token_view,
        flow_latency_view,
        node_latency_view,
        request_view,
        remote_api_call_latency_view,
        remote_api_call_request_view,
    ]
    for view in metrics_views:
        view._attribute_keys.update(common_keys)

    readers = [prometheus_reader]
    if extra_reader:
        readers.append(extra_reader)

    meter_provider = MeterProvider(
        metric_readers=readers,
        views=metrics_views,
    )
    set_meter_provider(meter_provider)
