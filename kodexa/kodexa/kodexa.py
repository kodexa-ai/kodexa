import json
import os

import msgpack
import requests
from requests.auth import HTTPBasicAuth

from kodexa import get_source, Document


class KodexaService:
    """
    Allows you to interact with a content service that has been deployed in the Kodexa cloud
    """

    def __init__(self, organization, service, version=None, attach_source=False, options={}, auth=[],
                 cloud_url='https://cloud.kodexa.com'):
        self.organization = organization
        self.service = service
        self.version = version
        self.attach_source = attach_source
        self.options = options
        self.auth = auth
        self.cloud_url = cloud_url

    def get_name(self):
        return f"Kodexa Content Service ({self.organization}/{self.service})"

    def process(self, document):
        # We use a very simple approach to get the document to the service

        service_message = {
            "document": document.to_dict(),
            "options": self.options,
            "stores": {}
        }

        upload_files = {}

        data = {
            "options": json.dumps(self.options)
        }

        if self.attach_source:
            upload_files["file"] = get_source(document)
        else:
            upload_files["message"] = msgpack.packb(service_message, use_bin_type=True)

        env_user = os.getenv('KODEXA_USER')
        env_password = os.environ.get('KODEXA_PASSWORD')

        if len(self.auth) == 0 and env_user and env_password:
            self.auth = [env_user, env_password]

        endpoint = f"{self.cloud_url}/api/processing/{self.organization}/{self.service}/upload"

        r = requests.post(endpoint, files=upload_files, data=data, auth=HTTPBasicAuth(self.auth[0], self.auth[1]))
        response_message = json.loads(r.text)
        return Document.from_dict(response_message['document'])
