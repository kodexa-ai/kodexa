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
import sys
import time
from json import JSONDecodeError
from pprint import pprint

import better_exceptions
import jsonpickle
import requests
import yaml
from addict import Dict
from appdirs import AppDirs
from functional import seq
from rich import print, get_console

from kodexa.connectors import get_source
from kodexa.connectors.connectors import get_caller_dir, FolderConnector
from kodexa.model import Document, ExtensionPack, ModelStore, DocumentStore
from kodexa.model.objects import AssistantDefinition, Action, Taxonomy, ModelRuntime, Credential, ExecutionEvent, \
    ContentObject, AssistantEvent, ContentEvent, ScheduledEvent, Project, Execution, ProjectTemplate, Membership, \
    DataForm
from kodexa.pipeline import PipelineContext, Pipeline, PipelineStatistics
from kodexa.platform.client import DocumentStoreEndpoint, KodexaClient
from kodexa.stores import RemoteDocumentStore, RemoteDataStore
from kodexa.stores import TableDataStore, RemoteModelStore, LocalDocumentStore, LocalModelStore

logger = logging.getLogger()

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
          pipeline_metadata: Dict: The dictionary that will hold the metadata representation of the pipeline

        Returns: The updated pipeline_metadata

        """
        pipeline_metadata.metadata.steps = []
        pipeline_metadata.metadata.stores = []

        for pipeline_store in self.pipeline.stores:

            if isinstance(pipeline_store.store, RemoteDocumentStore):
                pipeline_metadata.metadata.stores.append(
                    {"name": pipeline_store.name, "ref": pipeline_store.store.ref, "storeType": "DOCUMENT"})
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
        'ref',
        'name',
        'description',
        'type',
        'status'
    ],
    'projects': [
        'id',
        'organization.name',
        'name',
        'description'
    ],
    'assistants': [
        'ref',
        'name',
        'description',
        'template'
    ],
    'executions': [
        'id',
        'startDate',
        'endDate',
        'status',
        'assistant.name',
        'documentFamily.path'
    ],
    'memberships': [
        'organization.slug',
        'organization.name'
    ],

    'stores': [
        'ref',
        'name',
        'description',
        'storeType',
        'storePurpose',
        'template'
    ],
    'default': [
        'ref',
        'name',
        'description',
        'type',
        'template'
    ]
}

OBJECT_TYPES = {
    "extensionPacks": {
        "name": "extension pack",
        "plural": "extension packs",
        "type": ExtensionPack
    },
    "pipelines": {
        "name": "pipeline",
        "plural": "pipelines",
        "type": Pipeline
    },
    "assistants": {
        "name": "assistant",
        "plural": "assistants",
        "type": AssistantDefinition
    },
    "actions": {
        "name": "action",
        "plural": "actions",
        "type": Action
    },
    "modelRuntimes": {
        "name": "modelRuntime",
        "plural": "modelRuntimes",
        "type": ModelRuntime
    },
    "credentials": {
        "name": "credential",
        "plural": "credentials",
        "type": Credential
    },
    "dataForms": {
        "name": "dataForm",
        "plural": "dataForms",
        "type": DataForm
    },
    "taxonomies": {
        "name": "taxonomy",
        "plural": "taxonomies",
        "type": Taxonomy
    },
    "stores": {
        "name": "store",
        "plural": "stores"
    },
    "projects": {
        "name": "project",
        "plural": "projects",
        "type": Project,
        "global": True
    },
    "projectTemplates": {
        "name": "projectTemplate",
        "plural": "projectTemplates",
        "type": ProjectTemplate
    },
    "executions": {
        "name": "execution",
        "plural": "executions",
        "type": Execution,
        "global": True,
        "sort": "startDate:desc"
    },
    "memberships": {
        "name": "membership",
        "plural": "memberships",
        "type": Membership,
        "global": True
    }
}


def resolve_object_type(obj_type):
    """Takes part of an object type (ie. pipeline) and then resolves the object type (pipelines)

    Args:
      obj_type: part of the object type

    Returns:
      The object type dict (if found)

    """
    hits = []
    keys = []

    if not isinstance(obj_type, str):
        obj_type = str(obj_type).lower()

    for target_type in OBJECT_TYPES.keys():
        if obj_type in target_type:
            hits.append(OBJECT_TYPES[target_type])
            keys.append(target_type)

    if len(hits) == 1:
        return keys[0], hits[0]

    if len(hits) == 0:
        print(f":exclaimation: Unable to find object type {obj_type}")
        sys.exit(1)
    else:
        print(f":exclaimation: To many potential matches for object type ({','.join(keys)}")
        sys.exit(1)


class KodexaPlatform:
    """
    The KodexaPlatform object allows you to work with an instance of the Kodexa platform, allow you to list, view and deploy
    components

    Note it also can be used to get your access token and Kodexa platform URL using:

    * A user config file if available
    * Environment variables (KODEXA_ACCESS_TOKEN and KODEXA_URL)

    """

    @staticmethod
    def get_client():
        from kodexa import KodexaClient
        return KodexaClient(KodexaPlatform.get_url(), KodexaPlatform.get_access_token())

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

        The URL should be in the form https://my-company.kodexa.ai

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

        if response.status_code == 404:
            raise Exception("Unable to find access token")

        raise Exception("An error occurred connecting to the Kodexa platform")

    @classmethod
    def deploy_extension(cls, metadata):
        response = requests.post(f"{KodexaPlatform.get_url()}/api/extensionPacks/{metadata['orgSlug']}",
                                 json=metadata.to_dict(),
                                 headers={"x-access-token": KodexaPlatform.get_access_token(),
                                          "content-type": "application/json"})
        if response.status_code == 200:
            logger.info("Extension deployed")
        else:
            logger.warning(response.text)
            raise Exception("Unable to deploy new extension")

    @staticmethod
    def deploy_extension_from_uri(path, organisation_slug):
        url = f"{KodexaPlatform.get_url()}/api/extensionPacks/{organisation_slug}?uri={path}"
        logger.info(f"Publishing extension pack to organization {organisation_slug}")
        response = requests.post(url,
                                 headers={"x-access-token": KodexaPlatform.get_access_token(),
                                          "content-type": "application/json"})
        if response.status_code == 200:
            logger.info("Extension deployed")
        else:
            logger.warning(response.text)
            raise Exception("Unable to deploy new extension")

    @staticmethod
    def resolve_ref(ref: str):

        org_slug = ref.split('/')[0]
        slug = ref.split('/')[1].split(":")[0]

        version = None

        if len(ref.split('/')[1].split(":")) == 2:
            version = ref.split('/')[1].split(":")[1]

        return [org_slug, slug, version]

    @staticmethod
    def __build_object(ref, object_type_metadata, object_class):
        from kodexa import KodexaPlatform
        url = f"{KodexaPlatform.get_url()}/api/{object_type_metadata['plural']}/{ref.replace(':', '/')}"
        import requests
        response = requests.get(url,
                                headers={"x-access-token": KodexaPlatform.get_access_token(),
                                         "content-type": "application/json"})

        if response.status_code == 200:
            return object_class(**response.json())
        if response.status_code == 404:
            return None

        raise Exception(
            f"Unable to create {object_type_metadata['plural']} with ref {ref} [{response.status_code} {response.text}]")

    @staticmethod
    def get_object_instance(ref: str, object_type):
        object_type, object_type_metadata = resolve_object_type(object_type)

        if 'type' in object_type_metadata:
            return KodexaPlatform.__build_object(ref, object_type_metadata, object_type_metadata['type'])

        if object_type == 'stores':
            # We need to work out what type of store we have
            return KodexaPlatform.get_object(ref, object_type)

        # TODO - there are other things we need?
        raise Exception(f"Unable to get a local instance of {ref} of type {object_type}")

    @staticmethod
    def deploy(ref: str, kodexa_object, name: str = None, description: str = None,
               options=None, public=False, force_replace=False, dry_run=False, print_yaml=False):

        if '/' not in ref:
            logger.warning("A ref must be valid, i.e. org_slug/pipeline_slug:version")
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

        from kodexa import RemoteDataStore

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

        elif isinstance(kodexa_object, DocumentStore):
            object_url = 'stores'
            metadata_object.name = 'New Store' if kodexa_object.name is None else kodexa_object.name
            metadata_object.description = 'A document store' if kodexa_object.description is None else kodexa_object.description
            metadata_object.type = 'store'
            metadata_object.storeType = 'DOCUMENT'
        elif isinstance(kodexa_object, ModelStore):
            object_url = 'stores'
            metadata_object.name = 'New Store' if kodexa_object.name is None else kodexa_object.name
            metadata_object.description = 'A model store' if kodexa_object.description is None else kodexa_object.description
            metadata_object.type = 'store'
            metadata_object.storeType = 'MODEL'
        elif isinstance(kodexa_object, RemoteDataStore):
            object_url = 'stores'
            metadata_object.name = 'New Store' if kodexa_object.name is None else kodexa_object.name
            metadata_object.description = 'A table data store' if kodexa_object.description is None else kodexa_object.description
            metadata_object.type = 'store'
            metadata_object.storeType = 'TABLE'
        elif isinstance(kodexa_object, Taxonomy):
            metadata_object.name = 'New Taxonomy' if kodexa_object.name is None else kodexa_object.name
            metadata_object.description = 'A new taxonomy' if kodexa_object.description is None else kodexa_object.description
            object_url = 'taxonomies'
            metadata_object.type = 'taxonomy'
            metadata_object.enabled = kodexa_object.enabled
            metadata_object.taxonomyType = kodexa_object.taxonomy_type
            metadata_object.taxons = jsonpickle.decode(
                jsonpickle.encode([taxon.to_dict() for taxon in kodexa_object.taxons], unpicklable=False))
        elif isinstance(kodexa_object, AssistantDefinition):
            metadata_object.name = 'New Assistant Definition' if kodexa_object.name is None else kodexa_object.name
            metadata_object.description = 'A new assistant definition' if kodexa_object.description is None else kodexa_object.description
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

            if object_version:
                url = f"{KodexaPlatform.get_url()}/api/{object_url}/{organization_slug}/{object_slug}/{object_version}"
            else:
                url = f"{KodexaPlatform.get_url()}/api/{object_url}/{organization_slug}/{object_slug}"

            response = requests.get(url,
                                    headers={"x-access-token": KodexaPlatform.get_access_token(),
                                             "content-type": "application/json"})

            if response.status_code == 401:
                logger.warning(f"You do not have the permissions to access this {metadata_object.type}")
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
                    logger.warning(response.text)
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
                        logger.warning(response.text)
                        raise Exception("Unable to deploy and replace")
                else:
                    logger.warning("Not updating")
                    return
            else:
                logger.warning("Unable to deploy")
                logger.warning(response.content)

        return metadata_object

    @staticmethod
    def list_objects(organization_slug, object_type, query="*", page=1, pagesize=10, sort=None):

        url = f"{KodexaPlatform.get_url()}/api/{object_type}/{organization_slug}" if organization_slug else f"{KodexaPlatform.get_url()}/api/{object_type}"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort

        list_response = requests.get(url,
                                     params=params,
                                     headers={"x-access-token": KodexaPlatform.get_access_token(),
                                              "content-type": "application/json"})
        if list_response.status_code == 200:
            return list_response.json()

        logger.warning(list_response.text)
        raise Exception("Unable to list objects [" + list_response.text + "]")

    @staticmethod
    def undeploy(object_type: str, ref: str):
        object_type, object_type_metadata = resolve_object_type(object_type)

        url_ref = ref.replace(':', '/')
        response = requests.delete(f"{KodexaPlatform.get_url()}/api/{object_type_metadata['plural']}/{url_ref}",
                                   headers={"x-access-token": KodexaPlatform.get_access_token(),
                                            "content-type": "application/json"})
        if response.status_code == 200:
            logger.info(f"Undeployed {object_type_metadata['name']} {ref}")
        else:
            logger.warning(response.text)
            raise Exception(f"Unable to undeploy {object_type_metadata['name']} {ref}")

    @staticmethod
    def delete_object(ref, object_type):
        # Generate a URL ref
        object_type, object_type_metadata = resolve_object_type(object_type)
        url_ref = ref.replace(':', '/')
        delete_response = requests.delete(f"{KodexaPlatform.get_url()}/api/{object_type}/{url_ref}",
                                          headers={"x-access-token": KodexaPlatform.get_access_token(),
                                                   "content-type": "application/json"})
        if delete_response.status_code != 200:
            logger.warning(delete_response.text)
            raise Exception(f"Unable to delete object {ref}")

    @staticmethod
    def get_object(ref, object_type):
        object_type, object_type_metadata = resolve_object_type(object_type)
        url_ref = ref.replace(':', '/')
        obj_response = requests.get(f"{KodexaPlatform.get_url()}/api/{object_type}/{url_ref}",
                                    headers={"x-access-token": KodexaPlatform.get_access_token(),
                                             "content-type": "application/json"})

        if obj_response.status_code == 404:
            logger.info(f"Object {ref} not found")
            return None
        if obj_response.status_code != 200:
            logger.warning(obj_response.text)
            raise Exception(f"Unable to get object {ref}")

        obj_json = obj_response.json()
        if obj_json is None:
            return None
        if 'type' in object_type_metadata:
            return object_type_metadata['type'].parse_obj(obj_json)
        if object_type == 'stores':
            if obj_json['storeType'] == 'TABLE':
                return KodexaPlatform.__build_object(ref, object_type_metadata, RemoteDataStore)
            if obj_json['storeType'] == 'DOCUMENT':
                return KodexaPlatform.__build_object(ref, object_type_metadata, RemoteDocumentStore)
            if obj_json['storeType'] == 'MODEL':
                return KodexaPlatform.__build_object(ref, object_type_metadata, RemoteModelStore)
        else:
            print("errr")
            return obj_json

    @classmethod
    def executions(cls):
        obj_response = requests.get(f"{KodexaPlatform.get_url()}/api/executions",
                                    headers={"content-type": "application/json",
                                             "x-access-token": KodexaPlatform.get_access_token()})

        if obj_response.status_code == 200:
            print("\n")
            from rich.table import Table

            table = Table(title=f"Listing Executions")

            cols = ['id', 'startDate', 'endDate', 'status', 'name', 'description']
            for col in cols:
                table.add_column(col)
            for object_dict in obj_response.json()['content']:
                row = []

                for col in cols:
                    row.append(object_dict[col] if col in object_dict else '')
                table.add_row(*row)

            print(table)
        else:
            print(f"Check your URL and password [{obj_response.status_code}]")

    @classmethod
    def get_project_resource(cls, resource_id, resource_name, resource_type):
        obj_response = requests.get(f"{KodexaPlatform.get_url()}/api/projects/{resource_id}/{resource_name}",
                                    headers={"content-type": "application/json",
                                             "x-access-token": KodexaPlatform.get_access_token()})

        if obj_response.status_code == 200:
            cls.__print_table(obj_response.json(), resource_type, False, False)
        else:
            print(f"Check your URL and password [{obj_response.status_code}]")

    @classmethod
    def projects(cls):
        obj_response = requests.get(f"{KodexaPlatform.get_url()}/api/projects",
                                    headers={"content-type": "application/json",
                                             "x-access-token": KodexaPlatform.get_access_token()})

        if obj_response.status_code == 200:
            print("\n")
            from rich.table import Table

            table = Table(title=f"Listing Projects")

            cols = ['id', 'organization.slug', 'name', 'description']
            for col in cols:
                table.add_column(col)
            for object_dict in obj_response.json()['content']:
                row = []

                for col in cols:
                    row.append(object_dict[col] if col in object_dict else '')
                table.add_row(*row)

            print(table)
        else:
            print(f"Check your URL and password [{obj_response.status_code}]")

    @classmethod
    def apply(cls, obj, org_slug=None):

        object_type, object_type_metadata = resolve_object_type(obj['type'])

        if 'global' not in object_type_metadata and not org_slug:
            print(":fire: You must provide an organization slug for this type of resource")
            return

        url_ref = f"{org_slug}/{obj['slug']}" if 'global' not in object_type_metadata else f"{object_type}/{obj['id']}"

        existing = KodexaPlatform.get_object(url_ref, object_type)
        if existing is not None:

            obj_response = requests.put(f"{KodexaPlatform.get_url()}/api/{object_type}/{url_ref}",
                                        json=obj,
                                        headers={"x-access-token": KodexaPlatform.get_access_token(),
                                                 "content-type": "application/json"})
        else:
            obj_response = requests.post(f"{KodexaPlatform.get_url()}/api/{object_type}/{url_ref.split('/')[0]}",
                                         json=obj,
                                         headers={"x-access-token": KodexaPlatform.get_access_token(),
                                                  "content-type": "application/json"})
        if obj_response.status_code != 200:
            logger.warning(obj_response.text)
            raise Exception(f"Unable to {'update' if existing is not None else 'create'} object {url_ref}")

        obj_json = obj_response.json()
        if 'type' in object_type_metadata:
            return object_type_metadata['type'].parse_obj(obj_json)

        return obj_json

    @classmethod
    def get(cls, object_type, ref, path=None, output_format=None, query="*", page: int = 1, pagesize: int = 10,
            sort: str = None):

        object_type, object_type_metadata = resolve_object_type(object_type)

        if sort is None and 'sort' in object_type_metadata:
            sort = object_type_metadata['sort']

        if 'global' not in object_type_metadata and not ref:
            print(":fire: You must provide a ref for this type of resource")
            return

        try:

            # If ref is just the org then we will list them
            if ref and ('/' in ref or 'global' in object_type_metadata):
                obj = KodexaPlatform.get_object(ref, object_type)

                if obj is None:
                    print(f":fire: Unable to find {object_type_metadata['name']} {ref}")
                    return

                if path is not None:
                    import jq
                    obj = jq.compile(path).input(obj).all()
                import yaml
                if output_format == 'yaml':
                    def represent_none(self, _):
                        return self.represent_scalar('tag:yaml.org,2002:null', '')

                    yaml.add_representer(type(None), represent_none)

                    print(yaml.dump(obj.dict(by_alias=True)))
                elif output_format == 'json':
                    print(obj.json(by_alias=True, indent=4))
                else:
                    pprint(obj)

            else:
                objects = KodexaPlatform.list_objects(ref, object_type, query, page, pagesize, sort)
                cls.__print_table(objects, object_type)
        except:
            print(f"\n:exclamation: Failed to get {object_type_metadata['name']} [{sys.exc_info()[0]}]")
            print("\n".join(
                better_exceptions.format_exception(*sys.exc_info())))

    @classmethod
    def delete(cls, object_type, ref):
        object_type, object_type_metadata = resolve_object_type(object_type)
        print(f"Deleting {object_type_metadata['name']} [bold]{ref}[/bold]")

        try:
            KodexaPlatform.delete_object(ref, object_type)
            print(f"Deleted {object_type_metadata['name']} [bold]{ref}[/bold] :tada:")
        except:
            print(f"\n:exclamation: Failed to delete {object_type_metadata['name']} [{sys.exc_info()[0]}]")

    @classmethod
    def login(cls, kodexa_url, username, password):
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
        if r.status_code == 200:
            return r.json()

        logger.warning(r.text)
        raise Exception("Unable to get server information, check your platform settings")

    @classmethod
    def reindex(cls, object_type):
        object_type, object_type_metadata = resolve_object_type(object_type)
        print(f"Reindexing {object_type_metadata['name']}")
        r = requests.post(f"{KodexaPlatform.get_url()}/api/{object_type}/_reindex",
                          headers={"x-access-token": KodexaPlatform.get_access_token(),
                                   "content-type": "application/json"})
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        if r.status_code == 200:
            return r.text

        logger.warning(r.text)
        raise Exception("Unable to reindex check your reference and platform settings")

    @classmethod
    def get_tempdir(cls):
        import tempfile
        return os.getenv('KODEXA_TMP', tempfile.gettempdir())

    @classmethod
    def query(cls, ref, query, download=False, page=1, page_size=10, sort=None, download_native=False):

        client = KodexaClient(KodexaPlatform.get_url(), KodexaPlatform.get_access_token())
        store = client.get_object_by_ref('store', ref)

        if isinstance(store, DocumentStoreEndpoint):
            if download:
                page_document_families = store.query(query, page=page, page_size=page_size, sort=sort)
                for family_endpoint in page_document_families.content:
                    print(f"Downloading {family_endpoint.path}")
                    import os
                    file_path = os.path.splitext(family_endpoint.path)[0] + '.kddb'
                    directory = os.path.dirname(file_path)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    family_endpoint.get_document().to_kddb(file_path)
            if download_native:
                page_document_families = store.query(query, page=page, page_size=page_size, sort=sort)
                for family_endpoint in page_document_families.content:
                    print(f"Downloading {family_endpoint.path}")
                    import os
                    file_path = family_endpoint.path
                    directory = os.path.dirname(file_path)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    with open(file_path, 'wb') as f:
                        f.write(family_endpoint.get_native())
            else:
                print("\n")
                from rich.table import Table

                table = Table(title=f"Listing Documents")

                cols = ['id', 'path', 'labels', 'document_status', 'assignments', 'mixins', 'locked', 'created']
                for col in cols:
                    table.add_column(col)

                def format_col(col, value):
                    if col == 'labels':
                        return ", ".join(seq(value).map(lambda x: x.label).to_list())

                    return str(value)

                page_document_families = store.query(query, page=page, page_size=page_size, sort=sort)
                for family_endpoint in page_document_families.content:
                    row = []
                    for col in cols:
                        row.append(format_col(col, getattr(family_endpoint, col)))
                    table.add_row(*row)

                print(table)

                print(f"Total Matching Documents: {page_document_families.total_elements}")

    @classmethod
    def logs(cls, execution_id):
        r = requests.get(f"{KodexaPlatform.get_url()}/api/executions/{execution_id}/logs",
                         params={"page": 1, "pageSize": 10000, "sort": "logDate:asc"},
                         headers={"x-access-token": KodexaPlatform.get_access_token(),
                                  "content-type": "application/json"})
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        if r.status_code == 200:
            for entry in r.json()['content']:
                get_console().print(entry['entry'], end='', markup=False)
        else:
            logger.warning(r.text)
            raise Exception("Unable to reindex check your reference and platform settings")

    @classmethod
    def upload_file(cls, ref, path):
        store = KodexaPlatform.get_object_instance(ref, 'store')

        if isinstance(store, RemoteDocumentStore):
            with open(path, 'rb') as content:
                store.put_native(path, content)
        else:
            raise Exception("Reference must be a document store")

    @classmethod
    def get_project(cls, project_id):
        project_instance = cls.get_object_instance(project_id, 'project')
        print(f"Name: [bold]{project_instance.name}[/bold]")
        print(f"Description: [bold]{project_instance.description}[/bold]\n")

        print("[bold]Document Stores[/bold]")
        cls.get_project_resource(project_id, 'documentStores', 'stores')
        print("[bold]Data Stores[/bold]")
        cls.get_project_resource(project_id, 'dataStores', 'stores')
        print("[bold]Content Taxonomies[/bold]")
        cls.get_project_resource(project_id, 'contentTaxonomies', 'taxonomies')
        print("[bold]Assistants[/bold]")
        cls.get_project_resource(project_id, 'assistants', 'assistants')

    @classmethod
    def __print_table(cls, objects, object_type, title=True, show_count=True):
        cols = DEFAULT_COLUMNS['default']

        object_type, object_type_metadata = resolve_object_type(object_type)

        if object_type in DEFAULT_COLUMNS:
            cols = DEFAULT_COLUMNS[object_type]

        from rich.table import Table

        table = Table(title=f"Listing {object_type_metadata['plural']}" if title else None)
        for col in cols:
            table.add_column(col)

        if 'content' in objects:
            hits = objects['content']
        else:
            hits = objects

        for object_dict in hits:
            row = []

            for col in cols:
                from simpleeval import simple_eval
                from simpleeval import AttributeDoesNotExist
                try:
                    row.append(str(simple_eval('object.' + col, names={'object': object_dict})))
                except AttributeDoesNotExist:
                    row.append("")
            table.add_row(*row)

        print(table)

        if 'content' in objects and show_count:
            print(
                f"\n{objects['totalElements']} {object_type_metadata['plural']} found, page {objects['number'] + 1} of {objects['totalPages']}")

    @classmethod
    def send_event(cls, project_id, assistant_id, obj):
        r = requests.post(f"{KodexaPlatform.get_url()}/api/projects/{project_id}/assistants/{assistant_id}/events",
                          data={
                              'eventType': obj['eventType'],
                              'options': json.dumps(obj['options'])
                          },
                          headers={"x-access-token": KodexaPlatform.get_access_token()})
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        if r.status_code == 200:
            print(f"Starting an execution with id {r.json()['id']}")
            return r.json()

        print(r.text)
        raise Exception("Unable to send event")


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
        if r.status_code == 200:
            return r.json()

        logger.warning(r.text)
        raise Exception("Unable to get action metadata, check your reference and platform settings")

    def start(self):
        """ """
        logger.info(f"Creating session {self.slug} ({KodexaPlatform.get_url()})")
        r = requests.post(f"{KodexaPlatform.get_url()}/api/sessions", params={self.session_type: self.slug},
                          headers={"x-access-token": KodexaPlatform.get_access_token()})

        if r.status_code != 200:
            logger.warning("Unable to create session")
            logger.warning(r.text)
            raise Exception("Unable to create a session, check your URL and access token")

        self.cloud_session = Dict(json.loads(r.text))

    def execution_action(self, document, options, attach_source, context):
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
                logger.warning("Execution creation failed [" + r.text + "], response " + str(r.status_code))
                raise Exception("Execution creation failed [" + r.text + "], response " + str(r.status_code))
        except JSONDecodeError:
            logger.warning("Unable to handle response [" + r.text + "], response " + str(r.status_code))
            raise

        return execution

    def wait_for_execution(self, execution):
        status = execution.status
        while execution.status == "PENDING" or execution.status == "RUNNING":
            r = requests.get(
                f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}",
                headers={"x-access-token": KodexaPlatform.get_access_token()})
            try:
                execution = Dict(json.loads(r.text))
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
                if step.status == 'FAILED':
                    logger.warning(f"Step {step.name} has failed. {step.exceptionDetails.message}.")

                    if step.exceptionDetails.errorType == 'Validation':
                        logger.warning("Additional validation information has been provided:")
                        for validation_error in step.exceptionDetails.validationErrors:
                            logger.warning(f"- {validation_error.option} : {validation_error.message}")

                    if step.exceptionDetails.help:
                        logger.warning(f"Additional help is available:\n\n{step.exceptionDetails.help}")

                    raise Exception(f"Processing has failed on step {step.name}")

            raise Exception("Processing has failed, no steps seem to have failed")

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


class RemoteStep:
    """Allows you to interact with a step that has been deployed in the Kodexa platform"""

    def __init__(self, ref, step_type='ACTION', attach_source=False, options=None):
        if options is None:
            options = {}
        self.ref = ref
        self.step_type = step_type
        self.attach_source = attach_source
        self.options = options

    def to_dict(self):
        """ """
        return {
            'ref': self.ref,
            'step_type': self.step_type,
            'options': self.options
        }

    def get_name(self):
        """ """
        return f"Remote Action ({self.ref})"

    def process(self, document, context):
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


class EventHelper:

    def __init__(self, event: ExecutionEvent):
        self.event: ExecutionEvent = event

    @staticmethod
    def get_base_event(event_dict: Dict):
        if event_dict['type'] == 'assistant':
            return AssistantEvent(**event_dict)
        if event_dict['type'] == 'content':
            return ContentEvent(**event_dict)
        if event_dict['type'] == 'scheduled':
            return ScheduledEvent(**event_dict)

        raise f"Unknown event type {event_dict}"

    def log(self, message: str):
        response = requests.post(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/logs",
            json=[
                {'entry': message}
            ],
            headers={'x-access-token': KodexaPlatform.get_access_token()}, timeout=300)
        if response.status_code != 200:
            print(f"Logging failed {response.status_code}", flush=True)

    def get_content_object(self, content_object_id: str):
        logger.info(
            f"Getting content object {content_object_id} in event {self.event.id} in execution {self.event.execution.id}")

        co_response = requests.get(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/objects/{content_object_id}",
            headers={'x-access-token': KodexaPlatform.get_access_token()}, timeout=300)
        if co_response.status_code != 200:
            logger.error(f"Response {co_response.status_code} {co_response.text}")
            raise Exception(f"Unable to find content object {content_object_id} in execution {self.event.execution.id}")
        return io.BytesIO(co_response.content)

    def put_content_object(self, content_object: ContentObject, content) -> ContentObject:
        files = {
            "content": content
        }
        data = {
            "contentObjectJson": json.dumps(content_object.dict(by_alias=True))
        }
        logger.info("Posting back content object to execution object")
        co_response = requests.post(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/objects",
            data=data,
            headers={'x-access-token': KodexaPlatform.get_access_token()},
            files=files, timeout=300)

        if co_response.status_code != 200:
            logger.info("Unable to post back object")
            logger.error(co_response.text)
            raise Exception("Unable to post back content object")

        logger.info("Object posted back")

        return ContentObject.parse_obj(co_response.json())

    def build_pipeline_context(self) -> PipelineContext:
        context = PipelineContext(context={}, content_provider=self,
                                  store_provider=self, execution_id=self.event.execution.id)

        if self.event.store_ref and self.event.document_family_id:
            logger.info("We have storeRef and document family")
            client = KodexaClient()
            rds: DocumentStoreEndpoint = client.get_object_by_ref('store', self.event.store_ref)
            document_family = rds.get_family(self.event.document_family_id)

            context.document_family = document_family
            context.document_store = rds

        return context

    def get_input_document(self, context):
        for content_object in self.event.execution.content_objects:

            if content_object.id == self.event.input_id:
                input_document_bytes = self.get_content_object(self.event.input_id)
                logger.info("Loading KDDB document")
                input_document = Document.from_kddb(input_document_bytes.read())
                logger.info("Loaded KDDB document")
                context.content_object = content_object
                input_document.uuid = context.content_object.id

                if content_object.store_ref is not None:
                    context.document_store = KodexaPlatform.get_object_instance(content_object.store_ref, 'store')

                return input_document


class SessionConnector:
    event_helper = None

    @classmethod
    def get_name(cls):
        return "cloud-content"

    @classmethod
    def get_source(cls, document):
        if cls.event_helper is None:
            raise Exception("The event_helper needs to be set to use this connector")

        logger.info(f"Getting content object {document.source.original_path}")
        return cls.event_helper.get_content_object(document.source.original_path)
