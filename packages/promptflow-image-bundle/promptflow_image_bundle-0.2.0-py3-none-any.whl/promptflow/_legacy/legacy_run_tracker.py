import json
from datetime import datetime
from typing import List, Optional

from promptflow._internal import (
    ErrorResponse,
    RootErrorCode,
    RunRecordNotFound,
    RunTracker,
    flow_logger,
    logger,
    transpose,
)
from promptflow._legacy.contracts import LegacyRunMode
from promptflow.contracts.run_info import FlowRunInfo, RunInfo, Status
from promptflow.exceptions import ErrorTarget, ValidationException
from promptflow.runtime._errors import RunInfoNotFoundInStorageError
from promptflow.runtime.constants import TOTAL_CHILD_RUNS_KEY, PromptflowEdition


class LegacyRunTracker(RunTracker):
    """Keep some legacy logic here which are not open sourced."""

    @property
    def is_bulk_test(self):
        return self._run_mode == LegacyRunMode.BulkTest

    @property
    def should_upload_metrics(self):
        return self._run_mode in (LegacyRunMode.BulkTest, LegacyRunMode.Eval)

    @property
    def should_update_run_history(self):
        return (
            self._run_mode in (LegacyRunMode.BulkTest, LegacyRunMode.Eval)
            and self._storage._edition == PromptflowEdition.ENTERPRISE
        )

    def _get_root_flow_run_from_storage(self, flow_id, root_run_id):
        """Try get root flow run from storage, return None if not found"""
        try:
            # Get run info and create if not exist.
            run_info: FlowRunInfo = self._storage.get_flow_run(root_run_id, flow_id)
        except RunInfoNotFoundInStorageError:
            return None
        return run_info

    def start_root_flow_run(
        self,
        flow_id,
        root_run_id,
        run_id,
        parent_run_id,
        inputs=None,
    ) -> FlowRunInfo:
        """Initialize the root flow run since it can be pre-created to storage before executor receives it."""
        run_info = self._get_root_flow_run_from_storage(flow_id=flow_id, root_run_id=root_run_id)
        if run_info is None:
            flow_logger.info(
                f"Root flow run not found in run storage {type(self._storage).__qualname__!r},"
                f" will create a new root flow run. Run id: {root_run_id!r}, flow id: {flow_id!r}"
            )
            run_info = self.start_flow_run(
                flow_id=flow_id,
                run_id=run_id,
                root_run_id=root_run_id,
                parent_run_id=parent_run_id,
                inputs=inputs,
            )
        else:
            # Update status to started.
            run_info.start_time = datetime.utcnow()
            run_info.status = Status.Running
            if not run_info.parent_run_id:
                run_info.parent_run_id = parent_run_id

            self._storage.update_flow_run_info(run_info)
            flow_logger.info(
                f"Root flow run found in run storage {type(self._storage).__qualname__!r}. "
                f"Run id: {root_run_id!r}, flow id: {flow_id!r}."
            )

        # upload metrics is needed for only two run modes which are bulk test mode and evaluation mode,
        # and only for root flow runs.
        run_info.upload_metrics = self.should_upload_metrics
        self._flow_runs[root_run_id] = run_info
        self._current_run_id = root_run_id

        # start the root flow run that was created in azure machine learning workspace
        if self.should_update_run_history:
            self._storage._start_aml_root_run(run_id=run_id)

        return run_info

    def mark_notstarted_runs_as_failed(
        self, flow_id, root_run_ids, ex: Exception, need_update_run_history: bool = True
    ):
        """Handle run info update since root flow run can be created to storage before the executor receives
        the flow request
        """
        # No action needed for these two run modes
        if LegacyRunMode(self._run_mode) in (LegacyRunMode.SingleNode, LegacyRunMode.FromNode):
            return

        self._has_failed_root_run = True
        # for exceptions that raised before the flow is started, need to mark run failure and update the run info
        for root_run_id in root_run_ids:
            if root_run_id not in self._flow_runs:
                run_info = self._get_root_flow_run_from_storage(flow_id=flow_id, root_run_id=root_run_id)
                if run_info and run_info.status == Status.NotStarted:
                    self._flow_runs[root_run_id] = run_info
                    #  Make sure start_time is marked
                    run_info.start_time = run_info.start_time or datetime.utcnow()
                    self.end_run(run_id=root_run_id, ex=ex, update_at_last=True)
                    logger.info(f"Updated run {root_run_id!r} as failed in run info.")
                    # need to end the aml root runs for enterprise edition
                    if self.should_update_run_history and need_update_run_history:
                        self._storage._start_aml_root_run(run_id=root_run_id)
                        run_info.status = Status.Failed  # mark the status as Failed
                        self._storage._end_aml_root_run(run_info=run_info, ex=ex)
                        logger.info(f"Updated run {root_run_id!r} as failed in run history.")

    def mark_active_runs_as_failed_on_exit(self, root_run_ids, ex: Exception):
        """Mark active runs as failed on exit. This is useful to runtime shutdown gracefully."""
        # No action needed for these two run modes
        if LegacyRunMode(self._run_mode) in (LegacyRunMode.SingleNode, LegacyRunMode.FromNode):
            return

        logger.info("Updating active runs to failed on exit.")
        for root_run_id in root_run_ids:
            if root_run_id in self._flow_runs:
                run_info = self._flow_runs[root_run_id]
                if run_info.status == Status.Running:
                    run_info.status = Status.Failed
                    self.end_run(run_id=root_run_id, ex=ex, update_at_last=True)
                    logger.info(f"Updated run {root_run_id!r} as failed in run info.")
                    if self.should_update_run_history:
                        self._storage._end_aml_root_run(run_info=run_info, ex=ex)
                        logger.info(f"Updated run {root_run_id!r} as failed in run history.")

    def end_run(
        self,
        run_id: str,
        *,
        result: Optional[dict] = None,
        ex: Optional[Exception] = None,
        traces: Optional[List] = None,
        update_at_last: Optional[bool] = None,
    ):
        run_info = super().end_run(run_id, result=result, ex=ex, traces=traces)

        # this could be used to determine bulk test aml run status or for other usages
        # currently we mark bulk test run as completed anyway.
        if run_info.status == Status.Failed and isinstance(run_info, FlowRunInfo) and run_id == run_info.root_run_id:
            self._has_failed_root_run = True

        if update_at_last is True and isinstance(run_info, FlowRunInfo):
            self.update_flow_run_info(run_info)

    def end_bulk_test_aml_run(self, bulk_test_id):
        # set the bulk test run as current active run
        self._storage._start_aml_root_run(run_id=bulk_test_id)
        # end the bulk run with status "Completed" for current implementation
        status_str = Status.Completed.value
        self._storage._end_aml_bulk_test_run(bulk_test_id=bulk_test_id, bulk_test_status=status_str)
        logger.info(f"Updated bulk test run {bulk_test_id!r} as {status_str} in run history.")

    def collect_flow_runs(self, root_run_id: str) -> List[FlowRunInfo]:
        return [run_info for run_info in self.flow_run_list if run_info.root_run_id == root_run_id]

    def collect_child_flow_runs(self, parent_run_id: str) -> List[FlowRunInfo]:
        return [run_info for run_info in self.flow_run_list if run_info.parent_run_id == parent_run_id]

    def set_flow_metrics(self, run_id):
        run_info = self.ensure_run_info(run_id)
        if not isinstance(run_info, FlowRunInfo):
            return
        node_run_infos = self.collect_node_runs(run_id)
        run_info.system_metrics = run_info.system_metrics or {}
        run_info.system_metrics.update(self.collect_metrics(node_run_infos, self.OPENAI_AGGREGATE_METRICS))

        # log line data child run numbers for root flow run, note the run_id must be a root run id
        child_runs = self.collect_child_flow_runs(run_id)
        run_info.system_metrics[TOTAL_CHILD_RUNS_KEY] = len(child_runs)

    def _root_run_postprocess(self, run_info: FlowRunInfo):
        # For root level flow run, it is actually the parent of the flow runs of all lines of data
        # it needs to collect all metrics from all lines.
        self.set_flow_metrics(run_info.run_id)
        # root run should also aggregate child run errors to root run's error
        self._aggregate_child_run_errors(run_info)

    def _aggregate_child_run_errors(self, root_run_info: FlowRunInfo):
        """Aggregate child run errors to root run's error.

        (Example)
            Base flow run (variant_0)
                Child run 0 (line data 0) -> Succeeded
                Child run 1 (line data 1) -> Failed by UserError/SubUserError
                Child run 2 (line data 2) -> Failed by SystemError/SubSystemError

            Root run's error messageFormat would be a json string of a dict:
            {
                "totalChildRuns": 3,
                "userErrorChildRuns": 1,
                "systemErrorChildRuns": 1,
                "errorDetails": [
                    {
                        "code": "UserError/SubUserError",
                        "messageFormat": "Sample user error message",
                        "count": 1
                    },
                    {
                        "code": "SystemError/SubSystemError",
                        "messageFormat": "Sample system error message",
                        "count": 1
                    }
                ]
            }

            So the full error response of this root run would be like:
            {
                "error": {
                    "code": "SystemError/SubSystemError",
                    "message": "I don't like banana!",
                    "messageFormat": '{"totalChildRuns": 3, "userErrorChildRuns": 1, "systemErrorChildRuns": 1, "errorDetails": [{"code": "UserError/SubUserError", "message": "Sample user error message", "count": 1}, {"code": "SystemError/SubSystemError", "message": "Sample user error message", "count": 1}]}',                     "message": '{"totalChildRuns": 3, "userErrorChildRuns": 1, "systemErrorChildRuns": 1, "errorDetails": [{"code": "UserError/SubUserError", "message": "Sample user error message", "count": 1}, {"code": "SystemError/SubSystemError", "message": "Sample user error message", "count": 1}]}',   # noqa: E501
                }
                "componentName": "promptflow/{runtime_version}"
            }

            Note that the message_format is the message_format of the first system error child run, if no such child run it
            is the error message_format of the first user error child run.

            messageFormat is a json string of aggregated child run error info.
        """
        # get all child runs info
        child_runs = self.collect_child_flow_runs(parent_run_id=root_run_info.run_id)
        if not child_runs:
            return
        child_runs = sorted(child_runs, key=lambda run_info: run_info.run_id)

        # calculate the number of user error and system error child runs
        user_error_child_runs = [
            run_info for run_info in child_runs if run_info.error and run_info.error["code"] == RootErrorCode.USER_ERROR
        ]
        system_error_child_runs = [
            run_info
            for run_info in child_runs
            if run_info.error and run_info.error["code"] == RootErrorCode.SYSTEM_ERROR
        ]
        error_details = {}

        # set root run error dict as first system or user error child run's error dict
        if user_error_child_runs:
            root_run_info.error = user_error_child_runs[0].error
        if system_error_child_runs:
            root_run_info.error = system_error_child_runs[0].error

        # aggregate child runs' errors, update root run error message
        for run_info in child_runs:
            error = run_info.error
            if error is None:
                continue

            # use error code and error message as key to aggregate
            error_key = error["code"] + error.get("messageFormat", "")
            if error_key not in error_details:
                error_details[error_key] = {
                    "code": ErrorResponse(error).error_code_hierarchy,
                    "messageFormat": error.get("messageFormat", ""),
                    "count": 1,
                }
            else:
                error_details[error_key]["count"] += 1

        # update root run error message with aggregated error details
        if error_details:
            # there is a hard limitation for writing run history error message which is 3000 characters
            # so we use "messageFormat" to store the full error message, the limitation for "messageFormat"
            # is between 1.6 million and 3.2 million characters
            root_run_info.error["messageFormat"] = json.dumps(
                {
                    "totalChildRuns": len(child_runs),
                    "userErrorChildRuns": len(user_error_child_runs),
                    "systemErrorChildRuns": len(system_error_child_runs),
                    "errorDetails": self._validate_error_details(list(error_details.values())),
                }
            )

    def _validate_error_details(self, error_list):
        """
        Make sure error details json string size is less than 1.6 million characters. Truncate the error detail
        to not exceed the limit if needed.
        """
        MAX_JSON_STRING_SIZE = 1600000
        while len(json.dumps(error_list)) > MAX_JSON_STRING_SIZE:
            old_length = len(error_list)
            new_length = old_length // 2
            error_list = error_list[:new_length]
            logger.warning(
                f"Error details json string size exceeds limit {MAX_JSON_STRING_SIZE!r}, "
                f"truncated error details item count from {old_length!r} to {new_length!r}."
            )

        return error_list

    def start_root_run_in_storage_for_prs(
        self,
        flow_id: str,
        run_id: str,
    ):
        """Update status and start time in PromptFlow backend storage.
        For PRS usage only.

        Args:
            flow_id (str): FlowId in PromptFlow
            run_id (str): RunId of the batch run
        """
        run_info = self._get_root_flow_run_from_storage(flow_id, run_id)
        if run_info is None:
            raise RunRecordNotFound(
                message=f"Record with flow_id: {flow_id}, run_id: {run_id} is not found",
                target=ErrorTarget.RUN_TRACKER,
            )

        # Update status to started.
        run_info.start_time = datetime.utcnow()
        run_info.status = Status.Running

        self._storage.update_flow_run_info(run_info)

    def update_root_run_result_in_storage_for_prs(
        self,
        flow_id: str,
        run_id: str,
        results: Optional[list],
        ex: Optional[Exception] = None,
    ):
        """Update bulk test output and metric or exception to root run.
        For PRS usage only.

        Args:
            flow_id (str): FlowId in PromptFlow
            run_id (str): RunId of the batch run
            results (list): list of single line flow result, each element is a dict containing key "flow_results".
            ex (Exception): Exception object if the PRS run failed due to initialization failure or other system error.
        """
        run_info = self._get_root_flow_run_from_storage(flow_id, run_id)
        # Put run info into memory to pass the validation in post process functions.
        self._flow_runs[run_id] = run_info
        if run_info is None:
            raise RunRecordNotFound(
                message=f"Record with flow_id: {flow_id}, run_id: {run_id} is not found",
                target=ErrorTarget.RUN_TRACKER,
            )

        if not results:
            batch_results = []
        else:
            # Get output keys from the first result.
            output_keys = results[0].get("flow_results", {}).keys()
            batch_results = transpose([result.get("flow_results", {}) for result in results], keys=output_keys)

        self._flow_run_postprocess(run_info, batch_results, ex)
        self.update_flow_run_info(run_info)

    def update_flow_run_info(self, run_info: FlowRunInfo):
        """This operation only updates the flow run info related fields."""
        self._storage.update_flow_run_info(run_info)

    def log_metric(self, run_id: str, key: str, val: float, variant_id: Optional[str] = None):
        run_info = self.ensure_run_info(run_id)
        if run_info.metrics is None:
            run_info.metrics = {}
        if key not in run_info.metrics:
            run_info.metrics[key] = []
        item = {"value": val}
        if variant_id is not None:
            item["variant_id"] = variant_id
        run_info.metrics[key].append(item)


def log_metric(key, value, variant_id=None):
    run_tracker = LegacyRunTracker.active_instance()
    run_id = run_tracker.get_current_run_in_context() if run_tracker else None
    if not run_id:
        logger.warning(f"Cannot log metric {key}={value} because no run is active")
        return
    run_info = run_tracker.get_run(run_id)
    if not isinstance(run_info, RunInfo):
        logger.warning(f"Cannot log metric {key}={value} because run {run_id} is not a node run")
        return
    flow_run_info = run_tracker.get_run(run_info.parent_run_id)
    if not isinstance(flow_run_info, FlowRunInfo):
        parent_run_id = run_info.parent_run_id
        logger.warning(f"Cannot log metric {key}={value} because {run_id}'s parent {parent_run_id} is not a flow run")
        return
    if flow_run_info.root_run_id != flow_run_info.run_id:
        msg = f"Only aggregation node can log metrics. Please make sure '{run_info.node}' is an aggregation node."
        raise NodeTypeNotsupportedForLoggingMetric(message=msg, target=ErrorTarget.TOOL)
    if variant_id and not isinstance(variant_id, str):
        messgae = f"variant_id must be a string, got {variant_id} of type {type(variant_id)}"
        raise VariantIdTypeError(message=messgae, target=ErrorTarget.TOOL)
    try:
        value = float(value)
    except (TypeError, ValueError) as e:
        logger.warning(
            f"Cannot log metric because the value is not a number. Metric {key}={value} of type {type(value)}"
        )
        logger.warning(str(e))
        #  Currently this is just for backward compatibility. We should remove this in the future.
        return
    run_tracker.log_metric(flow_run_info.run_id, key, value, variant_id=variant_id)


class NodeTypeNotsupportedForLoggingMetric(ValidationException):
    pass


class VariantIdTypeError(ValidationException):
    pass
