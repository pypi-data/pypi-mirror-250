import contextvars
import multiprocessing
import os
import shutil
import threading
import time
from pathlib import Path
from typing import Dict, List

import psutil
from psutil import NoSuchProcess

from promptflow._internal import OperationContext, set_context, update_log_path
from promptflow._legacy.contracts import LegacyRunMode
from promptflow._legacy.executor import FlowExecutionCoodinator
from promptflow._legacy.runtime_utils import (
    get_executor,
    get_log_context,
    reset_and_close_logger,
    resolve_data,
    set_environment_variables,
)
from promptflow.contracts.run_info import Status
from promptflow.runtime._errors import FlowRunTimeoutError
from promptflow.runtime.contracts.runtime import SubmitFlowRequest
from promptflow.runtime.runtime_config import RuntimeConfig
from promptflow.runtime.utils import logger, multi_processing_exception_wrapper
from promptflow.runtime.utils._utils import get_storage_from_config
from promptflow.runtime.utils.internal_logger_utils import system_logger
from promptflow.runtime.utils.retry_utils import retry
from promptflow.runtime.utils.thread_utils import timeout

STATUS_CHECKER_INTERVAL = 20  # seconds
MONITOR_REQUEST_TIMEOUT = 10  # seconds
SYNC_SUBMISSION_TIMEOUT = 330  # seconds
WAIT_SUBPROCESS_EXCEPTION_TIMEOUT = 10  # seconds


def execute_request(config: RuntimeConfig, request: SubmitFlowRequest):
    """execute request in child process."""
    origin_wd = os.getcwd()
    executor = None
    working_dir = None
    try:
        # pre process: set environment variables & prepare input data
        set_environment_variables(request.environment_variables)
        token = request.workspace_msi_token_for_storage_resource
        executor = get_executor(
            config,
            workspace_access_token=token,
            azure_storage_setting=request.azure_storage_setting,
            run_mode=request.run_mode.get_executor_run_mode() if request.run_mode is not None else None,
        )
        # enrich run tracker with the run mode, to determine if we need to update run history
        executor._run_tracker._run_mode = request.run_mode

        assert request.flow_run_id

        working_dir = Path(f"requests/{request.flow_run_id}")
        working_dir.mkdir(parents=True, exist_ok=True)
        # For non-code first, we don't have flow_source in request, remove corresponding code
        if request.flow_source is not None:
            logger.info("Flow source is not None, which is not expected for v1 case.")
        os.chdir(working_dir)

        # resolve data in user folder
        resolve_data(request, destination="./inputs", runtime_config=config)

        # execute
        # When it is CI compute and AzureFileShare flow source, working dir may be customer content
        logger.info(
            "Start execute request: %s in dir {customer_content}...",
            request.flow_run_id,
            extra={"customer_content": working_dir},
        )
        result = executor.exec_request_raw(request)
    finally:
        os.chdir(origin_wd)
        # post process: clean up and restore working dir
        # note: no need to clean environment variables, because they are only set in child process
        if working_dir and not config.execution.debug:
            logger.info("Cleanup working dir %s", working_dir)
            shutil.rmtree(working_dir, ignore_errors=True)

    return result


def start_thread_to_monitor_request_handler_process(config: RuntimeConfig, request: SubmitFlowRequest, process):
    """Start a thread to monitor request handler process.
    When request cancel is received, it will
    1. terminate the request handler process.
    2. mark the run as canceled.
    """
    token = request.workspace_msi_token_for_storage_resource
    bulk_test_run_ids = FlowExecutionCoodinator.get_bulk_test_variants_run_ids(req=request)

    def get_run_ids_status(run_ids):
        storage = get_storage_from_config(config, token=token)
        status = {}
        for run_id in run_ids:
            run_status = storage.get_run_status(run_id=run_id)
            status[run_id] = run_status
        return status

    def terminate_process():
        if process.is_alive():
            children = psutil.Process(process.pid).children(recursive=True)
            for child in children:
                try:
                    child.terminate()
                    system_logger.info("Successfully terminated child process with pid %s", child.pid)
                except NoSuchProcess:
                    system_logger.info("Child process %s already terminated and not found, skipping", child.pid)
                    pass
            process.terminate()
            system_logger.info("Successfully terminated process with pid %s", process.pid)
        else:
            system_logger.info("Process already terminated")
        return True

    def kill_evaluation_process() -> bool:
        if process.is_alive():
            # check if all evaluation runs are terminated
            status = get_run_ids_status(bulk_test_run_ids)
            if all([Status.is_terminated(s) for s in status.values()]):
                # TODO(2423785): terminate the process gracefully
                process.kill()
                logger.info("Successfully terminated process with pid %s", process.pid)
                return True
            else:
                logger.info("Not all variants reached terminated status: %s", status)
                return False
        else:
            logger.info("Process already canceled for evaluation process %s", process.pid)
            return True

    # add timeout & retry to avoid request stuck issue
    @retry(TimeoutError, tries=3)
    @timeout(timeout_seconds=MONITOR_REQUEST_TIMEOUT)
    def get_storage_from_config_with_retry():
        return get_storage_from_config(
            config,
            token=token,
            azure_storage_setting=request.azure_storage_setting,
            run_mode=request.run_mode.get_executor_run_mode() if request.run_mode is not None else None,
        )

    @retry(TimeoutError, tries=3)
    @timeout(timeout_seconds=MONITOR_REQUEST_TIMEOUT)
    def get_run_status_with_retry(storage, run_id):
        return storage.get_run_status(run_id=run_id)

    @retry(TimeoutError, tries=3)
    @timeout(timeout_seconds=MONITOR_REQUEST_TIMEOUT)
    def cancel_run_with_retry(storage, run_id):
        return storage.cancel_run(run_id=run_id)

    def monitor_run_status(
        flow_id: str,
        run_id: str,
        run_ids: List[str],
        terminate_process,
        context: contextvars.Context,
        log_path: str,
    ):
        try:
            storage = get_storage_from_config_with_retry()
            set_context(context)
            update_log_path(log_path, logger)
            logger.info("Start checking run status for run %s", run_id)
            while True:
                # keep monitoring to make sure long running process can be terminated
                time.sleep(STATUS_CHECKER_INTERVAL)

                run_status = get_run_status_with_retry(storage=storage, run_id=run_id)
                if run_status is None:
                    logger.info("Run %s not found, end execution monitoring", run_id)
                    return
                logger.info("Run %s is in progress, Execution status: %s", run_id, run_status)
                if run_status in [Status.Canceled.value, Status.CancelRequested.value]:
                    logger.info("Cancel requested for run %s", run_id)
                    try:
                        # terminate the process gracefully
                        terminated = terminate_process()
                        if not terminated:
                            continue
                        # mark the run as canceled
                        for child_run_id in run_ids:
                            logger.info("Updating status for run %s", child_run_id)
                            cancel_run_with_retry(storage=storage, run_id=child_run_id)
                            logger.info("Successfully canceled run %s", child_run_id)

                            logger.info("Updating child runs status for run %s", child_run_id)
                            storage.cancel_flow_child_runs(flow_id, child_run_id)
                            logger.info("Successfully canceled child runs for run %s", child_run_id)

                        logger.info("Successfully canceled run %s with child runs %s", run_id, run_ids)
                        return
                    except Exception as e:
                        logger.error("Failed to kill process for run %s due to %s", run_id, e, exc_info=True)
                        return
                elif Status.is_terminated(run_status):
                    logger.debug("Run %s is in terminate status %s", run_id, run_status)
                    return
        except Exception as e:
            logger.warning("Failed to monitor run status for run %s due to %s", run_id, e, exc_info=True)

    # monitor bulk test & evaluation
    if request.run_mode in [LegacyRunMode.BulkTest, LegacyRunMode.Eval]:
        # need to monitor variant run's parent run status, which stores in bulk_test_id
        flow_id = request.flow_id
        run_id = request.submission_data.bulk_test_id
        logger.info("Start checking run status for bulk run %s", run_id)
        # cancel the parent run(run_id) as well as all its child runs
        all_run_ids = FlowExecutionCoodinator.get_root_run_ids(req=request) + [run_id]
        thread = threading.Thread(
            name="monitor_bulk_run_status",
            target=monitor_run_status,
            kwargs={
                "flow_id": flow_id,
                "run_id": run_id,
                "run_ids": all_run_ids,
                "terminate_process": terminate_process,
                "context": contextvars.copy_context(),
                "log_path": request.run_id_to_log_path.get(request.flow_run_id) if request.run_id_to_log_path else None,
            },
            daemon=True,
        )
        thread.start()

    # monitor evaluation if bulk test has one
    if request.run_mode == LegacyRunMode.BulkTest and request.submission_data and request.submission_data.eval_flow:
        flow_id = request.flow_id
        run_id = request.submission_data.eval_flow_run_id
        logger.info("Start checking run status for evaluation run %s", run_id)
        thread = threading.Thread(
            name="monitor_evaluation_status",
            target=monitor_run_status,
            kwargs={
                "flow_id": flow_id,
                "run_id": run_id,
                "run_ids": [run_id],
                "terminate_process": kill_evaluation_process,
                "context": contextvars.copy_context(),
                "log_path": request.run_id_to_log_path.get(run_id) if request.run_id_to_log_path else None,
            },
            daemon=True,
        )
        thread.start()


def execute_request_multiprocessing_impl(
    config: RuntimeConfig,
    parent_pid: int,
    request: SubmitFlowRequest,
    return_dict,
    exception_queue,
    context_dict: Dict,
):
    """execute request in a child process.
    the child process should execute inside multi_processing_exception_wrapper to avoide exception issue.
    """
    operation_context = OperationContext.get_instance()
    operation_context.update(context_dict)
    with multi_processing_exception_wrapper(exception_queue):
        # set log context here;
        # otherwise the previously set context-local log handlers/filters will be lost
        # because this method is invoked in another process.
        with reset_and_close_logger(), get_log_context(request):
            logger.info("[%s--%s] Start processing flow......", parent_pid, os.getpid())
            result = execute_request(config, request)
            return_dict["result"] = result


def execute_request_multiprocessing(config: RuntimeConfig, request: SubmitFlowRequest):
    """execute request in a child process."""
    pid = os.getpid()

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    context_dict = OperationContext.get_instance().get_context_dict()
    exception_queue = multiprocessing.Queue()
    # TODO: change to support streaming output
    p = multiprocessing.Process(
        target=execute_request_multiprocessing_impl,
        args=(config, pid, request, return_dict, exception_queue, context_dict),
    )
    system_logger.info(f"{request.flow_run_id} Start execute request multiprocessing")
    p.start()
    logger.info("Starting to check process %s status", p.pid)
    start_thread_to_monitor_request_handler_process(
        config=config,
        request=request,
        process=p,
    )

    if request.run_mode in (LegacyRunMode.BulkTest, LegacyRunMode.Eval):
        p.join()
    else:
        p.join(timeout=SYNC_SUBMISSION_TIMEOUT)

        if p.is_alive():
            logger.error(f"[{p.pid}] Stop flow subprocess for exceeding {SYNC_SUBMISSION_TIMEOUT} seconds.")
            p.terminate()
            p.join()
            raise FlowRunTimeoutError(SYNC_SUBMISSION_TIMEOUT)
    logger.info("Process %s finished", p.pid)
    # when p is killed by signal, exitcode will be negative without exception
    if p.exitcode and p.exitcode > 0:
        exception = None
        try:
            exception = exception_queue.get(timeout=WAIT_SUBPROCESS_EXCEPTION_TIMEOUT)
        except Exception:
            pass
        # JsonSerializedPromptflowException will be raised here
        # no need to change to PromptflowException since it will be handled in app.handle_exception
        # we can unify the exception when we decide to expose executor.execute as an public API
        if exception is not None:
            raise exception
    result = return_dict.get("result", {})

    logger.info("[%s] Child process finished!", pid)
    return result
