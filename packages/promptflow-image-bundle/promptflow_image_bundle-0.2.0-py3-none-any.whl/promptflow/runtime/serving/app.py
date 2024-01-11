# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import mimetypes
import os
import re
import time
from pathlib import Path

import flask
from flask import Flask, g, jsonify, request, url_for
from jinja2 import Template

from promptflow._internal import (
    VERSION,
    ErrorResponse,
    ResponseCreator,
    generate_swagger,
    get_output_fields_to_remove,
    get_sample_json,
    handle_error_to_response,
    load_json,
    load_request_data,
    setup_user_agent_to_operation_context,
    streaming_response_required,
    validate_request_data,
)
from promptflow.contracts.flow import Flow
from promptflow.contracts.run_info import Status
from promptflow.exceptions import ErrorTarget, SystemErrorException
from promptflow.runtime import PromptFlowRuntime
from promptflow.runtime._errors import FlowFileNotFound
from promptflow.runtime.constants import DEFAULT_FLOW_YAML_FILE, PromptflowEdition, RuntimeMode
from promptflow.runtime.serving.data_collector import FlowDataCollector
from promptflow.runtime.serving.flow_invoker import ConnectionLoadingType, FlowInvoker, FlowResult
from promptflow.runtime.serving.metrics import ResponseType
from promptflow.runtime.serving.metrics_az import AzureMetricsRecorder
from promptflow.runtime.serving.streaming_monitor import StreamingMonitor
from promptflow.runtime.serving.utils import enable_monitoring, get_cost_up_to_now
from promptflow.runtime.utils import log_runtime_pf_version, logger

# from flask_cors import CORS
USER_AGENT = f"promptflow-cloud-serving/{VERSION}"
AML_DEPLOYMENT_RESOURCE_ID_REGEX = "/subscriptions/(.*)/resourceGroups/(.*)/providers/Microsoft.MachineLearningServices/workspaces/(.*)/onlineEndpoints/(.*)/deployments/(.*)"  # noqa: E501


class PromptflowServingApp(Flask):
    def init(self, **kwargs):
        with self.app_context():
            self.logger.handlers = logger.handlers
            self.logger.setLevel(logger.level)
            # parse promptflow project path
            project_path: str = os.getenv("PROMPTFLOW_PROJECT_PATH", None)
            self.model_name = "default"
            if not project_path:
                model_dir = os.getenv("AZUREML_MODEL_DIR", ".")
                model_rootdir = os.listdir(model_dir)[0]
                self.model_name = model_rootdir
                project_path = os.path.join(model_dir, model_rootdir)
            self.project_path = project_path
            os.chdir(self.project_path)
            self.logger.info(f"Model path: {project_path}")
            # load swagger sample if exists
            self.sample = get_sample_json(self.project_path, logger)
            self.init_swagger()
            setup_user_agent_to_operation_context(USER_AGENT)

            connection_loading_type = ConnectionLoadingType.Environment
            # load runtime config and set the runtime_mode to serving
            # this AML_DEPLOYMENT_RESOURCE_ID will be automatically set by MIR for pf as mlflow flavor model.
            deploy_resource_id = os.getenv("AML_DEPLOYMENT_RESOURCE_ID", None)
            if deploy_resource_id:
                match_result = re.match(AML_DEPLOYMENT_RESOURCE_ID_REGEX, deploy_resource_id)
                if len(match_result.groups()) == 5:
                    config_override = (
                        f"deployment.subscription_id={match_result.group(1)}, "
                        f"deployment.resource_group={match_result.group(2)}, "
                        f"deployment.workspace_name={match_result.group(3)}, "
                        f"deployment.endpoint_name={match_result.group(4)}, "
                        f"deployment.deployment_name={match_result.group(5)}"
                    )
                    logger.info(f"Setting PRT_CONFIG_OVERRIDE_ENV to {config_override!r}..")
                    os.environ["PRT_CONFIG_OVERRIDE"] = config_override
                else:
                    logger.warn(f"Invalid AML_DEPLOYMENT_RESOURCE_ID: {deploy_resource_id}")
            self.runtime_config = PromptFlowRuntime.get_instance().config
            self.logger.info(f"Setting runtime_mode to {RuntimeMode.SERVING!r}..")

            self.runtime_config.deployment.runtime_mode = RuntimeMode.SERVING
            if self.runtime_config.deployment.subscription_id:
                # Set edition to enterprise if workspace is provided
                self.runtime_config.deployment.edition = PromptflowEdition.ENTERPRISE
                connection_loading_type = ConnectionLoadingType.Workspace
                # Add workspace info to environment variables, some tools may need these to initialize mlclient
                self.runtime_config._add_workspace_info_to_environ()

            self.data_collector = FlowDataCollector()
            self.flow_file = self.get_flow_file()

            # check application insights status
            app_insight_key = os.getenv("AML_APP_INSIGHTS_KEY") or os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")
            self.metric_recorder = None
            if app_insight_key:
                self.metric_recorder = AzureMetricsRecorder(app_insight_key, self.runtime_config)
                self.logger.info("App insight metrics enabled!")

            # init flow invoker and try load flow
            self.flow_invoker = FlowInvoker(
                self.flow_file,
                streaming_response_required,
                connection_loading_type,
                subscription_id=self.runtime_config.deployment.subscription_id,
                resource_group=self.runtime_config.deployment.resource_group,
                workspace_name=self.runtime_config.deployment.workspace_name,
            )
            self.enable_trace_logging = os.environ.get("PROMPTFLOW_TRACE_LOGGING_ENABLE", "false").lower() == "true"

            # ensure response has the correct content type
            mimetypes.add_type("application/javascript", ".js")
            mimetypes.add_type("text/css", ".css")

    def get_flow_file(self):
        """Get flow file from project folder."""
        project_path = Path(self.project_path)
        if (project_path / DEFAULT_FLOW_YAML_FILE).exists():
            flow_file = project_path / DEFAULT_FLOW_YAML_FILE
        elif (project_path / "flow.json").exists():
            # For backward compatibility to support json flow file, will be deprecated
            flow_file = project_path / "flow.json"
        else:
            raise FlowFileNotFound(f"Cannot find flow file in {self.project_path}", target=ErrorTarget.SERVING_APP)
        return flow_file

    def init_swagger(self):
        flow_file = self.get_flow_file()
        if flow_file.suffix == ".json":
            flow = Flow.deserialize(load_json(flow_file))
        else:
            flow = Flow.from_yaml(flow_file)
        self.response_fields_to_remove = get_output_fields_to_remove(flow, logger)
        self.swagger = generate_swagger(flow, self.sample, self.response_fields_to_remove)


app = PromptflowServingApp(__name__)
# CORS(app)


if __name__ != "__main__":
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)


def is_monitoring_enabled() -> bool:
    enabled = False
    if request.endpoint in app.view_functions:
        view_func = app.view_functions[request.endpoint]
        enabled = hasattr(view_func, "_enable_monitoring")
    return enabled


@app.errorhandler(Exception)
def handle_error(e):
    err_resp, resp_code = handle_error_to_response(e, logger)
    if app.metric_recorder:
        flow_id = g.get("flow_id", app.model_name)
        err_code = ErrorResponse.from_exception(e).innermost_error_code
        app.metric_recorder.record_flow_request(flow_id, resp_code, err_code, g.streaming)
    return err_resp, resp_code


@app.before_request
def start_monitoring():
    if not is_monitoring_enabled():
        return
    g.start_time = time.time()
    g.streaming = streaming_response_required()
    g.req_id = request.headers.get("x-request-id", None)
    g.client_req_id = request.headers.get("x-ms-client-request-id", None)
    logger.info(f"Start monitoring new request, request_id: {g.req_id}, client_request_id: {g.client_req_id}.")


@app.after_request
def finish_monitoring(response):
    """record mdc logs and metrics."""
    if not is_monitoring_enabled():
        return response
    data = g.get("data", None)
    flow_result: FlowResult = g.get("flow_result", None)
    req_id = g.get("req_id", None)
    client_req_id = g.get("client_req_id", None)
    flow_id = g.get("flow_id", app.model_name)
    # collect non-streaming flow request/response data
    if data and flow_result and flow_result.output and not g.streaming:
        app.data_collector.collect_flow_data(data, flow_result.output, req_id, client_req_id)

    if app.metric_recorder:
        if flow_result:
            app.metric_recorder.record_tracing_metrics(flow_result.run_info, flow_result.node_run_infos)
        err_code = g.get("err_code", "None")
        app.metric_recorder.record_flow_request(flow_id, response.status_code, err_code, g.streaming)
        # streaming metrics will be recorded in the streaming callback func
        if not g.streaming:
            latency = get_cost_up_to_now(g.start_time)
            app.metric_recorder.record_flow_latency(
                flow_id, response.status_code, g.streaming, ResponseType.Default.value, latency
            )

    logger.info(f"Finish monitoring request, request_id: {req_id}, client_request_id: {client_req_id}.")
    return response


@app.route("/score", methods=["POST"])
@enable_monitoring
def score():
    """process a flow request in the runtime."""
    raw_data = request.get_data()
    logger.debug(f"PromptFlow executor received data: {raw_data}")
    log_runtime_pf_version(logger)
    flow = app.flow_invoker.flow
    if flow.inputs.keys().__len__() == 0:
        data = {}
        logger.info(f"Flow has no input, request data '{raw_data}' will be ignored.")
    else:
        logger.info("Start loading request data...")
        data = load_request_data(flow, raw_data, logger)
    g.data = data
    g.flow_id = flow.id
    logger.debug(f"Validating flow input with data {data!r}")
    validate_request_data(flow, data)
    logger.info("Start executing flow with data...")

    # update opeartion context before execution
    runtime = PromptFlowRuntime.get_instance()
    runtime.update_operation_context(request)
    run_id = g.client_req_id or g.req_id
    flow_result = app.flow_invoker.invoke(data, run_id=run_id, allow_generator_output=g.streaming)
    g.flow_result = flow_result
    # add trace logging support for debugging
    if flow_result and app.enable_trace_logging:
        logger.info(f"Flow execution result: {flow_result}")
    # check flow result, if failed, return error response
    if flow_result.run_info.status != Status.Completed:
        if flow_result.run_info.error:
            err = ErrorResponse(flow_result.run_info.error)
            g.err_code = err.innermost_error_code
            return jsonify(err.to_simplified_dict()), err.response_code
        else:
            # in case of run failed but can't find any error, return 500
            exception = SystemErrorException("Flow execution failed without error message.")
            return jsonify(ErrorResponse.from_exception(exception).to_simplified_dict()), 500

    result = flow_result.output or {}
    # remove evaluation only fields
    result = {k: v for k, v in result.items() if k not in app.response_fields_to_remove}
    response_creator = ResponseCreator(
        flow_run_result=result,
        accept_mimetypes=request.accept_mimetypes,
    )
    g.streaming = response_creator.has_stream_field and response_creator.text_stream_specified_explicitly
    # set streaming callback functions if the response is streaming
    if g.streaming:
        streaming_monitor = StreamingMonitor(
            flow_id=flow.id,
            start_time=g.start_time,
            inputs=data,
            outputs=flow_result.output,
            req_id=g.req_id,
            streaming_field_name=response_creator.stream_field_name,
            metric_recorder=app.metric_recorder,
            data_collector=app.data_collector,
        )
        response_creator._on_stream_start = streaming_monitor.on_stream_start
        response_creator._on_stream_end = streaming_monitor.on_stream_end
        response_creator._on_stream_event = streaming_monitor.on_stream_event

    response = response_creator.create_response()
    return response


@app.route("/swagger.json", methods=["GET"])
def swagger():
    """Get the swagger object."""
    return jsonify(app.swagger)


@app.route("/health", methods=["GET"])
def health():
    """Check if the runtime is alive."""
    return {"status": "Healthy", "version": VERSION}


@app.route("/version", methods=["GET"])
def version():
    """Check the runtime's version."""
    build_info = os.environ.get("BUILD_INFO", "")
    try:
        build_info_dict = json.loads(build_info)
        version = build_info_dict["build_number"]
    except Exception:
        version = VERSION
    return {"status": "Healthy", "build_info": build_info, "version": version}


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def home(path):
    """Show the home page."""
    rules = {rule.rule: rule.methods for rule in app.url_map.iter_rules()}
    if request.path not in rules or request.method not in rules[request.path]:
        unsupported_message = (
            f"The requested api {request.path!r} with {request.method} is not supported by current app, "
            f"if you entered the URL manually please check your spelling and try again."
        )
        return unsupported_message, 404
    index_path = Path("index.html")
    if index_path.exists():
        template = Template(open(index_path, "r", encoding="UTF-8").read())
        return flask.render_template(template, url_for=url_for)
    else:
        return "<h1>Welcome to promptflow app.</h1>"


def create_app(**kwargs):
    try:
        app.init(**kwargs)
    except Exception as e:
        log_runtime_pf_version(logger)
        logger.error("An error occurred when init app: %s", e)
        raise

    return app


if __name__ == "__main__":
    create_app().run()
