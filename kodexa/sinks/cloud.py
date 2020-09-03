import json
import logging
from json import JSONDecodeError

import requests
from addict import Dict

from kodexa import KodexaPlatform

logger = logging.getLogger('kodexa.sink')


class KodexaPlatformSink:
    """
    A sink to allow you to write documents to a Kodexa Platform instance.

    This will use the token and URL from the KodexaPlatform settings.
    """

    def __init__(self, organization_slug: str, slug: str):
        self.organization_slug = organization_slug
        self.slug = slug

    @staticmethod
    def get_name():
        return "Kodexa Platform Sink"

    def sink(self, document):
        """
        Adds the document to the sink

        :param document: document to add
        """
        files = {"file": document.to_msgpack()}
        content_object_response = requests.post(
            f"{KodexaPlatform.get_url()}/api/stores/{self.organization_slug}/{self.slug}/contents",
            headers={"x-access-token": KodexaPlatform.get_access_token()}, files=files)

        try:
            if content_object_response.status_code == 200:
                content_object = Dict(json.loads(content_object_response.text))
            else:
                logger.error("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
                raise Exception("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
        except JSONDecodeError:
            logger.error("Unable to handle response [" + content_object_response.text + "], response " + str(
                content_object_response.status_code))
            raise
