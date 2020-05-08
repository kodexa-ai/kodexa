import fnmatch
import io
import logging
import mimetypes
import tempfile
import urllib
from os import listdir
from os.path import join

import requests

from kodexa.model import Document, DocumentMetadata


class FolderConnector:

    @staticmethod
    def get_name():
        return "folder"

    def __init__(self, path, file_filter="*"):
        self.path = path
        self.file_filter = file_filter

        if not self.path:
            raise ValueError('You must provide a path')

        self.files = self.__get_files__()
        self.index = 0

    def get_source(self, document):
        return open(join(self.path, document.metadata.source_path), 'rb')

    def __iter__(self):
        return self

    def __next__(self):
        if self.index > len(self.files) - 1:
            raise StopIteration
        else:
            self.index += 1
            return Document(DocumentMetadata(
                {"source_path": self.files[self.index - 1], "connector": self.get_name(),
                 "mime_type": mimetypes.guess_type(self.files[self.index - 1]),
                 "connector_options": {"path": self.path, "file_filter": self.file_filter}}))

    def __get_files__(self):
        return [f for f in listdir(self.path) if
                fnmatch.fnmatch(f, self.file_filter)]


class FileHandleConnector:

    @staticmethod
    def get_name():
        return 'file-handle'

    def __init__(self, file):
        self.file = file
        self.index = 0
        self.completed = False

    def get_source(self, document):
        return open(document.metadata['connector_options']['file'], 'rb')

    def __iter__(self):
        return self

    def __next__(self):
        if self.completed:
            raise StopIteration
        else:
            return Document(DocumentMetadata(
                {"source_path": self.file, "connector": self.get_name(),
                 "mime_type": mimetypes.guess_type(self.file),
                 "connector_options": {"file": self.file}}))


class UrlConnector:

    @staticmethod
    def get_name():
        return "url"

    def __init__(self, url, headers=None):
        if headers is None:
            headers = {}
        self.url = url
        self.headers = headers
        self.index = 0
        self.completed = False

    def get_source(self, document):

        # If we have an http URL then we should use requests, it is much
        # cleaner
        if document.metadata['connector_options']['url'].startswith('http'):
            response = requests.get(document.metadata['connector_options']['url'],
                                    headers=document.metadata['connector_options']['headers'])
            return io.BytesIO(response.content)
        else:
            if 'headers' in document.metadata.connector_options:
                opener = urllib.request.build_opener()
                for header in document.metadata.connector_options.headers:
                    opener.addheaders = [(header, document.metadata['connector_options']['headers'][header])]
                urllib.request.install_opener(opener)
            with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
                urllib.request.urlretrieve(document.metadata['connector_options']['url'], tmp_file.name)

                return open(tmp_file.name, 'rb')

    def __iter__(self):
        return self

    def __next__(self):
        if self.completed:
            raise StopIteration
        else:
            self.completed = True
            return Document(DocumentMetadata(
                {"connector": self.get_name(),
                 "connector_options": {"url": self.url, "headers": self.headers}}))


registered_connectors = {}


def get_connectors():
    return registered_connectors.keys()


def get_connector(connector, options):
    if connector in registered_connectors:
        logging.info("Getting registered connector")
        return registered_connectors[connector](**options)
    else:
        logging.info(f"Unable to find connector {connector}")
        return None


def add_connector(connector):
    registered_connectors[connector.get_name()] = connector


def get_source(document):
    connector = get_connector(document.metadata['connector'],
                              document.metadata[
                                  'connector_options'] if 'connector_options' in document.metadata else {})
    return connector.get_source(document)


add_connector(FolderConnector)
add_connector(FileHandleConnector)
add_connector(UrlConnector)
