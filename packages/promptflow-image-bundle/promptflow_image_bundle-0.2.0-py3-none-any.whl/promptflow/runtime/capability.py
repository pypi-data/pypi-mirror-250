""" define runtime capability, which describes the features and apis supported by current runtime. """
from dataclasses import dataclass
from promptflow._internal import get_feature_list, FeatureState, Feature

RUNTIME = "runtime"  # runtime component name


@dataclass
class Api:
    """The dataclass to describe an api."""
    verb: str
    route: list
    version: str
    description: str

    def to_dict(self):
        return {
            "verb": self.verb,
            "route": self.route,
            "version": self.version,
            "description": self.description
        }


def get_runtime_api_list():
    # define current runtime api list.
    runtime_api_list = [
        Api(
            verb="GET",
            route=["/package_tools", "/aml-api/v1.0/package_tools"],
            version="1.0",
            description="Get tools supported by runtime."
        ),
        Api(
            verb="POST",
            route=["/submit_single_node", "/aml-api/v1.0/submit_single_node"],
            version="1.0",
            description="Submit single node to runtime."
        ),
        Api(
            verb="POST",
            route=["/submit_flow", "/aml-api/v1.0/submit_flow"],
            version="1.0",
            description="Submit flow to runtime."
        ),
        Api(
            verb="POST",
            route=["/submit_bulk_run", "/aml-api/v1.0/submit_bulk_run"],
            version="1.0",
            description="Submit bulk run to runtime."
        ),
        Api(
            verb="POST",
            route=["/score", "/aml-api/v1.0/score", "/submit", "/aml-api/v1.0/submit"],
            version="1.0",
            description="Submit single node, flow or bulk run to runtime (legacy)."
        ),
        Api(
            verb="POST",
            route=["/meta", "/aml-api/v1.0/meta"],
            version="1.0",
            description="Generate tool meta (deprecated)."
        ),
        Api(
            verb="POST",
            route=["/meta-v2", "/aml-api/v1.0/meta-v2/"],
            version="1.0",
            description="Generate tool meta-v2."
        ),
        Api(
            verb="GET",
            route=["/health", "/aml-api/v1.0/health"],
            version="1.0",
            description="Check if the runtime is alive."
        ),
        Api(
            verb="GET",
            route=["/version", "/aml-api/v1.0/version"],
            version="1.0",
            description="Check the runtime's version."
        ),
        Api(
            verb="POST",
            route=["/dynamic_list", "/aml-api/v1.0/dynamic_list"],
            version="1.0",
            description="Dynamically generates a list of items for a tool input."
        ),
        Api(
            verb="POST",
            route=["/retrieve_tool_func_result", "/aml-api/v1.0/retrieve_tool_func_result"],
            version="1.0",
            description="Retrieve generated result of a tool function."
        ),
    ]

    runtime_api_list = [runtime_api.to_dict() for runtime_api in runtime_api_list]
    return runtime_api_list


def get_runtime_feature_list():
    # define current runtime feature list.
    runtime_feature_list = [
        Feature(
            name="CSharpFlowBatchRun",
            description="c# flow batch run support",
            state=FeatureState.E2ETEST,
        ),
    ]
    return runtime_feature_list


def get_executor_feature_list():
    executor_feature_list = get_feature_list()
    return executor_feature_list


def get_merged_feature_list(runtime_feature_list, executor_feature_list):
    """ merge runtime feature list and executor feature list. """
    runtime_feature_dict = {runtime_feature.name: runtime_feature for runtime_feature in runtime_feature_list}
    merged_feature_list = []

    for executor_feature in executor_feature_list:
        executor_feature_name = executor_feature.name
        if executor_feature_name in runtime_feature_dict.keys():
            # for feature in both runtime and executor, merge them
            runtime_feature = runtime_feature_dict[executor_feature_name]
            merged_feature = get_merged_feature(runtime_feature.name,
                                                runtime_feature.description,
                                                {RUNTIME: runtime_feature.state.value,
                                                 executor_feature.component: executor_feature.state.value})
            merged_feature_list.append(merged_feature)
            runtime_feature_dict.pop(executor_feature_name, None)
        else:
            # for feature only in executor, add `Ready` state for runtime component
            merged_feature = get_merged_feature(executor_feature.name,
                                                executor_feature.description,
                                                {RUNTIME: FeatureState.READY.value,
                                                 executor_feature.component: executor_feature.state.value})
            merged_feature_list.append(merged_feature)

    if len(runtime_feature_dict) > 0:
        remaining_feature_list = [get_merged_feature(runtime_feature.name,
                                                     runtime_feature.description,
                                                     {RUNTIME: runtime_feature.state.value})
                                  for runtime_feature in runtime_feature_dict.values()]
        merged_feature_list = merged_feature_list + remaining_feature_list

    return merged_feature_list


def get_total_feature_list():
    """ get all current feature list that should be returned to pfs. """
    return get_merged_feature_list(get_runtime_feature_list(), get_executor_feature_list())


def get_merged_feature(name, description, state):
    return {
        "name": name,
        "description": description,
        "state": state
    }
