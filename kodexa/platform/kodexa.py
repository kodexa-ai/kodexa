"""
Provides classes and utilities to allow you to interact with an instance of the Kodexa
platform.
"""

from __future__ import annotations

import errno
import io
import json
import logging
import os
import time
from json import JSONDecodeError
from typing import Dict

import requests
from appdirs import AppDirs

from kodexa.connectors import get_source
from kodexa.connectors.connectors import get_caller_dir, FolderConnector
from kodexa.model import Document
from kodexa.model.objects import (
    ExecutionEvent,
    ContentObject,
    AssistantEvent,
    ContentEvent,
    ScheduledEvent,
    DocumentFamilyEvent,
    ChannelEvent,
    DataObjectEvent,
    WorkspaceEvent,
)
from kodexa.pipeline import PipelineContext, PipelineStatistics
from kodexa.platform.client import DocumentStoreEndpoint, KodexaClient, process_response

logger = logging.getLogger()

dirs = AppDirs("Kodexa", "Kodexa")


def get_profile(profile=None):
    """
    Gets the current profile.

    Args:
        profile (str, optional): The profile to get. Defaults to None.

    Returns:
        str: The profile if it is defined, or "default" if it is not.
    """
    kodexa_config = get_config()
    if profile is None:
        if "_current_profile_" in kodexa_config:
            return kodexa_config["_current_profile_"]
        else:
            return "default"
    return profile


def get_config(profile=None, create=False):
    """
    Gets the kodexa config object used for local PAT storage.

    Args:
        profile (str, optional): The profile to get the config for. Defaults to current profile or "default"
        create (bool, optional): Whether to create a new profile if it does not exist. Defaults to False.

    Returns:
        dict: The kodexa config as a dictionary. If the profile exists in the config, it returns the config for that profile.
        If the profile does not exist, it creates a new profile with default values and returns it. If no profile is provided,
        it returns the default config. If the config file does not exist, it returns a default config or a new profile with
        default values depending on whether a profile was provided or not.
    """
    path = os.path.join(dirs.user_config_dir, ".kodexa.json")
    if os.path.exists(path):
        with open(path, "r") as outfile:
            kodexa_config = json.load(outfile)

            if "_current_profile_" in kodexa_config and profile is None:
                profile = kodexa_config["_current_profile_"]
                if profile is None:
                    raise Exception("No profile set")
            else:
                profile = "default" if profile is None else profile

            if profile not in kodexa_config:
                if create:
                    kodexa_config[profile] = {
                        "url": None,
                        "access_token": None,
                    }
                else:
                    raise Exception(f"Profile {profile} does not exist")
            return kodexa_config
    else:
        profile = "default" if profile is None else profile
        return (
            {profile: {"url": None, "access_token": None}}
        )


def save_config(config_obj):
    """
    Saves the configuration dictionary for the user.

    Args:
        config_obj (dict): The configuration dictionary to be saved.

    Raises:
        OSError: If the directory cannot be created, and the error is not that the directory already exists.
    """
    path = os.path.join(dirs.user_config_dir, ".kodexa.json")
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(path, "w") as outfile:
        json.dump(config_obj, outfile)


class KodexaPlatform:
    """
    The KodexaPlatform object allows you to work with an instance of the Kodexa platform, allow you to list, view and deploy
    components. It can also be used to get your access token and Kodexa platform URL using a user config file if available
    or Environment variables (KODEXA_ACCESS_TOKEN and KODEXA_URL).
    """

    """
    The KodexaPlatform object allows you to work with an instance of the Kodexa platform, allow you to list, view and deploy
    components

    Note it also can be used to get your access token and Kodexa platform URL using:

    * A user config file if available
    * Environment variables (KODEXA_ACCESS_TOKEN and KODEXA_URL)

    """

    @staticmethod
    def get_client():
        """
        Get a Kodexa client.

        Returns:
            KodexaClient: An instance of the Kodexa client.
        """
        from kodexa import KodexaClient

        return KodexaClient(KodexaPlatform.get_url(), KodexaPlatform.get_access_token())

    @staticmethod
    def get_access_token(profile=None) -> str:
        """
        Get the access token.

        Args:
            profile (str, optional): The profile to use. Defaults to None.

        Returns:
            str: The access token if it is defined in the user config store, or as an environment variable.
        """
        kodexa_config = get_config(profile)
        access_token = os.getenv("KODEXA_ACCESS_TOKEN")
        return (
            access_token
            if access_token is not None
            else kodexa_config[get_profile(profile)]["access_token"]
        )

    @staticmethod
    def get_url(profile=None) -> str:
        """
        Get the URL to use to access a Kodexa Platform.

        Args:
            profile (str, optional): The profile to use. Defaults to None.

        Returns:
            str: The URL if it is defined in the user config store, or as an environment variable.
        """
        kodexa_config = get_config(profile)
        env_url = os.getenv("KODEXA_URL", None)
        return (
            env_url
            if env_url is not None
            else kodexa_config[get_profile(profile)]["url"]
        )

    @staticmethod
    def set_access_token(access_token: str):
        """
        Set to override the access token to use. This does not impact your user config stored value.

        Args:
            access_token (str): The new access token.
        """
        if access_token is not None:
            os.environ["KODEXA_ACCESS_TOKEN"] = access_token

    @staticmethod
    def set_url(url: str):
        """
        Set to override the URL to use. This does not impact your user config stored value.

        Args:
            url (str): The new URL.
        """
        if url is not None:
            os.environ["KODEXA_URL"] = url

    @staticmethod
    def resolve_ref(ref: str):
        """
        Resolve the reference.

        Args:
            ref (str): The reference to resolve.

        Returns:
            list: A list containing the organization slug, slug, and version.
        """

        org_slug = ref.split("/")[0]
        slug = ref.split("/")[1].split(":")[0]

        version = None

        if len(ref.split("/")[1].split(":")) == 2:
            version = ref.split("/")[1].split(":")[1]

        return [org_slug, slug, version]

    @classmethod
    def configure(cls, kodexa_url, access_token, profile=None):
        """
        Configure kodexa access to platform

        Args
            kodexa_url (str): The URL of the Kodexa platform.
            access_token (str): The access token to use.
            profile (str, optional): The profile to use. Defaults to current profile or "default".
        """
        kodexa_config = get_config(profile)

        kodexa_config["_current_profile_"] = profile

        kodexa_config[profile] = {
            "url": kodexa_url,
            "access_token": access_token,
        }

        save_config(kodexa_config)

    @classmethod
    def list_profiles(cls):
        kodexa_config = get_config()

        # its the keys without __current_profile__
        return [key for key in kodexa_config if key != "_current_profile_"]

    @classmethod
    def get_current_profile(cls):
        return get_profile()

    @classmethod
    def set_profile(cls, profile):
        kodexa_config = get_config(profile)
        kodexa_config["_current_profile_"] = profile
        save_config(kodexa_config)

    @classmethod
    def delete_profile(cls, profile):
        kodexa_config = get_config(profile)
        del kodexa_config[profile]

        if kodexa_config["_current_profile_"] == profile:
            kodexa_config["_current_profile_"] = "default"

        save_config(kodexa_config)

    @classmethod
    def login(cls, kodexa_url, token, profile=None):
        """
        Login to the Kodexa platform.

        Args:
            kodexa_url (str): The URL of the Kodexa platform.
            token (str): The token to use for login.
            profile (str, optional): The profile to use. Defaults to None.
        """
        from requests.auth import HTTPBasicAuth

        obj_response = requests.get(
            f"{kodexa_url}/api/account/me",
            headers={"content-type": "application/json", "x-access-token": token, "cf-access-token": os.environ.get("CF_TOKEN", "")}
        )
        if obj_response.status_code == 200:
            kodexa_config = get_config(profile)
            kodexa_config[profile]["url"] = kodexa_url
            kodexa_config[profile]["access_token"] = token
            save_config(kodexa_config)
            print("Logged in")
        else:
            print(f"Check your URL and password [{obj_response.status_code}]")

    @classmethod
    def get_server_info(cls):
        """
        Get server information.

        Returns:
            dict: The server information.
        """
        r = requests.get(
            f"{KodexaPlatform.get_url()}/api",
            headers={
                "x-access-token": KodexaPlatform.get_access_token(),
                "cf-access-token": os.environ.get("CF_TOKEN", ""),
                "content-type": "application/json",
            },
        )
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        if r.status_code == 200:
            return r.json()

        logger.warning(r.text)
        raise Exception(
            "Unable to get server information, check your platform settings"
        )

    @classmethod
    def get_tempdir(cls):
        """
        Get the temporary directory.

        Returns:
            str: The path to the temporary directory.
        """
        import tempfile

        return os.getenv("KODEXA_TMP", tempfile.gettempdir())


class RemoteSession:
    """A Session on the Kodexa platform for leveraging pipelines and services"""

    """A Session on the Kodexa platform for leveraging pipelines and services"""

    def __init__(self, session_type, slug):
        self.session_type = session_type
        self.slug = slug
        self.cloud_session = None

    def get_action_metadata(self, ref):
        """
        Download metadata for a specific action.

        Args:
            ref (str): The reference of the action.

        Returns:
            dict: The metadata of the action if the request is successful.
        """
        logger.debug(f"Downloading metadata for action {ref}")
        r = requests.get(
            f"{KodexaPlatform.get_url()}/api/actions/{ref.replace(':', '/')}",
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
        )
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        if r.status_code == 200:
            return r.json()

        logger.warning(r.text)
        raise Exception(
            "Unable to get action metadata, check your reference and platform settings"
        )

    def start(self):
        """
        Start the session.
        """
        logger.info(f"Creating session {self.slug} ({KodexaPlatform.get_url()})")
        r = requests.post(
            f"{KodexaPlatform.get_url()}/api/sessions",
            params={self.session_type: self.slug},
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
        )

        process_response(r)

        self.cloud_session = json.loads(r.text)

    def execution_action(self, document, options, attach_source, context):
        """
        Execute an action in the session.

        Args:
            document (Document): The document to be processed.
            options (dict): The options for the action.
            attach_source (bool): Whether to attach the source to the call.
            context (Context): The context of the execution.

        Returns:
            dict: The execution result.
        """
        files = {}
        if attach_source:
            logger.debug("Attaching source to call")
            files["file"] = get_source(document)
            files["file_document"] = document.to_kddb()
        else:
            files["document"] = document.to_kddb()

        data = {
            "options": json.dumps(options),
            "document_metadata_json": json.dumps(document.metadata),
            "context": json.dumps(context.context),
        }

        logger.info(f"Executing session {self.cloud_session.id}")
        r = requests.post(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/execute",
            params={self.session_type: self.slug, "documentVersion": document.version},
            data=data,
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
            files=files,
        )
        try:
            if r.status_code == 200:
                execution = json.loads(r.text)
            else:
                logger.warning(
                    "Execution creation failed ["
                    + r.text
                    + "], response "
                    + str(r.status_code)
                )
                raise Exception(
                    "Execution creation failed ["
                    + r.text
                    + "], response "
                    + str(r.status_code)
                )
        except JSONDecodeError:
            logger.warning(
                "Unable to handle response ["
                + r.text
                + "], response "
                + str(r.status_code)
            )
            raise

        return execution

    def wait_for_execution(self, execution):
        """
        Wait for the execution to finish.

        Args:
            execution (dict): The execution to wait for.

        Returns:
            dict: The execution result.
        """
        status = execution.status
        while execution.status == "PENDING" or execution.status == "RUNNING":
            r = requests.get(
                f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}",
                headers={"x-access-token": KodexaPlatform.get_access_token(),
                         "cf-access-token": os.environ.get("CF_TOKEN", "")},
            )
            try:
                execution = json.loads(r.text)
            except JSONDecodeError:
                logger.warning("Unable to handle response [" + r.text + "]")
                raise

            if status != execution.status:
                logger.info(f"Status changed from {status} -> {execution.status}")
                status = execution.status

            time.sleep(5)

        if status == "FAILED":
            logger.warning("Execution has failed")
            for step in execution.steps:
                if step.status == "FAILED":
                    logger.warning(
                        f"Step {step.name} has failed. {step.exceptionDetails.message}."
                    )

                    if step.exceptionDetails.errorType == "Validation":
                        logger.warning(
                            "Additional validation information has been provided:"
                        )
                        for validation_error in step.exceptionDetails.validationErrors:
                            logger.warning(
                                f"- {validation_error.option} : {validation_error.message}"
                            )

                    if step.exceptionDetails.help:
                        logger.warning(
                            f"Additional help is available:\n\n{step.exceptionDetails.help}"
                        )

                    raise Exception(f"Processing has failed on step {step.name}")

            raise Exception("Processing has failed, no steps seem to have failed")

        return execution

    def get_output_document(self, execution):
        """
        Get the output document from a given execution.

        Args:
            execution (dict): The execution holding the document.

        Returns:
            Document: The output document (or None if there isn't one).
        """
        if execution.outputId:
            logger.info(f"Downloading output document [{execution.outputId}]")
            doc = requests.get(
                f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}/objects/{execution.outputId}",
                headers={"x-access-token": KodexaPlatform.get_access_token(),
                         "cf-access-token": os.environ.get("CF_TOKEN", "")},
            )
            return Document.from_kddb(doc.content)

        logger.info("No output document")
        return None


class RemotePipeline:
    """A class to interact with a pipeline that has been deployed to an instance of Kodexa Platform.

    Attributes:
        slug (str): The slug for the remote pipeline.
        connector (Document or list): The document or list of documents to be processed.
        version (str, optional): The version of the pipeline. Defaults to None.
        attach_source (bool, optional): Whether to attach the source document to the pipeline. Defaults to True.
        parameters (dict, optional): The parameters for the pipeline. Defaults to an empty dictionary.
        auth (list, optional): The authentication credentials. Defaults to an empty list.
    """

    """Allow you to interact with a pipeline that has been deployed to an instance of Kodexa Platform"""

    def __init__(
            self,
            slug,
            connector,
            version=None,
            attach_source=True,
            parameters=None,
            auth=None,
    ):
        logger.info(f"Initializing a new pipeline {slug}")

        if isinstance(connector, Document):
            self.connector = [connector]
        else:
            self.connector = connector
        self.context: PipelineContext = PipelineContext()

        if auth is None:
            auth = []
        if parameters is None:
            parameters = {}
        self.slug = slug
        self.version = version
        self.attach_source = attach_source
        self.parameters = parameters
        self.auth = auth

    def run(self):
        """Runs the pipeline and returns the context."""
        self.context.statistics = PipelineStatistics()

        logger.info(f"Starting remote pipeline {self.slug}")
        cloud_session = RemoteSession("pipeline", self.slug)
        cloud_session.start()

        for document in self.connector:
            logger.info(f"Processing {document}")
            execution = cloud_session.execution_action(
                document, self.parameters, self.attach_source, self.context
            )
            execution = cloud_session.wait_for_execution(execution)

            logger.info("Capturing output")
            result_document = cloud_session.get_output_document(execution)
            self.context.set_output_document(result_document)

            self.context.statistics.processed_document(result_document)
            self.context.context = execution.context

        logger.info(f"Completed pipeline {self.slug}")

        return self.context

    @staticmethod
    def from_url(slug: str, url, headers=None, *args, **kwargs) -> RemotePipeline:
        """Creates a new pipeline with the input being a document created from the given URL.

        Args:
            slug (str): The slug for the remote pipeline.
            url (str): The URL to create the document from.
            headers (dict, optional): A dictionary of headers. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            RemotePipeline: A new instance of a remote pipeline.
        """
        return RemotePipeline(slug, Document.from_url(url, headers), *args, **kwargs)

    @staticmethod
    def from_file(
            slug: str, file_path: str, unpack: bool = False, *args, **kwargs
    ) -> RemotePipeline:
        """Creates a new pipeline using a file path as a source.

        Args:
            slug (str): The slug for the remote pipeline.
            file_path (str): The path to the file.
            unpack (bool, optional): Whether to unpack the file as a KDXA. Defaults to False.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            RemotePipeline: A new instance of a remote pipeline.
        """
        return RemotePipeline(
            slug, Document.from_file(file_path, unpack), *args, **kwargs
        )

    @staticmethod
    def from_text(slug: str, text: str, *args, **kwargs) -> RemotePipeline:
        """Creates a new pipeline and provides text as the basis to create a document.

        Args:
            slug (str): The slug for the remote pipeline.
            text (str): The text to use to create the document.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            RemotePipeline: A new instance of a remote pipeline.
        """

        # need to update kwargs for attach_source
        kwargs.setdefault("attach_source", False)
        return RemotePipeline(slug, Document.from_text(text), *args, **kwargs)

    @staticmethod
    def from_folder(
            slug: str,
            folder_path: str,
            filename_filter: str = "*",
            recursive: bool = False,
            unpack: bool = False,
            relative: bool = False,
            caller_path: str = get_caller_dir(),
    ) -> RemotePipeline:
        """Creates a pipeline that will run against a set of local files from a folder.

        Args:
            slug (str): The slug for the remote pipeline.
            folder_path (str): The folder path.
            filename_filter (str, optional): The filter for filename (i.e. *.pdf). Defaults to "*".
            recursive (bool, optional): Whether to look recursively in sub-directories. Defaults to False.
            unpack (bool, optional): Whether to unpack the file as a KDXA document. Defaults to False.
            relative (bool, optional): Whether the folder path is relative to the caller. Defaults to False.
            caller_path (str, optional): The caller path. Defaults to the path from the stack.

        Returns:
            RemotePipeline: A new instance of a remote pipeline.
        """
        return RemotePipeline(
            slug,
            FolderConnector(
                folder_path,
                filename_filter,
                recursive,
                relative,
                caller_path,
                unpack=unpack,
            ),
        )


class RemoteStep:
    """Allows you to interact with a step that has been deployed in the Kodexa platform"""

    """Allows you to interact with a step that has been deployed in the Kodexa platform"""

    def __init__(self, ref, step_type="ACTION", attach_source=False, options=None, conditional=None):
        if options is None:
            options = {}
        self.ref = ref
        self.step_type = step_type
        self.attach_source = attach_source
        self.options = options
        self.conditional = conditional

    def to_dict(self):
        """Converts the RemoteStep object to a dictionary.

        Returns:
            dict: Dictionary representation of the RemoteStep object.
        """
        return {"ref": self.ref, "step_type": self.step_type, "options": self.options, "conditional": self.conditional}

    def get_name(self):
        """Generates a name for the RemoteStep object.

        Returns:
            str: Name of the RemoteStep object.
        """
        return f"Remote Action ({self.ref})"

    def process(self, document, context):
        """Processes the document and context using the RemoteStep.

        Args:
            document (Document): The document to be processed.
            context (Context): The context for processing.

        Returns:
            Document: The processed document.
        """
        cloud_session = RemoteSession("service", self.ref)
        cloud_session.start()

        logger.info(f"Loading metadata for {self.ref}")
        action_metadata = cloud_session.get_action_metadata(self.ref)

        requires_source = False
        if "requiresSource" in action_metadata["metadata"]:
            requires_source = action_metadata["metadata"]["requiresSource"]

        execution = cloud_session.execution_action(
            document,
            self.options,
            self.attach_source if self.attach_source else requires_source,
            context,
        )

        logger.debug("Waiting for remote execution")
        execution = cloud_session.wait_for_execution(execution)

        logger.debug("Downloading the result document")
        result_document = cloud_session.get_output_document(execution)

        logger.debug("Set the context to match the context from the execution")
        context.context = execution.context

        return result_document if result_document else document

    def to_configuration(self):
        """Returns a dictionary representing the configuration information for the step.

        Returns:
            dict: Dictionary representing the configuration of the step.
        """
        return {"ref": self.ref, "options": self.options}


class EventHelper:
    """Helper class for handling events.

    Attributes:
        event (ExecutionEvent): The execution event instance.
    """

    def __init__(self, event: ExecutionEvent):
        self.event: ExecutionEvent = event

    @staticmethod
    def get_base_event(event_dict: Dict):
        """Returns the base event based on the event type.

        Args:
            event_dict (Dict): The event dictionary.

        Raises:
            Exception: If the event type is unknown.
        """
        if event_dict["type"] == "assistant":
            return AssistantEvent(**event_dict)
        if event_dict["type"] == "content":
            return ContentEvent(**event_dict)
        if event_dict["type"] == "scheduled":
            return ScheduledEvent(**event_dict)
        if event_dict["type"] == "channel":
            return ChannelEvent(**event_dict)
        if event_dict["type"] == "documentFamily":
            return DocumentFamilyEvent(**event_dict)
        if event_dict["type"] == "dataObject":
            return DataObjectEvent(**event_dict)
        if event_dict["type"] == "workspace":
            return WorkspaceEvent(**event_dict)

        raise f"Unknown event type {event_dict}"

    def log(self, message: str):
        """Logs a message to the Kodexa platform.

        Args:
            message (str): The message to log.
        """
        response = requests.post(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/logs",
            json=[{"entry": message}],
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
            timeout=300,
        )
        if response.status_code != 200:
            print(f"Logging failed {response.status_code}", flush=True)

    def get_content_object(self, content_object_id: str):
        """Gets a content object from the Kodexa platform.

        Args:
            content_object_id (str): The ID of the content object.

        Raises:
            Exception: If the content object cannot be found.

        Returns:
            io.BytesIO: The content object.
        """
        logger.info(
            f"Getting content object {content_object_id} in event {self.event.id} in execution {self.event.execution.id}"
        )

        co_response = requests.get(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/objects/{content_object_id}",
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
            timeout=300
        )
        process_response(co_response)
        return io.BytesIO(co_response.content)

    def put_content_object(
            self, content_object: ContentObject, content
    ) -> ContentObject:
        """Puts a content object to the Kodexa platform.

        Args:
            content_object (ContentObject): The content object.
            content: The content.

        Raises:
            Exception: If the content object cannot be posted back.

        Returns:
            ContentObject: The posted content object.
        """
        files = {"content": content}
        data = {"contentObjectJson": json.dumps(content_object.dict(by_alias=True))}
        logger.info("Posting back content object to execution object")
        co_response = requests.post(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/objects",
            data=data,
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
            files=files,
            timeout=300
        )

        process_response(co_response)

        logger.info("Object posted back")

        return ContentObject.model_validate(co_response.json())

    def build_pipeline_context(self) -> PipelineContext:
        """Builds a pipeline context.

        Returns:
            PipelineContext: The pipeline context.
        """
        context = PipelineContext(
            context={}, content_provider=self, execution_id=self.event.execution.id
        )

        if self.event.store_ref and self.event.document_family_id:
            logger.info("We have storeRef and document family")
            rds: DocumentStoreEndpoint = KodexaClient().get_object_by_ref(
                "store", self.event.store_ref
            )
            document_family = rds.get_family(self.event.document_family_id)

            context.document_family = document_family
            context.document_store = rds

        return context

    def get_input_document(self, context):
        """Gets the input document.

        Args:
            context: The context.

        Returns:
            Document: The input document.
        """
        for content_object in self.event.execution.content_objects:
            if content_object.id == self.event.input_id:
                input_document_bytes = self.get_content_object(self.event.input_id)
                logger.info("Loading KDDB document")
                input_document = Document.from_kddb(input_document_bytes.read())
                logger.info("Loaded KDDB document")
                context.content_object = content_object
                input_document.uuid = context.content_object.id

                if content_object.store_ref is not None:
                    context.document_store = KodexaClient().get_object_by_ref(
                        "store", content_object.store_ref
                    )

                return input_document


class SessionConnector:
    """
    A class used to represent a SessionConnector.

    ...

    Attributes
    ----------
    event_helper : object
        a helper object used in the connector, default is None

    Methods
    -------
    get_name():
        Returns the name of the cloud content.

    get_source(document):
        Returns the content object of the document source.
    """

    event_helper = None

    @classmethod
    def get_name(cls):
        """
        Gets the name of the cloud content.

        Returns
        -------
        str
            The name of the cloud content.
        """
        return "cloud-content"

    @classmethod
    def get_source(cls, document):
        """
        Gets the content object of the document source.

        Parameters
        ----------
        document : object
            The document object to get the source from.

        Raises
        ------
        Exception
            If the event_helper is not set.

        Returns
        -------
        object
            The content object of the document source.
        """
        if cls.event_helper is None:
            raise Exception("The event_helper needs to be set to use this connector")

        logger.info(f"Getting content object {document.source.original_path}")
        return cls.event_helper.get_content_object(document.source.original_path)
