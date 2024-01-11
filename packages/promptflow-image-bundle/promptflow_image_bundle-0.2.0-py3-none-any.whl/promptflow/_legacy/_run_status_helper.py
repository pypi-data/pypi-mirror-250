import json
from typing import List

from promptflow._internal import ErrorResponse, ExceptionPresenter
from promptflow._legacy.contracts import LegacyRunMode
from promptflow._legacy.legacy_run_tracker import LegacyRunTracker
from promptflow.contracts.run_info import Status
from promptflow.runtime.contracts.runtime import SubmitFlowRequest
from promptflow.runtime.runtime_config import RuntimeConfig
from promptflow.runtime.utils import logger
from promptflow.runtime.utils._contract_util import normalize_dict_keys_camel_to_snake
from promptflow.runtime.utils._utils import get_storage_from_config


def mark_runs_as_failed_in_runhistory(
    config: RuntimeConfig, flow_request: SubmitFlowRequest, payload: dict, ex: Exception
):
    if not flow_request:
        payload = normalize_dict_keys_camel_to_snake(payload)
    run_mode = flow_request.run_mode if flow_request else LegacyRunMode(payload.get("run_mode", 0))
    _, root_run_ids, bulk_test_id = _get_run_ids(flow_request, payload)
    _mark_runs_as_failed_in_runhistory(config, run_mode, root_run_ids, bulk_test_id, ex)


def mark_runs_as_failed_in_storage_and_runhistory(
    config: RuntimeConfig, flow_request: SubmitFlowRequest, payload: dict, ex: Exception
):
    if not flow_request:
        payload = normalize_dict_keys_camel_to_snake(payload)
    flow_id, root_run_ids, bulk_test_id = _get_run_ids(flow_request, payload)
    run_mode = flow_request.run_mode if flow_request else LegacyRunMode(payload.get("run_mode", 0))

    try:
        _mark_run_as_failed_in_storage(config, run_mode, flow_id, root_run_ids, ex)
    except Exception as exception:
        logger.warning(
            "Hit exception when mark flow runs as failed in storage: \n%s",
            ExceptionPresenter.create(exception).to_dict(),
        )

    _mark_runs_as_failed_in_runhistory(config, run_mode, root_run_ids, bulk_test_id, ex)


def _mark_run_as_failed_in_storage(
    config: RuntimeConfig, run_mode: LegacyRunMode, flow_id: str, root_run_ids: List[str], ex: Exception
):
    storage = get_storage_from_config(config)
    run_tracker = LegacyRunTracker(storage)

    run_tracker._run_mode = run_mode
    run_tracker.mark_notstarted_runs_as_failed(flow_id, root_run_ids, ex, need_update_run_history=False)


def _mark_runs_as_failed_in_runhistory(
    config: RuntimeConfig, run_mode: LegacyRunMode, root_run_ids: List[str], bulk_test_id: str, ex: Exception
):
    if (run_mode in (LegacyRunMode.BulkTest, LegacyRunMode.Eval)) and config.storage.storage_account:
        from promptflow._legacy.azureml_run_storage import MlflowHelper

        mlflow_tracking_uri = config.set_mlflow_tracking_uri()
        mlflow_helper = MlflowHelper(mlflow_tracking_uri=mlflow_tracking_uri)

        for run_id in root_run_ids:
            try:
                logger.info(f"Start to update run {run_id} status to Failed.")
                mlflow_helper.start_run(run_id)
                mlflow_run = mlflow_helper.get_run(run_id=run_id)
                error_response = ErrorResponse.from_exception(ex).to_dict()
                mlflow_helper.write_error_message(mlflow_run=mlflow_run, error_response=error_response)
                mlflow_helper.end_run(run_id, Status.Failed.value)
                logger.info(f"End to update run {run_id} status to Failed.")
            except Exception as exception:
                logger.warning(
                    "Hit exception when update run %s status to Failed in run history, exception: %s",
                    run_id,
                    exception,
                )

        # TODO: revisit this logic when have a final decision about bulk test run
        if run_mode == LegacyRunMode.BulkTest and bulk_test_id:
            logger.info(f"Start to update bulk_test_run {bulk_test_id} status to Completed in run history.")
            mlflow_helper.start_run(bulk_test_id)
            mlflow_helper.end_run(bulk_test_id, Status.Completed.value)
            logger.info(f"End to update bulk_test_run {bulk_test_id} status to Completed in run history.")


def _get_run_ids(flow_request: SubmitFlowRequest, payload: dict):
    flow_id = None
    root_run_ids = None
    bulk_test_id = None
    if flow_request:
        logger.info("Flow request is None.")
        flow_id = flow_request.flow_id
        root_run_ids = flow_request.get_root_run_ids()
        if flow_request.run_mode == LegacyRunMode.BulkTest:
            bulk_test_id = flow_request.submission_data.bulk_test_id
    else:
        # Try to get all the run ids directly from payload
        flow_id = payload.get("flow_id", "")
        flow_run_id = payload.get("flow_run_id", "")
        root_run_ids = [flow_run_id]
        run_mode = LegacyRunMode(payload.get("run_mode", 0))
        if run_mode == LegacyRunMode.Flow or run_mode == LegacyRunMode.BulkTest:
            submission_data = payload.get("submission_data", {})
            if isinstance(submission_data, str):
                # submission data is a json string
                submission_data = json.loads(submission_data)

            if isinstance(submission_data, dict):
                variants_runs = submission_data.get("variants_runs", {})
                if variants_runs:
                    root_run_ids += list(variants_runs.values())

                eval_flow_run_id = submission_data.get("eval_flow_run_id", None)
                if eval_flow_run_id:
                    root_run_ids.append(eval_flow_run_id)

                bulk_test_id = submission_data.get("bulk_test_id", None)

    return flow_id, root_run_ids, bulk_test_id
