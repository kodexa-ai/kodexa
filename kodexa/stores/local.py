"""
Local stores implement the API for a store in Kodexa but allow you to work in an offline model.

This is useful for unit testing or working locally.
"""

import logging
import os
import shutil
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import jsonpickle
from pydantic import Field

from kodexa.model import ContentEvent, ContentObject, Document, DocumentFamily, DocumentStore, DocumentTransition, \
    ModelStore, Store
from kodexa.model.objects import ObjectEventType

logger = logging.getLogger()


class LocalDocumentStore(DocumentStore):
    """A Local implementation of a DocumentStore that can be useful for notebooks and development
       but is not for Production use"""

    store_path: Optional[str] = Field(
        None, description='The path to the local storage'
    )

    metastore: Optional[List] = Field(
        None, description='The metadata for the store'
    )

    listeners: Optional[List] = Field(
        None, description='Current local listeners'
    )

    index: Optional[int] = Field(
        None, description='Current index'
    )

    def get_by_content_object_id(self, document_family: DocumentFamily, content_object_id: str) -> Optional[Document]:
        pass

    def delete(self, path: str):
        pass

    def __init__(self, *args, **kwargs):
        if 'slug' not in kwargs:
            kwargs['slug'] = 'local'
        if 'type' not in kwargs:
            kwargs['type'] = 'DOCUMENT'
        if 'name' not in kwargs:
            kwargs['name'] = 'Local Document Store'
        if 'store_ref' not in kwargs:
            kwargs['store_ref'] = 'local/local'
        super().__init__(**kwargs)

        if self.store_path is None:
            from kodexa import KodexaPlatform
            self.store_path = tempfile.mkdtemp(dir=KodexaPlatform.get_tempdir())
            logger.info(f"Creating new local document store in {self.store_path} since no path was provided")

            # Create an empty index file
            self.metastore = []
            self.write_metastore()

        self.index = 0
        self.metastore: List[DocumentFamily] = []
        self.listeners: List = []

        path = Path(self.store_path)

        if kwargs.get('force_initialize', False) and path.exists():
            shutil.rmtree(self.store_path)

        if path.is_file():
            raise Exception("Unable to load store, since it is pointing to a file?")
        elif not path.exists():
            logger.info(f"Creating new local document store in {self.store_path}")
            path.mkdir(parents=True)

            # Create an empty index file
            self.metastore = []
            self.write_metastore()

        self.read_metastore()

        logger.info(f"Found {len(self.metastore)} documents in {self.store_path}")

    def put_native(self, path: str, content: Any, force_replace=False):
        """

        Args:
          path (str): The path to the native file
          content (Any): The content to store
          force_replace (bool): Replace the object in the store
        Returns:

        """

        # In order to store a native document we will first get the family
        # then we will create a content object for the native object
        # and also a content object for the document that references it

        family = self.get_family_by_path(path)

        if family is None:
            family = DocumentFamily(path=path)
            self.metastore.append(family)

        native_content_object = ContentObject(**{'contentType':'NATIVE'})
        native_content_object.id = str(uuid.uuid4()).replace("-", "")
        native_content_object.created_on = datetime.now()
        if family.content_objects is None:
            family.content_objects = []
        family.content_objects.append(native_content_object)
        with open(os.path.join(self.store_path, native_content_object.id), 'wb') as file:
            file.write(content)

        document = Document()
        document.source.connector = "document-store"
        document.source.headers = {"ref": family.store_ref, "family": family.id, "id": native_content_object.id}
        content_event = self.add_document(family, document)
        document.to_kdxa(os.path.join(self.store_path, content_event.content_object.id) + ".kdxa")

    def add_document(self, family, document: Document, transition: Optional[DocumentTransition] = None) -> ContentEvent:
        """

        Args:
          family: DocumentFamily:
          document: Document:
          transition: DocumentTransition:  (Default value = None)

        Returns:
          A new content event
        """
        new_content_object = ContentObject(**{'contentType': 'DOCUMENT'})
        new_content_object.id = str(uuid.uuid4())
        new_content_object.created_on = datetime.now()
        new_content_object.store_ref = family.store_ref
        new_content_object.metadata = document.metadata
        new_content_object.labels = document.labels
        new_content_object.mixins = document.get_mixins()

        if family.content_objects is None:
            family.content_objects = []
        family.content_objects.append(new_content_object)

        if transition is not None:
            transition.destination_content_object_id = new_content_object.id

            if family.transitions is None:
                family.transitions = []

            family.transitions.append(transition)

        new_event = ContentEvent()
        new_event.content_object = new_content_object
        new_event.object_event_type = ObjectEventType.new_object
        new_event.document_family = family
        return new_event

    def get_source_by_content_object(self, document_family: DocumentFamily, content_object: ContentObject) -> \
            Any:
        """
        Get the source for a given content object

        Args:
          document_family (DocumentFamily): the document family
          content_object  (ContentObject): the content object

        Returns:
          the source (or None if not found)

        """
        self.read_metastore()
        family = self.get_family(document_family.id)
        if family is None:
            return None

        return open(os.path.join(self.store_path, content_object.id), 'rb')

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.metastore):
            raise StopIteration
        content_object = self.metastore[self.index].content_objects[-1]
        document = self.get_document_by_content_object(self.metastore[self.index], content_object)

        from kodexa.model.model import ContentObjectReference
        content_object_reference = ContentObjectReference(content_object, self, document, self.metastore[self.index])
        self.index = self.index + 1
        return content_object_reference

    def get_ref(self) -> str:
        """ """
        return self.store_path

    def register_listener(self, listener):
        """

        Args:
          listener:

        Returns:

        """
        self.listeners.append(listener)

    def notify_listeners(self, content_event: ContentEvent):
        """

        Args:
          content_event: ContentEvent:

        Returns:

        """
        for listener in self.listeners:
            listener.process_event(content_event)

    def to_dict(self):
        """ """
        return {
            "type": "DOCUMENT",
            "data": {
                "path": self.store_path
            }
        }

    def accept(self, document: Document):
        """

        Args:
          document: Document:

        Returns:

        """
        if self.mode == 'ALL':
            return True
        if self.mode == 'ONLY_NEW':
            return not self.exists(document)

    def read_metastore(self):
        """Read the metadata store"""
        self.metastore: List[Dict] = []
        with open(os.path.join(self.store_path, 'metastore.json')) as f:
            self.metastore = jsonpickle.decode("".join(f.readlines()))

    def write_metastore(self):
        """Method to write the JSON store index back to store path"""
        with open(os.path.join(self.store_path, 'metastore.json'), 'w') as f:
            f.write(jsonpickle.encode(self.metastore))

    def get_family(self, document_family_id: str) -> Optional[DocumentFamily]:
        for family in self.metastore:
            if family.id == document_family_id:
                return family
        return None

    def get_by_uuid(self, uuid: str) -> Optional[Document]:
        """

        Args:
          uuid: str:

        Returns:

        """
        for family in self.metastore:
            for content_object in family.content_objects:

                if content_object.id == uuid:
                    return Document.from_kdxa(os.path.join(self.store_path, content_object.id) + ".kdxa")
        return None

    def get_by_path(self, path: str) -> Optional[Document]:
        """Return the latest document in the family at the given path

        Args:
          path: return:
          path: str:

        Returns:

        """
        for family in self.metastore:
            if family.path == path:
                return Document.from_kdxa(os.path.join(self.store_path, family.get_latest_content().id) + ".kdxa")
        return None

    def query_families(self, query: str = "*", page: int = 1, page_size: int = 100) -> List[DocumentFamily]:

        # TODO implement query
        return self.metastore

    def get_family_by_path(self, path: str) -> Optional[DocumentFamily]:
        for family in self.metastore:
            if family.path == path:
                return family
        return None

    def get_latest_document(self, path: str) -> Optional[Document]:
        """

        Args:
          path: str:

        Returns:

        """
        for family in self.metastore:
            if family.path == path:
                return self.get_document_by_content_object(family, family.content_objects[-1])
        return None

    def list_objects(self) -> List[ContentObject]:
        """ """
        co_list: List[ContentObject] = []
        for family in self.metastore:
            co_list.extend(family.content_objects)

        return co_list

    def count(self) -> int:
        """Returns a count of the number of document families

        :return:

        Args:

        Returns:

        """
        return len(self.metastore)

    def load_kdxa(self, path: str):
        """

        Args:
          path: str:

        Returns:

        """
        document = Document.from_kdxa(path)
        self.put(document.uuid, document)

    def add_related_document_to_family(self, document_family_id: str, transition: DocumentTransition,
                                       document: Document):
        """

        Args:
          document_family_id: str:
          transition: DocumentTransition:
          document: Document:

        Returns:

        """
        self.read_metastore()
        for family in self.metastore:
            if family.id == document_family_id:
                new_event = self.add_document(family, document, transition)
                document.to_kdxa(os.path.join(self.store_path, new_event.content_object.id) + ".kdxa")
                self.write_metastore()

    def get_document_by_content_object(self, document_family: DocumentFamily,
                                       content_object: ContentObject) -> Document:
        """

        Args:
          document_family (DocumentFamily): The document family
          content_object (ContentObject): The content object

        Returns:
          The Kodexa document related to the content family

        """
        return Document.from_kdxa(os.path.join(self.store_path, content_object.id) + ".kdxa")

    def replace_content_object(self, document_family: DocumentFamily, content_object_id: str,
                               document: Document) -> Optional[DocumentFamily]:

        for co in document_family.content_objects:
            if co.id == content_object_id:
                document.to_kdxa(os.path.join(self.store_path, content_object_id) + ".kdxa")
                co.labels = document.labels
                co.classes = document.classes
                self.write_metastore()
                return document_family

        return None

    def put(self, path: str, document: Document, force_replace: bool = False) -> DocumentFamily:
        """

        Args:
          path (str): The path to the document family
          document (Document): The document you wish to upload
          force_replace (bool): True if you want to delete the family in this path first

        Returns:
            The new document family instance
        """

        # We can only add a document if it doesn't already exist as a family
        if self.get_family_by_path(path) is None:
            new_document_family = DocumentFamily(path=path)
            new_event = self.add_document(new_document_family, document)
            document.to_kdxa(os.path.join(self.store_path, new_event.content_object.id) + ".kdxa")

            self.metastore.append(new_document_family)
            self.write_metastore()

            # Notify the listeners
            self.notify_listeners(new_event)

        document_family = self.get_family_by_path(path)
        if document_family is not None:
            return document_family
        else:
            raise Exception("Unable to get document family?")

    def exists(self, document):
        """Look to see if we have document with the same original path and original filename

        Args:
          document: document to check

        Returns:
          True if it is already in the document store

        """

        # Lets just work with original_filename?

        for family in self.metastore:
            if document.source.original_filename == family.path:
                return True
        return False


class LocalModelStore(ModelStore):
    store_path: Optional[str] = Field(
        None, description='The path to the local storage'
    )

    metastore: Optional[List] = Field(
        None, description='The metadata for the store'
    )

    listeners: Optional[List] = Field(
        None, description='Current local listeners'
    )

    index: Optional[int] = Field(
        None, description='Current index'
    )

    def __init__(self, *args, **kwargs):
        if 'slug' not in kwargs:
            kwargs['slug'] = 'local'
        if 'type' not in kwargs:
            kwargs['type'] = 'DOCUMENT'
        if 'name' not in kwargs:
            kwargs['name'] = 'Local Document Store'
        super().__init__(*args, **kwargs)

        if self.store_path is None:
            from kodexa import KodexaPlatform
            self.store_path = tempfile.mkdtemp(dir=KodexaPlatform.get_tempdir())
            logger.info(f"Creating new local model store in {self.store_path} since no path was provided")

        path = Path(self.store_path)

        if kwargs.get('force_initialize', False) and path.exists():
            shutil.rmtree(self.store_path)
        if path.is_file():
            raise Exception("Unable to load store, since it is pointing to a file?")
        elif not path.exists():
            path.mkdir(parents=True)

    def to_dict(self):
        """ """
        return {
            "type": "MODEL",
            "data": {
                "path": self.store_path
            }
        }

    def get_native(self, path: str):
        """

        Args:
          path: str:

        Returns:

        """
        if Path(os.path.join(self.store_path, path)).is_file():
            return open(os.path.join(self.store_path, path), 'rb')
        else:
            return None

    def put_native(self, path: str, content: Any, force_replace=False):
        """

        Args:
          path (str): The path to the native file
          content (Any): The content to store
        Returns:

        """
        with open(os.path.join(self.store_path, path), 'wb') as file:
            file.write(content)


class TableDataStore(Store):
    """Stores data as a list of lists that can represent a table.

    This is a good store when you are capturing nested or tabular data.

    Args:
      columns: a list of the column names (default to dynamic)
      rows: initial set of rows (default to empty)

    Returns:

    """

    columns: Optional[List] = Field(
        None, description='The columns in this store'
    )

    rows: Optional[List] = Field(
        None, description='The rows in this store'
    )

    pipeline_context: Optional[Any] = Field(
        None, description='The context for the pipeline'
    )

    def __init__(self, columns=None, rows=None, **data: Any):
        data['slug'] = 'local'
        data['type'] = 'TABLE'
        data['version'] = '1.0.0'
        data['name'] = 'Local Store'
        super().__init__(**data)
        if rows is None:
            rows = []
        if columns is None:
            columns = []
        self.columns: List[str] = columns
        self.rows: List[List] = rows

        self.pipeline_context = None

    """
    Return the store as a dict for serialization
    """

    def to_dict(self):
        """Create a dictionary representing this TableDataStore's structure and content.

        Args:

        Returns:
          dict: The properties of this TableDataStore structured as a dictionary.

        >>> table_data_store.to_dict()
        """

        return {
            "type": "TABLE",
            "data": {
                "columns": self.columns,
                "rows": self.rows
            }
        }

    def clear(self):
        """ """
        self.rows = []

    def to_df(self):
        """ """
        import pandas as pd

        if not self.columns:
            return pd.DataFrame(self.rows)
        else:
            return pd.DataFrame(self.rows, columns=self.columns)

    def set_pipeline_context(self, pipeline_context):
        """

        Args:
          pipeline_context:

        Returns:

        """
        self.pipeline_context = pipeline_context

    def add(self, row):
        """Writes a row to the Data Store

        Args:
          row: the row (as a list) to add

        Returns:

        """
        self.rows.append(row)

    def count(self):
        """Returns the number of rows in the store

        :return: number of rows

        Args:

        Returns:

        """
        return len(self.rows)

    def merge(self, other_store):
        """Merge another table store into this store

        Args:
          other_store: return: the other store

        Returns:
          the other store

        """
        self.rows = self.rows + other_store.rows

    @classmethod
    def from_dict(cls, store_dict):
        """

        Args:
          store_dict:

        Returns:

        """
        return TableDataStore(columns=store_dict['data']['columns'], rows=store_dict['data']['rows'])
