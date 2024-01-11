from typing import List, Optional

from promptflow._internal import RunTracker, add_metric_logger, flow_logger, logger
from promptflow.batch._result import BatchResult
from promptflow.contracts.run_info import FlowRunInfo, RunInfo, Status
from promptflow.contracts.run_mode import RunMode
from promptflow.exceptions import ErrorTarget, ValidationException
from promptflow.runtime.constants import TOTAL_CHILD_RUNS_KEY, PromptflowEdition
from promptflow.runtime.utils._run_history_client import RunHistoryClient
from promptflow.runtime.utils.mlflow_helper import MlflowHelper, generate_error_dict_for_root_run
from promptflow.runtime.utils.timer import Timer


class RunTrackerAdapter:
    """RunTrackerAdapter wraps core RunTracker and AzureMLRunStorageV2
    to update flow run status and metrics to run history.
    It's to replace the LegacyRunTracker.
    """

    def __init__(
        self,
        run_tracker: RunTracker,
        mlflow_helper: MlflowHelper,
        run_history_client: RunHistoryClient,
        run_mode: RunMode,
    ):
        self._run_tracker = run_tracker
        self._storage = run_tracker._storage
        self._run_mode = run_mode
        self._mlflow_helper = mlflow_helper
        self._run_history_client = run_history_client
        # register metric logger
        add_metric_logger(self.log_metric)

    def _is_bulk_test(self):
        return self._run_mode == RunMode.Batch

    def _should_upload_metrics(self):
        return self._run_mode == RunMode.Batch

    def _should_update_run_history(self):
        return self._run_mode == RunMode.Batch and self._storage._edition == PromptflowEdition.ENTERPRISE

    def start_root_flow_run(self, flow_id, root_run_id):
        root_run_info = self._run_tracker.start_flow_run(
            flow_id=flow_id,
            run_id=root_run_id,
            root_run_id=root_run_id,
            parent_run_id="",
        )

        if self._should_upload_metrics():
            root_run_info.upload_metrics = True

        if self._should_update_run_history():
            self._mlflow_helper.start_run(run_id=root_run_id, create_if_not_exist=True)

        return root_run_info

    def end_root_flow_run(
        self,
        run_id: str,
        *,
        result: Optional[dict] = None,
        ex: Optional[Exception] = None,
    ):
        self._run_tracker.end_run(run_id=run_id, result=result, ex=ex)

    def update_flow_run_info(self, run_info: FlowRunInfo, log_patterns: List[str] = None):
        if not Status.is_terminated(run_info.status):
            logger.info("Flow run is not terminated, skip persisting flow run record.")
            return

        timer_message = "Persist root run info for run " + run_info.run_id

        if self._is_root_run(run_info):
            with Timer(flow_logger, timer_message):
                self._mlflow_helper.upload_metrics_to_run_history(run_info.run_id, run_info.metrics)
                self._mlflow_helper.update_run_history_properties_from_run_info(run_info)
                output_asset_infos = self._storage.update_flow_run_info(run_info)
                if output_asset_infos is not None:
                    self._run_history_client.patch_run(run_info.root_run_id, output_asset_infos)

                # end the root flow run that was created in azure machine learning workspace
                self._mlflow_helper._end_aml_root_run(run_info=run_info, log_patterns=log_patterns)
        else:
            self._storage.persist_flow_run(run_info)

    def _is_root_run(self, run_info: FlowRunInfo) -> bool:
        return run_info.run_id == run_info.root_run_id

    def persist_status_summary(self, status_summary: dict, run_id: str):
        self._mlflow_helper.persist_status_summary(status_summary, run_id)

    def root_run_postprocess(self, run_info: FlowRunInfo, batch_result: BatchResult):
        # For root level flow run, it is actually the parent of the flow runs of all lines of data,
        # it needs to collect all metrics from all lines.
        self._set_flow_metrics(run_info.run_id)
        # Root run should also aggregate child run errors to root run's error
        if run_info.error is None:
            self._aggregate_child_run_errors(run_info, batch_result)

    def _set_flow_metrics(self, run_id):
        run_info = self._run_tracker.ensure_run_info(run_id)
        if not isinstance(run_info, FlowRunInfo):
            return

        node_run_infos = self._run_tracker.collect_node_runs(run_id)
        run_info.system_metrics = run_info.system_metrics or {}
        run_info.system_metrics.update(
            self._run_tracker.collect_metrics(node_run_infos, RunTracker.OPENAI_AGGREGATE_METRICS)
        )

        child_runs_count = len(
            [run_info for run_info in self._run_tracker.flow_run_list if run_info.parent_run_id == run_id]
        )
        run_info.system_metrics[TOTAL_CHILD_RUNS_KEY] = child_runs_count

    def _aggregate_child_run_errors(self, root_run_info: FlowRunInfo, batch_result: BatchResult):
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
        child_runs = [
            run_info for run_info in self._run_tracker.flow_run_list if run_info.parent_run_id == root_run_info.run_id
        ]
        if not child_runs:
            return
        child_runs = sorted(child_runs, key=lambda run_info: run_info.run_id)
        error_list = [r.error for r in child_runs if r.error]
        root_run_error = generate_error_dict_for_root_run(error_list, len(child_runs))
        if len(root_run_error) == 0:
            # If no error in child runs, but error in aggregation node runs, use the first error as root run's error.
            # Use getattr to avoid error
            # when batch_result.error_summary does not have "aggr_error_dict" attribute (for promptflow<1.3.0).
            # TODO: Remove getattr after promptflow<1.3.0 is not used in cloud anymore.
            if (
                batch_result
                and batch_result.error_summary
                and getattr(batch_result.error_summary, "aggr_error_dict", None)
            ):
                root_run_info.error = next(iter(batch_result.error_summary.aggr_error_dict.values()))
        else:
            root_run_info.error = root_run_error

    def log_metric(self, key, value, variant_id=None):
        run_tracker_active = self._run_tracker.active()
        run_id = self._run_tracker.get_current_run_in_context()
        if not run_tracker_active or not run_id:
            logger.warning(f"Cannot log metric {key}={value} because no run is active")
            return
        run_info = self._run_tracker.get_run(run_id)
        if not isinstance(run_info, RunInfo):
            logger.warning(f"Cannot log metric {key}={value} because run {run_id} is not a node run")
            return
        flow_run_info = self._run_tracker.get_run(run_info.parent_run_id)
        if not isinstance(flow_run_info, FlowRunInfo):
            parent_run_id = run_info.parent_run_id
            logger.warning(
                f"Cannot log metric {key}={value} because {run_id}'s parent {parent_run_id} is not a flow run"
            )
            return
        if flow_run_info.root_run_id != flow_run_info.run_id:
            message = (
                f"Only aggregation node can log metrics. Please make sure '{run_info.node}' is an aggregation node."
            )
            raise NodeTypeNotSupportedForLoggingMetric(message=message, target=ErrorTarget.TOOL)
        if variant_id and not isinstance(variant_id, str):
            message = f"variant_id must be a string, got {variant_id} of type {type(variant_id)}"
            raise VariantIdTypeError(message=message, target=ErrorTarget.TOOL)
        try:
            value = float(value)
        except (TypeError, ValueError) as e:
            logger.warning(
                f"Cannot log metric because the value is not a number. Metric {key}={value} of type {type(value)}"
            )
            logger.warning(str(e))
            #  Currently this is just for backward compatibility. We should remove this in the future.
            return

        # Add metrics to run info
        if flow_run_info.metrics is None:
            flow_run_info.metrics = {}
        if key not in flow_run_info.metrics:
            flow_run_info.metrics[key] = []
        item = {"value": value}
        if variant_id is not None:
            item["variant_id"] = variant_id
        flow_run_info.metrics[key].append(item)


class NodeTypeNotSupportedForLoggingMetric(ValidationException):
    pass


class VariantIdTypeError(ValidationException):
    pass
