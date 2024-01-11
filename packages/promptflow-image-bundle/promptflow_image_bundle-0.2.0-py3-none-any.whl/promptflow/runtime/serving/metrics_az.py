# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
    MetricReader)

from promptflow.runtime.serving.metrics import MetricsRecorder
from promptflow.runtime import RuntimeConfig

ENDPOINT_KEY = "endpoint"
DEPLOYMENT_KEY = "deployment"


class AzureMetricsRecorder(MetricsRecorder):
    def __init__(self, instrumentation_key: str, runtime_config: RuntimeConfig, export_interval_millis: int = 60000):
        common_dimensions = {}
        if runtime_config and runtime_config.deployment.endpoint_name:
            common_dimensions[ENDPOINT_KEY] = runtime_config.deployment.endpoint_name
        if runtime_config and runtime_config.deployment.deployment_name:
            common_dimensions[DEPLOYMENT_KEY] = runtime_config.deployment.deployment_name
        metric_reader: MetricReader = None
        if instrumentation_key:
            metric_exporter = AzureMonitorMetricExporter(connection_string=f"InstrumentationKey={instrumentation_key}")
            metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis)
        super().__init__(metric_reader, common_dimensions)
