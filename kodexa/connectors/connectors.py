import fnmatch
import logging
import mimetypes
from os import listdir
from os.path import join

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
    connector = get_connector(document.metadata.connector, document.metadata.connector_options)
    return connector.get_source(document)


add_connector(FolderConnector)
