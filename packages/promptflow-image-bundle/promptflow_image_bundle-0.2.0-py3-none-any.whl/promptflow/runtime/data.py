""" download or mount remote data in runtime """
import os
import re
import shutil
from contextlib import AbstractContextManager
from pathlib import Path

import requests
from azure.ai.ml.exceptions import ErrorCategory, MlException
from azure.core.exceptions import HttpResponseError, ServiceResponseError
from azureml.exceptions import UserErrorException as AzureMLUserErrorException

from promptflow.exceptions import ErrorTarget, PromptflowException, SystemErrorException, UserErrorException
from promptflow.runtime.utils import logger
from promptflow.runtime.utils.retry_utils import retry

from ._errors import (
    InvalidAmlDataUri,
    InvalidBlobDataUri,
    InvalidDataUri,
    InvalidWasbsDataUri,
    RuntimeConfigNotProvided,
)
from .runtime_config import RuntimeConfig


class DownloadDataUserError(UserErrorException):
    def __init__(self, message):
        super().__init__(message, target=ErrorTarget.RUNTIME)


class DownloadDataSystemError(SystemErrorException):
    def __init__(self, message):
        super().__init__(message, target=ErrorTarget.RUNTIME)


SHORT_DATASTORE_URI_REGEX_FORMAT = "azureml://datastores/([^/]+)/paths/(.+)"
LONG_DATASTORE_URI_REGEX_FORMAT = (
    "azureml://subscriptions/([^/]+)/resource[gG]roups/([^/]+)/workspaces/([^/]+)/datastores/([^/]+)/paths/(.+)"
)
JOB_URI_REGEX_FORMAT = "azureml://jobs/([^/]+)/outputs/([^/]+)/paths/(.+)"

DATA_ASSET_ID_REGEX_FORMAT = (
    "azureml://subscriptions/([^/]+)/resource[gG]roups/([^/]+)/workspaces/([^/]+)/data/([^/]+)/versions/(.+)"
)
DATA_ASSET_ID_LABEL_REGEX_FORMAT = (
    "azureml://subscriptions/([^/]+)/resource[gG]roups/([^/]+)/workspaces/([^/]+)/data/([^/]+)/labels/(.+)"
)
ASSET_ARM_ID_REGEX_FORMAT = (
    "azureml:/subscriptions/([^/]+)/resource[gG]roups/([^/]+)/"
    "providers/Microsoft.MachineLearningServices/workspaces/([^/]+)/([^/]+)/([^/]+)/versions/(.+)"
)
AZUREML_VERSION_REGEX_FORMAT = "azureml:([^/]+):(.+)"
AZUREML_LABEL_REGEX_FORMAT = "azureml:([^/]+)@(.+)"


def _get_last_part_of_uri(uri: str) -> str:
    """get last part of uri"""
    return uri.split("/")[-1]


WASBS_REGEX_FORMAT = "wasbs://([^@]+)@([^/]+)/(.+)"


def _wasbs_to_http_url(wasbs_url: str) -> str:
    """convert wasbs url to http url"""
    if not wasbs_url.startswith("wasbs"):
        return wasbs_url

    m = re.match(WASBS_REGEX_FORMAT, wasbs_url)
    if m is None:
        raise InvalidWasbsDataUri(message_format="Invalid wasbs data url: {wasbs_url}", wasbs_url=wasbs_url)

    container, account, path = m.groups()
    return f"https://{account}/{container}/{path}"


BLOB_HTTP_REGEX_FORMAT = "https://([^/]+)/([^/]+)/(.+)"


def _http_to_wasbs_url(url: str) -> str:
    """convert http url to wasbs url"""

    m = re.match(BLOB_HTTP_REGEX_FORMAT, url)
    if m is None:
        raise InvalidBlobDataUri(message_format="Invalid blob data url: {blob_url}", blob_url=url)

    account, container, path = m.groups()
    return f"wasbs://{container}@{account}/{path}"


def _download_blob(uri, destination, credential) -> str:
    uri = _wasbs_to_http_url(uri)
    target_file = _get_last_part_of_uri(uri)
    if destination is not None:
        target_file = os.path.join(destination, target_file)

    from azure.storage.blob import BlobClient

    blob_client = BlobClient.from_blob_url(blob_url=uri, credential=credential)
    with open(target_file, "wb") as my_blob:
        blob_data = blob_client.download_blob()
        blob_data.readinto(my_blob)

    return target_file


def _download_blob_directory(uri, destination, credential) -> str:
    from urllib.parse import urlparse, urlunparse

    from azure.ai.ml._restclient.v2022_10_01.models import DatastoreType
    from azure.ai.ml._utils._storage_utils import get_artifact_path_from_storage_url, get_storage_client

    m = re.match(BLOB_HTTP_REGEX_FORMAT, uri)
    if m is None:
        raise InvalidBlobDataUri(message_format="Invalid blob data url: {blob_url}", blob_url=uri)

    account, container, path = m.groups()
    parsed_url = urlparse(uri)

    account_url = "https://" + account
    if parsed_url.query:
        # Use sas token instead of credential when there is sas token query
        account_url += "?" + parsed_url.query
        new_url = parsed_url._replace(query="")
        uri = urlunparse(new_url)
        credential = None

    starts_with = get_artifact_path_from_storage_url(blob_url=str(uri), container_name=container)
    storage_client = get_storage_client(
        credential=credential,
        container_name=container,
        storage_account=account,
        account_url=account_url,
        storage_type=DatastoreType.AZURE_BLOB,
    )
    storage_client.download(starts_with=starts_with, destination=destination)
    return destination


def _download_public_http_url(url, destination) -> str:
    target_file = _get_last_part_of_uri(url)
    if destination is not None:
        target_file = os.path.join(destination, target_file)

    with requests.get(url, stream=True) as r:
        with open(target_file, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return target_file


def _download_aml_uri(uri, destination, credential, runtime_config: RuntimeConfig) -> str:  # noqa: C901
    uri = _get_aml_uri(uri, credential, runtime_config)

    from azure.ai.ml import MLClient
    from azure.ai.ml._artifacts._artifact_utilities import download_artifact_from_aml_uri

    if re.match(SHORT_DATASTORE_URI_REGEX_FORMAT, uri):
        ml_client = runtime_config.get_ml_client(credential)
        return download_artifact_from_aml_uri(uri, destination, ml_client.datastores)
    elif re.match(LONG_DATASTORE_URI_REGEX_FORMAT, uri):
        sub, rg, ws, _, _ = re.match(LONG_DATASTORE_URI_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, subscription_id=sub, resource_group_name=rg, workspace_name=ws)
        # download all files in the datastore starts with the url
        return download_artifact_from_aml_uri(uri, destination, ml_client.datastores)
    else:
        raise InvalidAmlDataUri(message_format="Invalid aml data uri: {aml_uri}", aml_uri=uri)


def _get_aml_uri(uri, credential, runtime_config: RuntimeConfig) -> str:
    if not runtime_config and not (uri.startswith("azureml://") or uri.startswith("azureml:/subscriptions/")):
        raise RuntimeConfigNotProvided(message_format="Runtime_config must be provided for short form uri")
    # hide imports not for community version
    from azure.ai.ml import MLClient
    from azure.ai.ml.entities import Data

    # asset URI: resolve as datastore uri
    data: Data = None
    if re.match(ASSET_ARM_ID_REGEX_FORMAT, uri):
        sub, rg, ws, _, name, version = re.match(ASSET_ARM_ID_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, subscription_id=sub, resource_group_name=rg, workspace_name=ws)
        data = ml_client.data.get(name, version=version)
    elif re.match(AZUREML_VERSION_REGEX_FORMAT, uri):
        name, version = re.match(AZUREML_VERSION_REGEX_FORMAT, uri).groups()
        ml_client = runtime_config.get_ml_client(credential)
        data = ml_client.data.get(name, version=version)
    elif re.match(AZUREML_LABEL_REGEX_FORMAT, uri):
        name, label = re.match(AZUREML_LABEL_REGEX_FORMAT, uri).groups()
        ml_client = runtime_config.get_ml_client(credential)
        data = ml_client.data.get(name, label=label)
    elif re.match(DATA_ASSET_ID_REGEX_FORMAT, uri):
        # asset URI: long versions
        sub, rg, ws, name, version = re.match(DATA_ASSET_ID_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, subscription_id=sub, resource_group_name=rg, workspace_name=ws)
        data = ml_client.data.get(name, version=version)
    elif re.match(DATA_ASSET_ID_LABEL_REGEX_FORMAT, uri):
        sub, rg, ws, name, label = re.match(DATA_ASSET_ID_LABEL_REGEX_FORMAT, uri).groups()
        ml_client = MLClient(credential=credential, subscription_id=sub, resource_group_name=rg, workspace_name=ws)
        data = ml_client.data.get(name, label=label)

    if data:
        uri = str(data.path)

    # remove trailing slash all the time: it will break download file, and no slash won't break folder
    uri = uri.rstrip("/")
    # we have observed glob like uri including "**/" that will break download;
    # as we remove slash above, only check & remove "**" here.
    if uri.endswith("**"):
        uri = uri[:-2]

    # datastore uri
    if re.match(SHORT_DATASTORE_URI_REGEX_FORMAT, uri) or re.match(LONG_DATASTORE_URI_REGEX_FORMAT, uri):
        return uri

    raise InvalidAmlDataUri(message_format="Invalid aml data uri: {aml_uri}", aml_uri=uri)


def _mount_aml_data(uri, destination, credential, runtime_config: RuntimeConfig) -> (str, AbstractContextManager):
    uri = _get_aml_uri(uri, credential, runtime_config)
    datastore = None
    data_path = None

    from azureml.core import Dataset, Datastore, Workspace

    workspace: Workspace = None
    if re.match(SHORT_DATASTORE_URI_REGEX_FORMAT, uri):
        datastore_name, data_path = re.match(SHORT_DATASTORE_URI_REGEX_FORMAT, uri).groups()
        workspace = runtime_config.get_workspace()
    elif re.match(LONG_DATASTORE_URI_REGEX_FORMAT, uri):
        sub, rg, ws, datastore_name, data_path = re.match(LONG_DATASTORE_URI_REGEX_FORMAT, uri).groups()
        workspace = runtime_config.get_workspace(subscription_id=sub, resource_group=rg, workspace_name=ws)
    else:
        raise InvalidAmlDataUri(message_format="Invalid aml data uri: {aml_uri}", aml_uri=uri)

    datastore = Datastore.get(workspace=workspace, datastore_name=datastore_name)
    file_dataset = Dataset.File.from_files(path=(datastore, data_path))
    return destination, file_dataset.mount(destination)


@retry(DownloadDataSystemError, tries=3, logger=logger)
def prepare_data(
    uri: str, destination: str = None, credential=None, runtime_config: RuntimeConfig = None, try_mount: bool = False
) -> (str, AbstractContextManager):
    """prepare data from blob_uri to local_file.

    Support mount for aml data uri.
    Args:
        uri: uri of the data
        destination: local folder to download or mount data
        credential: credential to access remote storage

    Returns:
        prepared local path
        mount context if mount is used
    """
    # convert to str in case not
    try:
        uri = str(uri)
        destination = str(destination)

        Path(destination).mkdir(
            parents=True, exist_ok=True
        )  # CodeQL [SM01305] Safe use per destination is set by PRT service not by end user

        from .utils._token_utils import get_default_credential

        if uri.startswith("azureml:"):
            if credential is None:
                credential = get_default_credential()
            # asset & datastore uri
            if try_mount:
                logger.info("Use mount mode to prepare data")
                destination, context = _mount_aml_data(uri, destination, credential, runtime_config)
                return destination, context
            return _download_aml_uri(uri, destination, credential, runtime_config), None
        if uri.startswith("wasbs:"):
            # storage blob uri
            if credential is None:
                credential = get_default_credential()
            return _download_blob(uri, destination, credential), None
        if uri.startswith("http"):
            # public http url
            return _download_public_http_url(uri, destination), None
        if os.path.exists(uri):
            # local file
            return uri, None
        else:
            raise InvalidDataUri(message_format="Invalid data uri: {uri}", uri=uri)
    except HttpResponseError as ex:
        logger.error(
            "Prepare data failed. StatusCode=%s. Exception={customer_content}",
            ex.status_code,
            extra={"customer_content": ex},
            exc_info=True,
        )
        if ex.status_code is not None and ex.status_code // 100 == 4:
            raise DownloadDataUserError(f"Prepare data failed. {str(ex)}") from ex
        else:
            raise DownloadDataSystemError(f"Prepare data failed. {str(ex)}") from ex
    except MlException as ex:
        logger.error(
            "Prepare data failed. Target=%s. Message=%s. Category=%s. Exception={customer_content}",
            ex.target,
            ex.no_personal_data_message,
            ex.error_category,
            extra={"customer_content": ex},
            exc_info=True,
        )
        if ex.error_category is not None and ex.error_category == ErrorCategory.USER_ERROR:
            raise DownloadDataUserError(f"Prepare data failed. {str(ex)}") from ex
        else:
            raise DownloadDataSystemError(f"Prepare data failed. {str(ex)}") from ex
    except ServiceResponseError as ex:
        logger.error(
            "Prepare data failed. Exception={customer_content}",
            extra={"customer_content": ex},
            exc_info=True,
        )
        raise DownloadDataSystemError(f"Prepare data failed. {str(ex)}") from ex
    except AzureMLUserErrorException as ex:
        logger.error(
            "Prepare data failed. Mount met exception={customer_content}",
            extra={"customer_content": ex},
            exc_info=True,
        )
        raise DownloadDataUserError(f"Prepare data failed. Mount met {str(ex)}") from ex
    except Exception as ex:
        if isinstance(ex, PromptflowException):
            raise ex
        logger.error(
            "Prepare data failed with exception={customer_content}",
            extra={"customer_content": ex},
            exc_info=True,
        )
        raise DownloadDataSystemError(f"Prepare data failed. {str(ex)}") from ex


@retry(DownloadDataSystemError, tries=3, logger=logger)
def prepare_blob_directory(
    uri: str, destination: str = None, credential=None, runtime_config: RuntimeConfig = None
) -> str:
    try:
        from .utils._token_utils import get_default_credential

        os.makedirs(destination, exist_ok=True)
        if uri.startswith("wasbs:"):
            uri = _wasbs_to_http_url(uri)
        if uri.startswith("http"):
            if credential is None:
                credential = get_default_credential()
            return _download_blob_directory(uri, destination, credential)
        else:
            destination, _ = prepare_data(uri, destination, credential, runtime_config)
            return destination
    except HttpResponseError as ex:
        logger.error(
            "Prepare blob directory failed. StatusCode=%s. Exception={customer_content}",
            ex.status_code,
            extra={"customer_content": ex},
            exc_info=True,
        )
        if ex.status_code is not None and ex.status_code // 100 == 4:
            raise DownloadDataUserError(f"Prepare blob directory failed. {str(ex)}") from ex
        else:
            raise DownloadDataSystemError(f"Prepare blob directory failed. {str(ex)}") from ex
    except MlException as ex:
        logger.error(
            "Prepare blob directory failed. Target=%s. Message=%s. Category=%s. Exception={customer_content}",
            ex.target,
            ex.no_personal_data_message,
            ex.error_category,
            extra={"customer_content": ex},
            exc_info=True,
        )
        if ex.error_category is not None and ex.error_category == ErrorCategory.USER_ERROR:
            raise DownloadDataUserError(f"Prepare blob directory failed. {str(ex)}") from ex
        else:
            raise DownloadDataSystemError(f"Prepare blob directory failed. {str(ex)}") from ex
    except ServiceResponseError as ex:
        logger.error(
            "Prepare blob directory failed. Exception={customer_content}",
            extra={"customer_content": ex},
            exc_info=True,
        )
        raise DownloadDataSystemError(f"Prepare blob directory failed. {str(ex)}") from ex
