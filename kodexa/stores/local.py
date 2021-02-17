import logging
import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict

import jsonpickle

from kodexa.model import DocumentFamily, DocumentStore, Document, ContentObject, ModelStore, Store
from kodexa.model.document_families import ContentEvent, DocumentRelationship

logger = logging.getLogger('kodexa.stores')


class LocalDocumentStore(DocumentStore):

    def __init__(self, store_path: str, force_initialize: bool = False, mode: str = 'ALL'):

        modes = ['ALL', 'ONLY_NEW']

        if mode not in modes:
            raise Exception(f"LocalDocumentStore mode must be one of {','.join(modes)}")

        self.store_path: str = store_path
        self.index = 0
        self.metastore: List[DocumentFamily] = []
        self.mode = mode
        self.listeners: List = []

        path = Path(store_path)

        if force_initialize and path.exists():
            shutil.rmtree(store_path)

        if path.is_file():
            raise Exception("Unable to load store, since it is pointing to a file?")
        elif not path.exists():
            logger.info(f"Creating new local document store in {store_path}")
            path.mkdir(parents=True)

            # Create an empty index file
            self.metastore = []
            self.write_metastore()

        self.read_metastore()

        logger.info(f"Found {len(self.metastore)} documents in {store_path}")

    def get_name(self):
        return "Local Document Store"

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.metastore):
            raise StopIteration
        content_object = self.metastore[self.index].content_objects[-1]
        document = self.get_document_by_content_object(content_object)

        from kodexa.model.model import ContentObjectReference
        content_object_reference = ContentObjectReference(content_object, self, document, self.metastore[self.index])
        self.index = self.index + 1
        return content_object_reference

    def sink(self, document: Document, context):
        if context.document_family:
            self.put(context.document_family.path, document)
        else:
            if document.source.original_filename is not None:
                self.put(document.source.original_filename, document)

    def get_ref(self) -> str:
        return self.store_path

    def register_listener(self, listener):
        self.listeners.append(listener)

    def notify_listeners(self, content_event: ContentEvent):
        for listener in self.listeners:
            listener.process_event(content_event)

    def to_dict(self):
        return {
            "type": "DOCUMENT",
            "data": {
                "path": self.store_path
            }
        }

    def accept(self, document: Document):
        if self.mode == 'ALL':
            return True
        if self.mode == 'ONLY_NEW':
            return not self.exists(document)

    def read_metastore(self):
        """
        Read the metadata store
        """
        self.metastore: List[Dict] = []
        with open(os.path.join(self.store_path, 'metastore.json')) as f:
            self.metastore = jsonpickle.decode("".join(f.readlines()))

    def write_metastore(self):
        """
        Method to write the JSON store index back to store path
        """
        with open(os.path.join(self.store_path, 'metastore.json'), 'w') as f:
            f.write(jsonpickle.encode(self.metastore))

    def get_by_uuid(self, uuid: str) -> Optional[Document]:
        for family in self.metastore:
            for content_object in family.content_objects:

                if content_object.id == uuid:
                    return Document.from_kdxa(os.path.join(self.store_path, content_object.id) + ".kdxa")
        return None

    def get_by_path(self, path: str) -> Optional[Document]:
        """
        Return the latest document in the family at the given path

        :param path:
        :return:
        """
        for family in self.metastore:
            if family.path == path:
                # TODO we need to get the latest document from the family

                return Document.from_kdxa(os.path.join(self.store_path, family.get_latest_content().id) + ".kdxa")
        return None

    def get_family_by_path(self, path: str) -> Optional[DocumentFamily]:
        for family in self.metastore:
            if family.path == path:
                return family
        return None

    def get_latest_document(self, path: str) -> Optional[Document]:
        for family in self.metastore:
            if family.path == path:
                return self.get_document_by_content_object(family.content_objects[-1])
        return None

    def list_objects(self) -> List[ContentObject]:
        co_list: List[ContentObject] = []
        for family in self.metastore:
            co_list.extend(family.content_objects)

        return co_list

    def count(self) -> int:
        """
        Returns a count of the number of document families

        :return:
        """
        return len(self.metastore)

    def load_kdxa(self, path: str):
        document = Document.from_kdxa(path)
        self.put(document.uuid, document)

    def add_related_document_to_family(self, document_family_id: str, document_relationship: DocumentRelationship,
                                       document: Document):
        self.read_metastore()
        for family in self.metastore:
            if family.id == document_family_id:
                family.add_document(document, document_relationship)

    def get_document_by_content_object(self, content_object: ContentObject) -> Document:
        return Document.from_kdxa(os.path.join(self.store_path, content_object.id) + ".kdxa")

    def put(self, path: str, document: Document):

        # We can only add a document if it doesn't already exist as a family
        if self.get_family_by_path(path) is None:
            new_document_family = DocumentFamily(path, self.get_ref())
            new_event = new_document_family.add_document(document)
            document.to_kdxa(os.path.join(self.store_path, new_event.content_object.id) + ".kdxa")

            self.metastore.append(new_document_family)
            self.write_metastore()

            # Notify the listeners
            self.notify_listeners(new_event)

        return self.get_family_by_path(path)

    def exists(self, document):
        """
        Look to see if we have document with the same original path and original filename

        :param document: document to check
        :return: True if it is already in the document store
        """

        # Lets just work with original_filename?

        for family in self.metastore:
            if document.source.original_filename == family.path:
                return True
        return False


class LocalModelStore(ModelStore):

    def __init__(self, store_path: str, force_initialize=False):
        self.store_path = store_path
        path = Path(store_path)

        if force_initialize and path.exists():
            shutil.rmtree(store_path)

        if path.is_file():
            raise Exception("Unable to load store, since it is pointing to a file?")
        elif not path.exists():
            path.mkdir(parents=True)

    def to_dict(self):
        return {
            "type": "MODEL",
            "data": {
                "path": self.store_path
            }
        }

    def get(self, object_path: str):
        if Path(os.path.join(self.store_path, object_path)).is_file():
            return open(os.path.join(self.store_path, object_path), 'rb')
        else:
            return None

    def put(self, object_path: str, content):
        path = Path(object_path)
        with open(os.path.join(self.store_path, path), 'wb') as object_file:
            object_file.write(content)


class TableDataStore(Store):
    """
    Stores data as a list of lists that can represent a table.

    This is a good store when you are capturing nested or tabular data.

    :param columns: a list of the column names (default to dynamic)
    :param rows: initial set of rows (default to empty)

    """

    def __init__(self, columns=None, rows=None):

        if rows is None:
            rows = []
        if columns is None:
            columns = []
        self.columns: List[str] = columns
        self.rows: List[List] = rows

        from kodexa.pipeline import PipelineContext

        self.pipeline_context: Optional[PipelineContext] = None

    """
    Return the store as a dict for serialization
    """

    def to_dict(self):
        """
        Create a dictionary representing this TableDataStore's structure and content.

            >>> table_data_store.to_dict()

        :return: The properties of this TableDataStore structured as a dictionary.
        :rtype: dict
        """

        return {
            "type": "TABLE",
            "data": {
                "columns": self.columns,
                "rows": self.rows
            }
        }

    def clear(self):
        self.rows = []

    def to_df(self):
        import pandas as pd

        if not self.columns:
            return pd.DataFrame(self.rows)
        else:
            return pd.DataFrame(self.rows, columns=self.columns)

    def set_pipeline_context(self, pipeline_context):
        self.pipeline_context = pipeline_context

    def add(self, row):
        """
        Writes a row to the Data Store

        :param row: the row (as a list) to add
        """
        self.rows.append(row)

    def count(self):
        """
        Returns the number of rows in the store

        :return: number of rows
        """
        return len(self.rows)

    def merge(self, other_store):
        """
        Merge another table store into this store

        :param other_store:
        :return: the other store
        """
        self.rows = self.rows + other_store.rows

    @classmethod
    def from_dict(cls, store_dict):
        return TableDataStore(columns=store_dict['data']['columns'], rows=store_dict['data']['rows'])
