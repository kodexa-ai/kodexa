import json
import logging
import os
import time

import requests
from addict import Dict

from kodexa.connectors import get_source, FileHandleConnector
from kodexa.model import Document
from kodexa.pipeline import PipelineContext
from kodexa.stores import TableDataStore

logger = logging.getLogger('kodexa.cloud')


class KodexaCloudSession:
    """
    A Session on the Kodexa Cloud for leveraging pipelines and services
    """

    def __init__(self, session_type, slug, access_token=None, cloud_url='https://cloud.kodexa.com'):
        self.access_token = access_token if access_token else os.getenv('KODEXA_ACCESS_TOKEN')
        self.session_type = session_type
        self.cloud_url = cloud_url
        self.slug = slug
        self.cloud_session = None

    def start(self):
        r = requests.post(f"{self.cloud_url}/api/sessions", params={self.session_type: self.slug},
                          headers={"x-access-token": self.access_token})

        if r.status_code != 200:
            raise Exception("Unable to create a session, check your URL and access token")
        self.cloud_session = Dict(json.loads(r.text))

    def execute_service(self, document, options, attach_source):
        files = {}
        if attach_source:
            files["file"] = get_source(document)
        else:
            files["document"] = document.to_msgpack()

        data = {"options": json.dumps(options)}

        r = requests.post(f"{self.cloud_url}/api/sessions/{self.cloud_session.id}/execute",
                          params={self.session_type: self.slug},
                          data=data,
                          headers={"x-access-token": self.access_token}, files=files)
        execution = Dict(json.loads(r.text))
        return execution

    def wait_for_execution(self, execution):

        status = execution.status
        while execution.status == "PENDING" or execution.status == "RUNNING":
            r = requests.get(f"{self.cloud_url}/api/sessions/{self.cloud_session.id}/executions/{execution.id}",
                             headers={"x-access-token": self.access_token})
            execution = Dict(json.loads(r.text))
            if status != execution.status:
                logger.info(f"Status changed from {status} -> {execution.status}")
                status = execution.status
            time.sleep(1)

        if status == "FAILED":
            logger.error("Failed to execution in session")
            logger.exception(execution)
            raise Exception("Processing has failed")

        return execution

    def get_output_document(self, execution):
        if execution.outputId:
            doc = requests.get(
                f"{self.cloud_url}/api/sessions/{self.cloud_session.id}/executions/{execution.id}/objects/{execution.outputId}",
                headers={"x-access-token": self.access_token})
            return Document.from_msgpack(doc.content)
        else:
            return None

    def get_store(self, execution, store):
        response = requests.get(
            f"{self.cloud_url}/api/sessions/{self.cloud_session.id}/executions/{execution.id}/stores/{store.id}",
            headers={"x-access-token": self.access_token})
        raw_store = Dict(json.loads(response.text))
        return TableDataStore(raw_store.columns, raw_store.rows)

    def merge_stores(self, execution, context):
        for store in execution.stores:
            context.add_store(store.name, self.get_store(execution, store))


class KodexaCloudPipeline:
    """
    Allow you to interact with a pipeline that has been deployed in the Kodexa Cloud
    """

    def __init__(self, slug, version=None, attach_source=True, options=None, auth=None,
                 cloud_url='https://cloud.kodexa.com', access_token=None):
        if auth is None:
            auth = []
        if options is None:
            options = {}
        self.slug = slug
        self.version = version
        self.attach_source = attach_source
        self.options = options
        self.auth = auth
        self.cloud_url = cloud_url
        self.access_token = access_token

    def execute(self, input):
        cloud_session = KodexaCloudSession("pipeline", self.slug, self.access_token, self.cloud_url)
        cloud_session.start()

        if isinstance(input, Document):
            document = input
        else:
            connector = FileHandleConnector(input)
            document = connector.__next__()
        context = PipelineContext()
        execution = cloud_session.execute_service(document, self.options, self.attach_source)
        execution = cloud_session.wait_for_execution(execution)

        result_document = cloud_session.get_output_document(execution)
        context.set_output_document(result_document)
        cloud_session.merge_stores(execution, context)

        return context


class KodexaCloudService:
    """
    Allows you to interact with a content service that has been deployed in the Kodexa cloud
    """

    def __init__(self, slug, version=None, attach_source=False, options={}, auth=[],
                 cloud_url='https://cloud.kodexa.com', access_token=None):
        self.slug = slug
        self.version = version
        self.attach_source = attach_source
        self.options = options
        self.auth = auth
        self.cloud_url = cloud_url
        self.access_token = access_token

    def get_name(self):
        return f"Kodexa Service ({self.slug})"

    def process(self, document, context):
        cloud_session = KodexaCloudSession("service", self.slug, self.access_token, self.cloud_url)
        cloud_session.start()
        execution = cloud_session.execute_service(document, self.options, self.attach_source)
        execution = cloud_session.wait_for_execution(execution)

        result_document = cloud_session.get_output_document(execution)
        cloud_session.merge_stores(execution, context)

        return result_document if result_document else document
