"""
Provides classes and utilities to allow you to interact with an instance of the Kodexa
platform.
"""

from __future__ import annotations

import errno
import json
import logging
import os
import sys
import time
from json import JSONDecodeError

import jsonpickle
import requests
import yaml
from addict import Dict
from appdirs import AppDirs
from rich import print

from kodexa.assistant import Assistant
from kodexa.connectors import get_source
from kodexa.connectors.connectors import get_caller_dir, FolderConnector
from kodexa.model import Document, DocumentStore
from kodexa.pipeline import PipelineContext, Pipeline, PipelineStatistics
from kodexa.stores import RemoteDocumentStore
from kodexa.stores import TableDataStore, RemoteModelStore, LocalDocumentStore, LocalModelStore
from kodexa.taxonomy import Taxonomy

logger = logging.getLogger('kodexa.platform')

dirs = AppDirs("Kodexa", "Kodexa")


def get_config():
    """Get the kodexa config object we use when you want to store your PAT locally

    :return: the config as a dict

    Args:

    Returns:

    """
    path = os.path.join(dirs.user_config_dir, '.kodexa.json')
    if os.path.exists(path):
        with open(path, 'r') as outfile:
            return json.load(outfile)
    else:
        return {'url': None, 'access_token': None}


def save_config(config_obj):
    """Saves the configuration dictionary for the user

    Args:
      config_obj: return:

    Returns:

    """
    path = os.path.join(dirs.user_config_dir, '.kodexa.json')
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(path, 'w') as outfile:
        json.dump(config_obj, outfile)


class PipelineMetadataBuilder:
    """Build a metadata representation of the pipeline for passing to an instance of the
    Kodexa platform
    """

    def __init__(self, pipeline: Pipeline):
        """
        Initialize the pipeline builder based on the given pipeline

        Args:
            pipeline:
        """
        self.pipeline = pipeline

    def build_steps(self, pipeline_metadata: Dict):
        """
        Build up the pipeline metadata definition (extending the argument) based on the pipeline.

        This will create a serializable representation of the pipeline that we can send to a Kodexa platform
        instance for execution

        Args:
          pipeline_metadata: Dict: The dictionary that will hold the metadata represenation of the pipeline

        Returns: The updated pipeline_metadata

        """
        pipeline_metadata.metadata.steps = []
        pipeline_metadata.metadata.stores = []

        for pipeline_store in self.pipeline.stores:

            if isinstance(pipeline_store.store, RemoteDocumentStore):
                pipeline_metadata.metadata.stores.append(
                    {"name": pipeline_store.name, "ref": pipeline_store.store.get_ref(), "storeType": "DOCUMENT"})
            else:
                raise Exception("Pipeline refers to a non-remote store, deployment of local stores is not supported")

        for idx, step in enumerate(self.pipeline.steps):

            step_meta = step.to_dict()
            if step_meta['name'] is None:
                step_meta['name'] = f"Step {idx + 1}"

            if 'script' in step_meta:
                pipeline_metadata.metadata.steps.append({
                    'ref': 'kodexa/python-step',
                    'name': step_meta['name'],
                    'enabled': True,
                    'condition': None,
                    'options': {
                        'function_name': step_meta['function'],
                        'script': step_meta['script']
                    }
                })
            else:
                pipeline_metadata.metadata.steps.append(step_meta)

        return pipeline_metadata


DEFAULT_COLUMNS = {
    'extensionPacks': [
        'orgSlug',
        'slug',
        'version',
        'name',
        'description',
        'type',
        'status'
    ],
    'default': [
        'orgSlug',
        'slug',
        'version',
        'name',
        'description',
        'type'
    ]
}

OBJECT_TYPES = {
    "extensionPacks": {
        "name": "extension pack",
        "plural": "extension packs"
    },
    "pipelines": {
        "name": "pipeline",
        "plural": "pipelines"
    },
    "assistants": {
        "name": "assistant",
        "plural": "assistants"
    },
    "actions": {
        "name": "action",
        "plural": "actions"
    },
    "stores": {
        "name": "store",
        "plural": "stores"
    },
    "connectors": {
        "name": "connector",
        "plural": "connectors"
    },
    "taxonomies": {
        "name": "taxonomy",
        "plural": "taxonomies"
    }
}


def resolve_object_type(obj_type):
    """Takes part of an object type (ie. pipelin) and then resolves the object type (pipelines)

    Args:
      obj_type: part of the object type

    Returns:
      The object type dict (if found)

    """
    hits = []
    keys = []
    for target_type in OBJECT_TYPES.keys():
        if obj_type in target_type:
            hits.append(OBJECT_TYPES[target_type])
            keys.append(target_type)

    if len(hits) == 1:
        return keys[0], hits[0]

    if len(hits) == 0:
        print(":exclaimation: Unable to find object type {obj_type}")
        sys.exit(1)
    else:
        print(f":exclaimation: To many potential matches for object type ({','.join(keys)}")
        sys.exit(1)


class KodexaPlatform:
    """The KodexaPlatform object allows you to work with an instance of the Kodexa platform, allow you to list, view and deploy
    components

    Note it also can be used to get your access token and Kodexa platform URL using:

    * A user config file if available
    * Environment variables (KODEXA_ACCESS_TOKEN and KODEXA_URL)

    """

    @staticmethod
    def get_access_token() -> str:
        """
        Returns the access token

        >>> access_token = KodexaPlatform.get_access_token()

        Returns: The access token if it is defined in the user config store, or as an environment variable

        """
        kodexa_config = get_config()
        access_token = os.getenv('KODEXA_ACCESS_TOKEN')
        return access_token if access_token is not None else kodexa_config['access_token']

    @staticmethod
    def get_url() -> str:
        """
        Returns the URL to use to access a Kodexa Platform

        The URL should be in the form https://my-server.my-company.com

        >>> access_token = KodexaPlatform.get_url()

        Returns: The URL if it is defined in the user config store, or as an environment variable

        """
        kodexa_config = get_config()
        env_url = os.getenv('KODEXA_URL', None)
        return env_url if env_url is not None else kodexa_config['url']

    @staticmethod
    def set_access_token(access_token: str):
        """
        Set to override the access token to use, not that this does not impact your user config stored
        value

        Args:
          access_token:str: The new access token

        Returns: None

        """
        if access_token is not None:
            os.environ["KODEXA_ACCESS_TOKEN"] = access_token

    @staticmethod
    def set_url(url: str):
        """
        Set to override the URL to use, not that this does not impact your user config stored
        value

        Args:
          url:str: The new URL

        Returns: None

        """
        if url is not None:
            os.environ["KODEXA_URL"] = url

    @staticmethod
    def get_access_token_details() -> Dict:
        """
        Pull the access token details (including a list of the available organizations)

        Returns: Dict: details of the access token

        """
        response = requests.get(
            f"{KodexaPlatform.get_url()}/api/account/accessToken",
            headers={"x-access-token": KodexaPlatform.get_access_token()})
        if response.status_code == 200:
            return Dict(response.json())
        else:
            if response.status_code == 404:
                raise Exception("Unable to find access token")
            else:
                raise Exception("An error occurred connecting to the Kodexa platform")

    @staticmethod
    def deploy_extension(metadata):
        """

        Args:
          metadata:

        Returns:

        """
        response = requests.post(f"{KodexaPlatform.get_url()}/api/extensionPacks/{metadata['orgSlug']}",
                                 json=metadata.to_dict(),
                                 headers={"x-access-token": KodexaPlatform.get_access_token(),
                                          "content-type": "application/json"})
        if response.status_code == 200:
            logger.info("Extension deployed")
        else:
            logger.error(response.text)
            raise Exception("Unable to deploy new extension")

    @staticmethod
    def deploy_extension_from_uri(path, organisation_slug):
        """

        Args:
          path:
          organisation_slug:

        Returns:

        """
        url = f"{KodexaPlatform.get_url()}/api/extensionPacks/{organisation_slug}?uri={path}"
        logger.info(f"Publishing extension pack to organization {organisation_slug}")
        response = requests.post(url,
                                 headers={"x-access-token": KodexaPlatform.get_access_token(),
                                          "content-type": "application/json"})
        if response.status_code == 200:
            logger.info("Extension deployed")
        else:
            logger.error(response.text)
            raise Exception("Unable to deploy new extension")

    @staticmethod
    def resolve_ref(ref: str):
        """

        Args:
          ref: str:

        Returns:

        """
        org_slug = ref.split('/')[0]
        slug = ref.split('/')[1].split(":")[0]

        version = None

        if len(ref.split('/')[1].split(":")) == 2:
            version = ref.split('/')[1].split(":")[1]

        return [org_slug, slug, version]

    @staticmethod
    def get_object_instance(ref: str, object_type: str):
        """

        Args:
          ref: str:
          object_type: str:

        Returns:

        """
        object_type, object_type_metadata = resolve_object_type(object_type)

        if object_type == 'taxonomies':
            from kodexa import RemoteTaxonomy
            return RemoteTaxonomy.get(ref)
        if object_type == 'stores':
            # We need to work out what type of store we have
            obj_info = KodexaPlatform.get_object(ref, object_type)
            if obj_info['storeType'] == 'TABLE':
                from kodexa import RemoteTableDataStore
                return RemoteTableDataStore(ref)
            if obj_info['storeType'] == 'DOCUMENT':
                return RemoteDocumentStore(ref)
            if obj_info['storeType'] == 'MODEL':
                return RemoteModelStore(ref)

        # TODO - there are other things we need?
        raise Exception(f"Unable to get a local instance of {ref} of type {object_type}")

    @staticmethod
    def deploy(ref: str, kodexa_object, name: str = None, description: str = None,
               options=None, public=False, force_replace=False, dry_run=False, print_yaml=False):
        """

        Args:
          ref: str:
          kodexa_object:
          name: str:  (Default value = None)
          description: str:  (Default value = None)
          options:  (Default value = None)
          public:  (Default value = False)
          force_replace:  (Default value = False)
          dry_run:  (Default value = False)
          print_yaml:  (Default value = False)

        Returns:

        """

        if '/' not in ref:
            logger.error("A ref must be valid, i.e. org_slug/pipeline_slug:version")
            raise Exception("Invalid slug")

        [organization_slug, object_slug, object_version] = KodexaPlatform.resolve_ref(ref)

        if options is None:
            options = {}

        metadata_object = Dict()
        metadata_object.orgSlug = organization_slug
        metadata_object.publicAccess = public
        metadata_object.slug = object_slug
        metadata_object.version = object_version
        metadata_object.name = name
        metadata_object.description = description

        object_url = None

        from kodexa import RemoteTableDataStore

        if isinstance(kodexa_object, Pipeline):

            metadata_object.name = 'New Pipeline' if metadata_object.name is None else metadata_object.name
            metadata_object.description = 'A new pipeline' if metadata_object.description is None else metadata_object.description

            object_url = "pipelines"

            if "example_urls" not in options:
                example_urls = []
            else:
                example_urls = options["example_urls"]

            if "more_info_url" not in options:
                more_info_url = None
            else:
                more_info_url = options["more_info_url"]

            builder = PipelineMetadataBuilder(kodexa_object)

            metadata_object.type = 'pipeline'
            metadata_object.metadata.parameters = []
            metadata_object.metadata.steps = []
            metadata_object.exampleUrls = example_urls
            metadata_object.moreInfoUrl = more_info_url

            builder.build_steps(metadata_object)

        elif isinstance(kodexa_object, LocalDocumentStore) or isinstance(kodexa_object, RemoteDocumentStore):
            object_url = 'stores'
            metadata_object.name = 'New Store' if metadata_object.name is None else metadata_object.name
            metadata_object.description = 'A document store' if metadata_object.description is None else metadata_object.description
            metadata_object.type = 'store'
            metadata_object.storeType = 'DOCUMENT'
        elif isinstance(kodexa_object, LocalModelStore) or isinstance(kodexa_object, RemoteModelStore):
            object_url = 'stores'
            metadata_object.name = 'New Store' if metadata_object.name is None else metadata_object.name
            metadata_object.description = 'A model store' if metadata_object.description is None else metadata_object.description
            metadata_object.type = 'store'
            metadata_object.storeType = 'MODEL'
        elif isinstance(kodexa_object, RemoteTableDataStore):
            object_url = 'stores'
            metadata_object.name = 'New Store' if metadata_object.name is None else metadata_object.name
            metadata_object.description = 'A table data store' if metadata_object.description is None else metadata_object.description
            metadata_object.type = 'store'
            metadata_object.storeType = 'TABLE'
        elif isinstance(kodexa_object, Taxonomy):
            metadata_object.name = 'New Taxonomy' if metadata_object.name is None else metadata_object.name
            metadata_object.description = 'A new taxonomy' if metadata_object.description is None else metadata_object.description
            object_url = 'taxonomies'
            metadata_object.type = 'taxonomy'
            metadata_object.enabled = kodexa_object.enabled
            metadata_object.taxonomyType = kodexa_object.taxonomy_type
            metadata_object.taxons = jsonpickle.decode(
                jsonpickle.encode([taxon.to_dict() for taxon in kodexa_object.taxons], unpicklable=False))
        elif isinstance(kodexa_object, Assistant):
            metadata_object.name = 'New Assistant Definition' if metadata_object.name is None else metadata_object.name
            metadata_object.description = 'A new assistant definition' if metadata_object.description is None else metadata_object.description
            object_url = 'assistants'
            metadata_object.type = 'assistant'

        else:
            raise Exception("Unknown object type, unable to deploy")

        if dry_run:

            if print_yaml:
                logger.info(f"Dry run output for {metadata_object.type} {ref}")
                logger.info(f"YAML output:\n")
                logger.info(yaml.dump(metadata_object.to_dict()))

        else:
            logger.info(f"Deploying {metadata_object.type} {ref}")

            access_token = KodexaPlatform.get_access_token_details()

            if organization_slug not in access_token.organizationSlugs:
                logger.error(f"You do not have access to the organization {organization_slug}")
                raise Exception("Unable to deploy, no access to organization")

            if object_version:
                url = f"{KodexaPlatform.get_url()}/api/{object_url}/{organization_slug}/{object_slug}/{object_version}"
            else:
                url = f"{KodexaPlatform.get_url()}/api/{object_url}/{organization_slug}/{object_slug}"

            response = requests.get(url,
                                    headers={"x-access-token": KodexaPlatform.get_access_token(),
                                             "content-type": "application/json"})

            if response.status_code == 401:
                logger.error(f"You do not have the permissions to access this {metadata_object.type}")
                raise Exception("Not authorized on pipeline")

            if response.status_code == 404:
                logger.info("Object doesn't exist, will deploy")
                response = requests.post(f"{KodexaPlatform.get_url()}/api/{object_url}/{organization_slug}",
                                         json=metadata_object.to_dict(),
                                         headers={"x-access-token": KodexaPlatform.get_access_token(),
                                                  "content-type": "application/json"})
                if response.status_code == 200:
                    logger.info("Deployed")
                else:
                    logger.error(response.text)
                    raise Exception("Unable to deploy")
            elif response.status_code == 200:
                logger.info(f"{ref} already exists")
                if force_replace:
                    logger.info(f"Replacing {ref}")
                    response = requests.put(url,
                                            json=metadata_object.to_dict(),
                                            headers={"x-access-token": KodexaPlatform.get_access_token(),
                                                     "content-type": "application/json"})
                    if response.status_code == 200:
                        logger.info("Deployed")
                    else:
                        logger.error(response.text)
                        raise Exception("Unable to deploy and replace")
                else:
                    logger.warning("Not updating")
                    return
            else:
                logger.error("Unable to deploy")
                logger.error(response.content)

        return metadata_object

    @staticmethod
    def list_objects(organization_slug, object_type):
        """

        Args:
          organization_slug:
          object_type:

        Returns:

        """
        list_response = requests.get(f"{KodexaPlatform.get_url()}/api/{object_type}/{organization_slug}",
                                     headers={"x-access-token": KodexaPlatform.get_access_token(),
                                              "content-type": "application/json"})
        if list_response.status_code == 200:
            return list_response.json()
        else:
            logger.error(list_response.text)
            raise Exception("Unable to list objects")

    @staticmethod
    def undeploy(object_type: str, ref: str):
        """

        Args:
          object_type: str:
          ref: str:

        Returns:

        """

        object_type, object_type_metadata = resolve_object_type(object_type)

        url_ref = ref.replace(':', '/')
        response = requests.delete(f"{KodexaPlatform.get_url()}/api/{object_type_metadata['plural']}/{url_ref}",
                                   headers={"x-access-token": KodexaPlatform.get_access_token(),
                                            "content-type": "application/json"})
        if response.status_code == 200:
            logger.info(f"Undeployed {object_type_metadata['name']} {ref}")
        else:
            logger.error(response.text)
            raise Exception(f"Unable to undeploy {object_type_metadata['name']} {ref}")

    @staticmethod
    def delete_object(ref, object_type):
        """

        Args:
          ref:
          object_type:

        Returns:

        """
        # Generate a URL ref
        url_ref = ref.replace(':', '/')
        delete_response = requests.delete(f"{KodexaPlatform.get_url()}/api/{object_type}/{url_ref}",
                                          headers={"x-access-token": KodexaPlatform.get_access_token(),
                                                   "content-type": "application/json"})
        if delete_response.status_code != 200:
            logger.error(delete_response.text)
            raise Exception("Unable to list objects")

    @staticmethod
    def get_object(ref, object_type):
        """

        Args:
          ref:
          object_type:

        Returns:

        """
        url_ref = ref.replace(':', '/')
        obj_response = requests.get(f"{KodexaPlatform.get_url()}/api/{object_type}/{url_ref}",
                                    headers={"x-access-token": KodexaPlatform.get_access_token(),
                                             "content-type": "application/json"})
        if obj_response.status_code != 200:
            logger.error(obj_response.text)
            raise Exception(f"Unable to get object {ref}")
        else:
            return obj_response.json()

    @classmethod
    def get(cls, object_type, ref, path=None):
        """

        Args:
          object_type:
          ref:
          path:  (Default value = None)

        Returns:

        """

        object_type, object_type_metadata = resolve_object_type(object_type)

        try:

            # If ref is just the org then we will list them
            if '/' in ref:
                obj = KodexaPlatform.get_object(ref, object_type)

                if path is not None:
                    import jq
                    obj = jq.compile(path).input(obj).all()
                import yaml
                print(obj)
            else:
                objects = KodexaPlatform.list_objects(ref, object_type)
                cols = DEFAULT_COLUMNS['default']

                if object_type in DEFAULT_COLUMNS:
                    cols = DEFAULT_COLUMNS[object_type]

                print("\n")
                from rich.table import Table

                table = Table(title=f"Listing {object_type_metadata['plural']}")
                for col in cols:
                    table.add_column(col)
                for object_dict in objects['content']:
                    row = []

                    for col in cols:
                        row.append(object_dict[col] if col in object_dict else '')
                    table.add_row(*row)

                print(table)
        except:
            print(f"\n:exclamation: Failed to get {object_type_metadata['name']} [{sys.exc_info()[0]}]")

    @classmethod
    def delete(cls, object_type, ref):
        """

        Args:
          object_type:
          ref:

        Returns:

        """
        object_type, object_type_metadata = resolve_object_type(object_type)
        print(f"Deleting {object_type_metadata['name']} [bold]{ref}[/bold]")

        try:
            KodexaPlatform.delete_object(ref, object_type)
            print(f"Deleted {object_type_metadata['name']} [bold]{ref}[/bold] :tada:")
        except:
            print(f"\n:exclamation: Failed to delete {object_type_metadata['name']} [{sys.exc_info()[0]}]")

    @classmethod
    def login(cls, kodexa_url, username, password):
        """

        Args:
          kodexa_url:
          username:
          password:

        Returns:

        """
        from requests.auth import HTTPBasicAuth
        obj_response = requests.get(f"{kodexa_url}/api/account/me/token",
                                    auth=HTTPBasicAuth(username, password),
                                    headers={"content-type": "application/json"})
        if obj_response.status_code == 200:
            kodexa_config = get_config()
            kodexa_config['url'] = kodexa_url
            kodexa_config['access_token'] = obj_response.text
            save_config(kodexa_config)
            print("Logged in")
        else:
            print(f"Check your URL and password [{obj_response.status_code}]")

    @classmethod
    def get_server_info(cls):
        """ """
        r = requests.get(f"{KodexaPlatform.get_url()}/api",
                         headers={"x-access-token": KodexaPlatform.get_access_token(),
                                  "content-type": "application/json"})
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        elif r.status_code == 200:
            return r.json()
        else:
            logger.error(r.text)
            raise Exception("Unable to get server information, check your platform settings")

    @classmethod
    def reindex(cls, object_type, ref):
        """

        Args:
          object_type:
          ref:

        Returns:

        """
        object_type, object_type_metadata = resolve_object_type(object_type)
        print(f"Reindexing {object_type_metadata['name']} [bold]{ref}[/bold]")
        url_ref = ref.replace(':', '/')
        r = requests.post(f"{KodexaPlatform.get_url()}/api/{object_type}/{url_ref}/_reindex",
                          headers={"x-access-token": KodexaPlatform.get_access_token(),
                                   "content-type": "application/json"})
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        elif r.status_code == 200:
            return r.text
        else:
            logger.error(r.text)
            raise Exception("Unable to reindex check your reference and platform settings")


class RemoteSession:
    """A Session on the Kodexa platform for leveraging pipelines and services"""

    def __init__(self, session_type, slug):
        self.session_type = session_type
        self.slug = slug
        self.cloud_session = None

    def get_action_metadata(self, ref):
        """

        Args:
          ref:

        Returns:

        """
        logger.debug(f"Downloading metadata for action {ref}")
        r = requests.get(f"{KodexaPlatform.get_url()}/api/actions/{ref.replace(':', '/')}",
                         headers={"x-access-token": KodexaPlatform.get_access_token()})
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        elif r.status_code == 200:
            return r.json()
        else:
            logger.error(r.text)
            raise Exception("Unable to get action metadata, check your reference and platform settings")

    def start(self):
        """ """
        logger.info(f"Creating session {self.slug} ({KodexaPlatform.get_url()})")
        r = requests.post(f"{KodexaPlatform.get_url()}/api/sessions", params={self.session_type: self.slug},
                          headers={"x-access-token": KodexaPlatform.get_access_token()})

        if r.status_code != 200:
            logger.error("Unable to create session")
            logger.error(r.text)
            raise Exception("Unable to create a session, check your URL and access token")

        self.cloud_session = Dict(json.loads(r.text))

    def execution_action(self, document, options, attach_source, context):
        """

        Args:
          document:
          options:
          attach_source:
          context:

        Returns:

        """
        files = {}
        if attach_source:
            logger.debug("Attaching source to call")
            files["file"] = get_source(document)
            files["file_document"] = document.to_kddb()
        else:
            files["document"] = document.to_kddb()

        data = {"options": json.dumps(options), "document_metadata_json": json.dumps(document.metadata),
                "context": json.dumps(context.context)}

        logger.info(f"Executing session {self.cloud_session.id}")
        r = requests.post(f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/execute",
                          params={self.session_type: self.slug, "documentVersion": document.version},
                          data=data,
                          headers={"x-access-token": KodexaPlatform.get_access_token()}, files=files)
        try:
            if r.status_code == 200:
                execution = Dict(json.loads(r.text))
            else:
                logger.error("Execution creation failed [" + r.text + "], response " + str(r.status_code))
                raise Exception("Execution creation failed [" + r.text + "], response " + str(r.status_code))
        except JSONDecodeError:
            logger.error("Unable to handle response [" + r.text + "], response " + str(r.status_code))
            raise

        return execution

    def wait_for_execution(self, execution):
        """
        Wait for the remote execution to complete

        Args:
          execution:

        Returns:

        """

        status = execution.status
        while execution.status == "PENDING" or execution.status == "RUNNING":
            r = requests.get(
                f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}",
                headers={"x-access-token": KodexaPlatform.get_access_token()})
            try:
                execution = Dict(json.loads(r.text))
            except JSONDecodeError:
                logger.error("Unable to handle response [" + r.text + "]")
                raise

            if status != execution.status:
                logger.info(f"Status changed from {status} -> {execution.status}")
                status = execution.status

            time.sleep(1)

        if status == "FAILED":
            logger.error("Execution has failed")
            for step in execution.steps:
                if step.status == 'FAILED':
                    logger.error(f"Step {step.name} has failed. {step.exceptionDetails.message}.")

                    if step.exceptionDetails.errorType == 'Validation':
                        logger.error("Additional validation information has been provided:")
                        for validation_error in step.exceptionDetails.validationErrors:
                            logger.error(f"- {validation_error.option} : {validation_error.message}")

                    if step.exceptionDetails.help:
                        logger.error(f"Additional help is available:\n\n{step.exceptionDetails.help}")

            logger.debug(execution)

            raise Exception(f"Processing has failed\nDetails: {step.exceptionDetails.help}")

        return execution

    def get_output_document(self, execution):
        """
        Get the output document from a given execution

        Args:
          execution: the execution holding the document

        Returns:
            the output document (or None if there isn't one)

        """
        if execution.outputId:
            logger.info(f"Downloading output document [{execution.outputId}]")
            doc = requests.get(
                f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}/objects/{execution.outputId}",
                headers={"x-access-token": KodexaPlatform.get_access_token()})
            return Document.from_kddb(doc.content)
        else:
            logger.info("No output document")
            return None

    def get_store(self, execution, store):
        """
        Download a store from an execution

        Args:
          execution: the execution containing the store
          store: the store

        Returns:
            The full store

        """
        logger.debug("Downloading store from server")
        response = requests.get(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}/stores/{store.id}",
            headers={"x-access-token": KodexaPlatform.get_access_token()})
        logger.debug(f"Response from server [{response.text}] [{response.status_code}]")
        raw_store = Dict(response.json())

        return TableDataStore(raw_store.data.columns, raw_store.data.rows)

    def merge_stores(self, execution, context: PipelineContext):
        """
        Merge the stores between an execution and a context

        Args:
          execution:
          context: PipelineContext:

        Returns:

        """
        for store in execution.stores:
            logger.debug(f"Merging store {store.id}")
            context.merge_store(store.name, self.get_store(execution, store))


class RemotePipeline:
    """Allow you to interact with a pipeline that has been deployed to an instance of Kodexa Platform"""

    def __init__(self, slug, connector, version=None, attach_source=True, parameters=None, auth=None):
        logger.info(f"Initializing a new pipeline {slug}")

        if isinstance(connector, Document):
            self.connector = [connector]
        else:
            self.connector = connector
        self.sink = None
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

    def set_sink(self, sink):
        """Set the sink you wish to use, note that it will replace any currently assigned
        sink

        Args:
          sink: the sink for the pipeline

        Returns:

        >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
            >>> pipeline.set_sink(ExampleSink())
        """
        logger.info(f"Setting sink {sink.get_name()} on {self.slug}")
        self.sink = sink

        return self

    def run(self):
        """ """
        self.context.statistics = PipelineStatistics()

        logger.info(f"Starting remote pipeline {self.slug}")
        cloud_session = RemoteSession("pipeline", self.slug)
        cloud_session.start()

        for document in self.connector:
            logger.info(f"Processing {document}")
            execution = cloud_session.execution_action(document, self.parameters, self.attach_source, self.context)
            execution = cloud_session.wait_for_execution(execution)

            logger.info("Capturing output")
            result_document = cloud_session.get_output_document(execution)
            self.context.set_output_document(result_document)
            cloud_session.merge_stores(execution, self.context)

            self.context.statistics.processed_document(result_document)
            self.context.context = execution.context
            if self.sink:
                logger.info(f"Writing to sink {self.sink.get_name()}")
                try:
                    self.sink.sink(result_document)
                except:
                    if document:
                        document.exceptions.append({
                            "step": self.sink.get_name(),
                            "exception": sys.exc_info()[0]
                        })
                    if self.context.stop_on_exception:
                        raise

        logger.info(f"Completed pipeline {self.slug}")

        return self.context

    @staticmethod
    def from_url(slug: str, url, headers=None, *args, **kwargs) -> RemotePipeline:
        """Build a new pipeline with the input being a document created from the given URL

        Args:
          slug: The slug for the remote pipeline
          url: The URL ie. https://www.google.com
          headers: A dictionary of headers (Default value = None)
          slug: str:
          *args:
          **kwargs:

        Returns:
          A new instance of a remote pipeline

        """
        return RemotePipeline(slug, Document.from_url(url, headers), *args, **kwargs)

    @staticmethod
    def from_file(slug: str, file_path: str, unpack: bool = False, *args, **kwargs) -> RemotePipeline:
        """Create a new pipeline using a file path as a source

        Args:
          slug: The slug for the remote pipeline
          file_path: The path to the file
          unpack: Unpack the file as a KDXA
          slug: str:
          file_path: str:
          unpack: bool:  (Default value = False)
          *args:
          **kwargs:

        Returns:
          Pipeline: A new pipeline

        """
        return RemotePipeline(slug, Document.from_file(file_path, unpack), *args, **kwargs)

    @staticmethod
    def from_text(slug: str, text: str, *args, **kwargs) -> RemotePipeline:
        """Build a new pipeline and provide text as the basic to create a document

        Args:
          slug: The slug for the remote pipeline
          text: Text to use to create document
          slug: str:
          text: str:
          *args:
          **kwargs:

        Returns:
          RemotePipeline: A new pipeline

        """

        # need to update kwargs for attach_source
        kwargs.setdefault('attach_source', False)
        return RemotePipeline(slug, Document.from_text(text), *args, **kwargs)

    @staticmethod
    def from_folder(slug: str, folder_path: str, filename_filter: str = "*", recursive: bool = False,
                    unpack: bool = False,
                    relative: bool = False,
                    caller_path: str = get_caller_dir()) -> RemotePipeline:
        """Create a pipeline that will run against a set of local files from a folder

        Args:
          slug: The slug for the remote pipeline
          folder_path: The folder path
          filename_filter: The filter for filename (i.e. *.pdf)
          recursive: Should we look recursively in sub-directories (default False)
          relative: Is the folder path relative to the caller (default False)
          caller_path: The caller path (defaults to trying to work this out from the stack)
          unpack: Unpack the file as a KDXA document
          slug: str:
          folder_path: str:
          filename_filter: str:  (Default value = "*")
          recursive: bool:  (Default value = False)
          unpack: bool:  (Default value = False)
          relative: bool:  (Default value = False)
          caller_path: str:  (Default value = get_caller_dir())

        Returns:
          RemotePipeline: A new pipeline

        """
        return RemotePipeline(slug, FolderConnector(folder_path, filename_filter, recursive, relative, caller_path,
                                                    unpack=unpack))

    def to_store(self, document_store: DocumentStore, processing_mode: str = "update"):
        """Allows you to provide the sink store easily

        This will wrap the store in a document store sink

        Args:
          document_store: document store to use
          processing_mode: the processing mode (update or new)
          document_store: DocumentStore:
          processing_mode: str:  (Default value = "update")

        Returns:
          the pipeline

        """
        from kodexa.sinks import DocumentStoreSink
        self.set_sink(DocumentStoreSink(document_store))
        return self


class RemoteAction:
    """Allows you to interact with an action that has been deployed in the Kodexa platform"""

    def __init__(self, slug, version=None, attach_source=False, options=None, auth=None):
        if auth is None:
            auth = []
        if options is None:
            options = {}
        self.slug = slug
        self.version = version
        self.attach_source = attach_source
        self.options = options
        self.auth = auth

    def to_dict(self):
        """ """
        return {
            'ref': self.slug,
            'options': self.options
        }

    def get_name(self):
        """ """
        return f"Remote Action ({self.slug})"

    def process(self, document, context):
        """
        Process the remove action

        Args:
          document:
          context:

        Returns:

        """
        cloud_session = RemoteSession("service", self.slug)
        cloud_session.start()

        logger.info(f"Loading metadata for {self.slug}")
        action_metadata = cloud_session.get_action_metadata(self.slug)

        requires_source = False
        if 'requiresSource' in action_metadata['metadata']:
            requires_source = action_metadata['metadata']['requiresSource']

        execution = cloud_session.execution_action(document, self.options,
                                                   self.attach_source if self.attach_source else requires_source,
                                                   context)

        logger.debug("Waiting for remote execution")
        execution = cloud_session.wait_for_execution(execution)

        logger.debug("Downloading the result document")
        result_document = cloud_session.get_output_document(execution)

        logger.debug("Set the context to match the context from the execution")
        context.context = execution.context

        logger.debug("Merge the stores from the execution back into the context")
        cloud_session.merge_stores(execution, context)

        return result_document if result_document else document

    def end_processing(self, pipeline_context: PipelineContext):
        """ """

        # TODO not yet implemented for remote steps
        pass

    def to_configuration(self):
        """Returns a dictionary representing the configuration information for the step

        :return: dictionary representing the configuration of the step

        Args:

        Returns:

        """
        return {
            "ref": self.slug,
            "options": self.options
        }


class ExtensionHelper:
    """ """

    @staticmethod
    def load_metadata(path):
        """

        Args:
          path:

        Returns:

        """

        if os.path.exists(os.path.join(path, 'dharma.json')):
            dharma_metadata_file = open(os.path.join(path, 'dharma.json'))
            dharma_metadata = Dict(json.loads(dharma_metadata_file.read()))
        elif os.path.exists(os.path.join(path, 'dharma.yml')):
            dharma_metadata_file = open(os.path.join(path, 'dharma.yml'))
            dharma_metadata = Dict(yaml.safe_load(dharma_metadata_file.read()))
        elif os.path.exists(os.path.join(path, 'kodexa.yml')):
            dharma_metadata_file = open(os.path.join(path, 'kodexa.yml'))
            dharma_metadata = Dict(yaml.safe_load(dharma_metadata_file.read()))
        else:
            raise Exception("Unable to find a kodexa.yml file describing your extension")
        return dharma_metadata
