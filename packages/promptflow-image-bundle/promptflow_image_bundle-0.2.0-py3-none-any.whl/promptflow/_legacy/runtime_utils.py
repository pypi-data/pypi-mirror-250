import os
from contextlib import contextmanager
from typing import List, Optional

from promptflow._internal import AbstractCacheManager, BuiltinsManager, ConnectionManager, OperationContext
from promptflow._legacy.contracts import BatchFlowRequest, EvalRequest, LegacyRunMode
from promptflow._legacy.data import load_data
from promptflow._legacy.executor import FlowExecutionCoodinator
from promptflow.contracts.run_mode import RunMode
from promptflow.exceptions import ErrorTarget, UserErrorException
from promptflow.runtime.constants import PromptflowEdition
from promptflow.runtime.contracts.azure_storage_setting import AzureStorageSetting
from promptflow.runtime.contracts.runtime import SubmitFlowRequest
from promptflow.runtime.data import prepare_data
from promptflow.runtime.runtime_config import RuntimeConfig
from promptflow.runtime.utils import logger
from promptflow.runtime.utils.internal_logger_utils import (
    FileType,
    SystemLogContext,
    close_telemetry_log_handler,
    reset_telemetry_log_handler,
)
from promptflow.runtime.utils.timer import Timer

DATA_PREFIX = "data."


def parse_data_mapping(s):
    if not s.startswith(DATA_PREFIX):
        return None
    return s[len(DATA_PREFIX) :]


def get_required_inputs(submit_request: SubmitFlowRequest) -> set:
    """get required inputs from flow"""
    req = submit_request.submission_data
    flow_inputs = set(req.flow.inputs.keys())
    if isinstance(req, EvalRequest):
        #  If mapping is not provided, simply use the flow inputs
        if req.inputs_mapping is None:
            return flow_inputs
        return {parse_data_mapping(v) for v in req.inputs_mapping.values() if v.startswith(DATA_PREFIX)}

    if isinstance(req, BatchFlowRequest) and req.eval_flow_inputs_mapping:
        eval_data_inputs = {
            parse_data_mapping(v) for v in req.eval_flow_inputs_mapping.values() if v.startswith(DATA_PREFIX)
        }
        return flow_inputs | eval_data_inputs

    return flow_inputs


def resolve_data(submit_flow_request: SubmitFlowRequest, destination: str, runtime_config: RuntimeConfig):
    """resolve data uri"""
    run_mode = submit_flow_request.run_mode

    inputs = get_required_inputs(submit_flow_request)

    if run_mode in (LegacyRunMode.Flow, run_mode.BulkTest) and submit_flow_request.batch_data_input:
        data_uri = submit_flow_request.batch_data_input.data_uri
        if data_uri:
            data = resolve_data_from_uri(data_uri, destination, runtime_config, inputs)
            req: BatchFlowRequest = submit_flow_request.submission_data
            req.batch_inputs = data

    if run_mode == LegacyRunMode.Eval and submit_flow_request.bulk_test_data_input:
        data_uri = submit_flow_request.bulk_test_data_input.data_uri
        if data_uri:
            data = resolve_data_from_uri(data_uri, destination, runtime_config, inputs)
            req_eval: EvalRequest = submit_flow_request.submission_data
            req_eval.bulk_test_inputs = data


def resolve_data_from_uri(data_uri, destination: str, runtime_config: RuntimeConfig, inputs: set):
    data = None
    if data_uri:
        from promptflow.runtime.utils._token_utils import get_default_credential

        with Timer(logger, "Resolve data from url"):
            credential = get_default_credential()
            # resolve data uri to local data
            local_file, _ = prepare_data(
                data_uri, destination=destination, credential=credential, runtime_config=runtime_config
            )

            data = load_data(local_file, logger=logger)
            if not data:
                raise EmptyDataResolved(message_format="resolve empty data from data_uri")

            # filter cols that exists in inputs
            result = []
            for line in data:
                r = {}
                for k, v in line.items():
                    if k in inputs:
                        r[k] = v
                result.append(r)
            data = result
            logger.info(
                "Resolved %s lines of data from uri: {customer_content}",
                len(data),
                extra={"customer_content": data_uri},
            )
    return data


def get_credential_list_from_request(request: SubmitFlowRequest) -> List[str]:
    """Get credential list from submission data.

    Credentials include:
        1. api keys in connections;
        2. app insights instrumentation key.
    """
    connections = request.submission_data.connections
    credential_list = ConnectionManager(connections).get_secret_list()
    if request.app_insights_instrumentation_key:
        credential_list.append(request.app_insights_instrumentation_key)
    return credential_list


def get_log_context(
    request: SubmitFlowRequest,
    run_id: Optional[str] = None,
) -> SystemLogContext:
    if run_id is None:
        run_id = request.flow_run_id
    file_path = request.run_id_to_log_path.get(run_id) if request.run_id_to_log_path else None
    edition = OperationContext.get_instance().get("edition", PromptflowEdition.COMMUNITY)
    file_type = FileType.Blob if edition == PromptflowEdition.ENTERPRISE else FileType.Local
    # convert LegacyRunMode to RunMode
    executor_run_mode: RunMode = request.run_mode.get_executor_run_mode() if request.run_mode is not None else None
    # Add root_flow_run_id and run_mode into logger's custom dimensions.
    custom_dimensions = {
        "root_flow_run_id": request.flow_run_id,
        "run_mode": request.run_mode.name if request.run_mode is not None else "",
    }
    return SystemLogContext(
        file_path=file_path,
        run_mode=executor_run_mode,
        credential_list=get_credential_list_from_request(request),
        file_type=file_type,
        custom_dimensions=custom_dimensions,
        app_insights_instrumentation_key=request.app_insights_instrumentation_key,
        input_logger=logger,
    )


@contextmanager
def reset_and_close_logger():
    """
    In child process, reset telemetry handler,
    because the previous thread in parent process won't work in this process.
    After, close handler otherwise logs will be lost.
    """
    reset_telemetry_log_handler(logger)
    try:
        yield
    finally:
        close_telemetry_log_handler(logger)


def set_environment_variables(env_vars: dict):
    """set environment variables."""
    if env_vars:
        for key, value in env_vars.items():
            os.environ[key] = value


def get_executor(
    config: RuntimeConfig,
    workspace_access_token: str = None,
    azure_storage_setting: AzureStorageSetting = None,
    run_mode: RunMode = None,
):
    """get executor."""
    from promptflow._internal import RunTracker

    builtins_manager = BuiltinsManager()
    run_storage = config.get_run_storage(
        workspace_access_token=workspace_access_token, azure_storage_setting=azure_storage_setting, run_mode=run_mode
    )
    cache_manager = AbstractCacheManager.init_from_env()
    run_tracker = RunTracker(run_storage)
    return FlowExecutionCoodinator(
        builtins_manager=builtins_manager,
        cache_manager=cache_manager,
        run_tracker=run_tracker,
    )


class EmptyDataResolved(UserErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.RUNTIME, **kwargs)
