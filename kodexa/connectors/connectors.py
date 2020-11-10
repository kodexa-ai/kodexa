import fnmatch
import inspect
import io
import logging
import mimetypes
import os
import tempfile
import urllib
from os.path import join
from typing import Dict, Type

import requests

from kodexa.model import Document, DocumentMetadata, DocumentStore

logger = logging.getLogger('kodexa.connectors')


def get_caller_dir():
    # get the caller's stack frame and extract its file path
    frame_info = inspect.stack()[3]
    filepath = frame_info.filename
    del frame_info  # drop the reference to the stack frame to avoid reference cycles

    # make the path absolute (optional)
    filepath = os.path.dirname(os.path.abspath(filepath))
    return filepath


class FolderConnector:

    @staticmethod
    def get_name():
        return "folder"

    def __init__(self, path, file_filter="*", recursive=False, relative=False, caller_path=get_caller_dir(),
                 unpack=False):
        self.path = path
        self.file_filter = file_filter
        self.recursive = recursive
        self.relative = relative
        self.caller_path = caller_path
        self.unpack = unpack

        if not self.path:
            raise ValueError('You must provide a path')

        self.files = self.__get_files__()
        self.index = 0

    @staticmethod
    def get_source(document):
        return open(join(document.source.original_path, document.source.original_filename), 'rb')

    def __iter__(self):
        return self

    def __next__(self):
        if self.index > len(self.files) - 1:
            raise StopIteration
        else:
            self.index += 1
            if self.unpack:
                return Document.from_kdxa(self.path)
            else:
                document = Document(DocumentMetadata(
                    {"source_path": self.files[self.index - 1], "connector": self.get_name(),
                     "mime_type": mimetypes.guess_type(self.files[self.index - 1]),
                     "connector_options": {"path": self.path, "file_filter": self.file_filter}}))
                document.source.original_filename = os.path.basename(self.files[self.index - 1])
                document.source.original_path = self.path
                document.source.connector = self.get_name()

                # TODO we need to get the checksum and last_updated and created times
                return document

    def __get_files__(self):
        all_files = []
        base_path = self.path

        if self.relative:
            base_path = os.path.join(self.caller_path, base_path)
        for dp, dn, fn in os.walk(os.path.expanduser(base_path)):
            for f in fn:
                file_name = os.path.join(dp, f)
                if fnmatch.fnmatch(f, self.file_filter):
                    all_files.append(file_name)

            if not self.recursive:
                break

        return all_files


class FileHandleConnector:

    @staticmethod
    def get_name():
        return 'file-handle'

    def __init__(self, original_path):
        self.file = original_path
        self.index = 0
        self.completed = False

    @staticmethod
    def get_source(document):
        return open(document.source.original_path, 'rb')

    def __iter__(self):
        return self

    def __next__(self):
        if self.completed:
            raise StopIteration
        else:
            document = Document(DocumentMetadata(
                {"source_path": self.file, "connector": self.get_name(),
                 "mime_type": mimetypes.guess_type(self.file),
                 "connector_options": {"file": self.file}}))
            document.source.original_filename = self.file
            document.source.original_path = os.path.basename(self.file)
            document.source.connector = self.get_name()

            # TODO we need to get the checksum and last_updated and created times
            return document


class UrlConnector:

    @staticmethod
    def get_name():
        return "url"

    def __init__(self, original_path, headers=None):
        if headers is None:
            headers = {}
        self.url = original_path
        self.headers = headers
        self.index = 0
        self.completed = False

    @staticmethod
    def get_source(document):

        # If we have an http URL then we should use requests, it is much
        # cleaner
        if document.source.original_path.startswith('http'):
            response = requests.get(document.source.original_path,
                                    headers=document.source.headers)
            return io.BytesIO(response.content)
        else:
            if document.source.headers:
                opener = urllib.request.build_opener()
                for header in document.source.headers:
                    opener.addheaders = [(header, document.source.headers[header])]
                urllib.request.install_opener(opener)
            with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
                urllib.request.urlretrieve(document.source.original_path, tmp_file.name)

                return open(tmp_file.name, 'rb')

    def __iter__(self):
        return self

    def __next__(self):
        if self.completed:
            raise StopIteration
        else:
            self.completed = True
            document = Document(DocumentMetadata(
                {"connector": self.get_name(),
                 "connector_options": {"url": self.url, "headers": self.headers}}))
            document.source.connector = self.get_name()
            document.source.original_path = self.url
            document.source.headers = self.headers
            return document


registered_connectors: Dict[str, Type] = {}


def get_connectors():
    return registered_connectors.keys()


def get_connector(connector, options):
    if connector in registered_connectors:
        logger.info(f"Getting registered connector {connector}")
        return registered_connectors[connector]
    else:
        logging.error(f"Unable to find connector {connector}")
        raise Exception(f"Unable to find connector {connector}")


def add_connector(connector):
    registered_connectors[connector.get_name()] = connector


def get_source(document):
    connector = get_connector(document.source.connector,
                              document.source)
    return connector.get_source(document)


class DocumentStoreConnector(object):

    def __init__(self, store: DocumentStore, subscription: str):
        self.store = store
        self.subscription = subscription
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.store.count():
            raise StopIteration
        else:
            uuid_value = self.store.list_objects()[self.index]['uuid']
            self.index += 1
            return self.store.get_by_uuid(uuid_value)


add_connector(FolderConnector)
add_connector(FileHandleConnector)
add_connector(UrlConnector)
