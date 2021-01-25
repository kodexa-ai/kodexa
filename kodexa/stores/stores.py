import dataclasses
import json
import logging
import os
import shutil
from json import JSONDecodeError
from pathlib import Path
from typing import List, Dict, Optional

import requests

from kodexa.model import Document, Store, DocumentStore, RemoteStore, ModelStore

logger = logging.getLogger('kodexa.stores')


class JsonDocumentStore(Store):
    """
    An implementation of a document store that uses JSON files to store the documents and
    maintains an index.idx containing some basics of the documents
    """

    def __init__(self, store_path: str, force_initialize: bool = False):
        self.store_path = store_path
        self.document_ids: List[str] = []
        self.index = 0

        # We will delete any store we find

        path = Path(store_path)

        if force_initialize and path.exists():
            shutil.rmtree(store_path)

        if path.is_file():
            raise Exception("Unable to load store, since it is pointing to a file?")
        elif not path.exists():
            logger.info(f"Creating new store in {store_path}")
            path.mkdir(parents=True)

            # Create an empty index file
            open(os.path.join(path, 'index.idx'), 'a').close()
        self.read_index()

        logger.info(f"Found {len(self.document_ids)} documents in {store_path}")

    def get_name(self):
        return f"JSON Document Store [{self.store_path}]"

    def sink(self, document: Document):
        self.add(document)

    def __iter__(self):
        return self

    def accept(self, document: Document):
        return True

    def __next__(self):
        if self.index > len(self.document_ids) - 1:
            raise StopIteration
        else:
            self.index += 1
            return self.load(self.document_ids[self.index - 1])

    def count(self):
        """
        The number of documents in the store

        :return: The number of documents
        """
        return len(self.document_ids)

    def get(self, idx: int):
        """
        Load the document at the given index

        :return: Document at given index
        """
        return self.load(self.document_ids[idx])

    def delete(self, idx: int):
        """
        Delete the document at the given index

        :return: The Document that was removed
        """
        document_id = self.document_ids.pop(idx)
        os.remove(os.path.join(self.store_path, document_id, '.json'))

    def add(self, document: Document):
        """
        Add a new document and return the index position

        :return: The index of the document added
        """
        self.document_ids.append(document.uuid)
        self.save_index()
        self.save(document)
        return len(self.document_ids)

    def save(self, document: Document):
        with open(os.path.join(self.store_path, document.uuid + '.json'), 'w', encoding='utf8') as f:
            f.write(document.to_json())

    def load(self, document_id: str):
        """
        Loads the document with the given document ID

        :return the document
        """
        with open(os.path.join(self.store_path, document_id + '.json'), encoding='utf8') as f:
            return Document.from_json(f.read())

    def get_document(self, index: int):
        """
        Gets the document from the specific index

        :param index: index of document to get
        :return: the document
        """
        return self.load(self.document_ids[index])

    def read_index(self):
        """
        Method to read the document index from the store path
        """
        self.document_ids = []
        with open(os.path.join(self.store_path, 'index.idx')) as f:
            self.document_ids = f.read().splitlines()

    def save_index(self):
        """
        Method to write the JSON store index back to store path
        """
        with open(os.path.join(self.store_path, 'index.idx'), 'w') as f:
            # f.writelines(self.document_ids)
            f.write('\n'.join(self.document_ids))

    def reset_connector(self):
        """
        Reset the index back to the beginning
        """
        self.index = 0


class RemoteTableDataStore(RemoteStore):

    def __init__(self, ref: str, columns: List[str] = []):
        self.ref = ref
        self.columns = columns

    def get_ref(self):
        return self.ref

    def delete_rows_by_content_object(self, content_object_id:str, taxonomy_ref:str):
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/rows"
        logger.debug(f"Uploading rows to store {url}")

        doc = requests.delete(
            url,
            params={"contentObjectId": content_object_id, "taxonomyRef": taxonomy_ref},
            headers={"x-access-token": KodexaPlatform.get_access_token(), "content-type": "application/json"})
        if doc.status_code == 200:
            return
        else:
            logger.error("Unable to delete rows to remote store [" + doc.text + "], response " + str(doc.status_code))
            raise Exception("Unable to delete rows to remote store [" + doc.text + "], response " + str(doc.status_code))

    def add_rows(self, rows):
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/rows"
        logger.debug(f"Uploading rows to store {url}")

        doc = requests.post(
            url,
            json=rows,
            headers={"x-access-token": KodexaPlatform.get_access_token(), "content-type": "application/json"})
        if doc.status_code == 200:
            return
        else:
            logger.error("Unable to post rows to remote store [" + doc.text + "], response " + str(doc.status_code))
            raise Exception("Unable to post rows to remote store [" + doc.text + "], response " + str(doc.status_code))

    def add(self, row):
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/rows"
        logger.debug(f"Uploading rows to store {url}")

        row_dict = {}
        for idx, row_value in enumerate(row):
            if len(self.columns) == 0 or len(self.columns) <= idx:
                row_dict[f'col{idx}'] = row_value
            else:
                row_dict[self.columns[idx]] = row_value

        doc = requests.post(
            url,
            json=[{'data': row_dict}],
            headers={"x-access-token": KodexaPlatform.get_access_token(), "content-type": "application/json"})
        if doc.status_code == 200:
            return
        else:
            logger.error("Unable to post rows to remote store [" + doc.text + "], response " + str(doc.status_code))
            raise Exception("Unable to post rows to remote store [" + doc.text + "], response " + str(doc.status_code))


class TableDataStore(Store):
    """
    Stores data as a list of lists that can represent a table.

    This is a good store when you are capturing nested or tabular data.

    :param columns: a list of the column names (default to dynamic)
    :param rows: initial set of rows (default to empty)
    :param source_documents: initial dictionary of document UUID to row links (default to empty)

    """

    def __init__(self, columns=None, rows=None, source_documents=None):
        if source_documents is None:
            source_documents = {}
        if rows is None:
            rows = []
        if columns is None:
            columns = []
        self.columns: List[str] = columns
        self.rows: List[List] = rows
        self.source_documents: Dict[str, Dict] = source_documents

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
                "rows": self.rows,
                "source_documents": self.source_documents
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

        if self.pipeline_context and self.pipeline_context.current_document:
            current_document = self.pipeline_context.get_current_document()
            if current_document.uuid not in self.source_documents:
                self.source_documents[current_document.uuid] = {"metadata": current_document.metadata, "rows": []}
            self.source_documents[current_document.uuid]["rows"].append(len(self.rows) - 1)

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


class RemoteDictDataStore(RemoteStore):

    def __init__(self, ref: str):
        self.ref: str = ref

    def get_ref(self):
        return self.ref

    def add(self, dict):
        """
        Writes a dict to the Data Store

        :param dict: the dict to add to the store
        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/dictionaries"
        logger.debug(f"Uploading dictionaries to store {url}")
        doc = requests.post(
            url,
            [{'data': dict}],
            headers={"x-access-token": KodexaPlatform.get_access_token()})
        if doc.status_code == 200:
            return
        else:
            logger.error("Unable to post dict to remote store [" + doc.text + "], response " + str(doc.status_code))
            raise Exception("Unable to post dict to remote store [" + doc.text + "], response " + str(doc.status_code))


class DictDataStore:
    """
    Stores data as a list of dictionaries that can be any structure

    This is a good store when you are capturing nested or semi-structured data
    """

    def __init__(self, dicts=None):
        if dicts is None:
            dicts = []
        self.dicts = dicts
        self.pipeline_context = None

    """
    Return the store as a dict for serialization
    """

    def to_dict(self):
        """
        Create a dictionary representing this DictDataStore's structure and content.

            >>> this_dictionary.to_dict()

        :return: The properties of this DictDataStore structured as a dictionary.
        :rtype: dict
        """
        return {
            "type": "DICTIONARY",
            "data": {
                "dicts": self.dicts
            }
        }

    def set_pipeline_context(self, pipeline_context):
        self.pipeline_context = pipeline_context

    def add(self, dict):
        """
        Writes a dict to the Data Store

        :param dict: the dict to add to the store
        """
        self.dicts.append(dict)

    def count(self):
        """
        Returns the number of dictionaries in the store

        :return: number of dictionaries
        """
        return len(self.dicts)

    def merge(self, other_store):
        """
        Merge another table store into this store

        :param other_store:
        :return: the other store
        """
        self.dicts = self.dicts + other_store.dicts


class DataStoreHelper:
    """
    A small helper that can convert a dictionary back into a store
    type
    """

    @staticmethod
    def from_dict(dict):
        """
        Build a new TableDataStore or DictDataStore from a dictionary.

            >>> Document.from_dict(doc_dict)

        :param dict doc_dict: A dictionary representation of a Kodexa Document.

        :return: A TableDataStore or DictDataStore - driven from 'type' in doc_dict.  If 'type' is not present or does not align with one of these two types, None is returend.
        :rtype: TableDataStore, DictDataStore, or None
        """

        if 'type' in dict:
            if 'TABLE' == dict['type']:
                columns = dict['data']['columns'] if 'columns' in dict['data'] else None
                rows = dict['data']['rows'] if 'rows' in dict['data'] else None
                return TableDataStore(columns=columns, rows=rows)
            elif 'DICTIONARY' == dict['type']:
                return DictDataStore(dict['data']['dicts'])
            elif 'DOCUMENT' == dict['type']:
                if 'ref' in dict:
                    return RemoteDocumentStore(dict['ref'])
                else:
                    return LocalDocumentStore(dict['data']['path'])
            elif 'MODEL' == dict['type']:
                if 'ref' in dict:
                    return RemoteModelStore(dict['ref'])
                else:
                    return LocalModelStore(dict['data']['path'])
            else:
                return None
        else:
            logger.info(f"Unknown store")
            return None


class LocalDocumentStore(DocumentStore):

    def __init__(self, store_path: str, force_initialize: bool = False, mode: str = 'ALL'):

        modes = ['ALL', 'ONLY_NEW']

        if mode not in modes:
            raise Exception(f"LocalDocumentStore mode must be one of {','.join(modes)}")

        self.store_path = store_path
        self.index = 0
        self.metastore: List[Dict] = []
        self.mode = mode

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
            self.metastore = json.load(f)

    def write_metastore(self):
        """
        Method to write the JSON store index back to store path
        """
        with open(os.path.join(self.store_path, 'metastore.json'), 'w') as f:
            json.dump(self.metastore, f)

    def get_by_uuid(self, uuid: str) -> Optional[Document]:
        for metadata in self.metastore:
            if metadata['uuid'] == uuid:
                return Document.from_kdxa(os.path.join(self.store_path, metadata['uuid']) + ".kdxa")
        return None

    def get_by_path(self, path: str) -> Optional[Document]:
        for metadata in self.metastore:
            if metadata['path'] == path:
                return Document.from_kdxa(os.path.join(self.store_path, metadata['uuid']) + ".kdxa")
        return None

    def list_objects(self) -> List[Dict]:
        return self.metastore

    def count(self) -> int:
        return len(self.metastore)

    def load_kdxa(self, path: str):
        document = Document.from_kdxa(path)
        self.put(document.uuid, document)

    def put(self, path: str, document: Document):
        document.to_kdxa(os.path.join(self.store_path, document.uuid) + ".kdxa")
        self.metastore.append(
            {'metadata': document.metadata, 'source': dataclasses.asdict(document.source), 'uuid': document.uuid,
             'id': document.uuid,
             'content_type': 'Document',
             'path': path, 'labels': document.get_labels()})
        self.write_metastore()

    def exists(self, document):
        """
        Look to see if we have document with the same original path and original filename

        :param document: document to check
        :return: True if it is already in the document store
        """
        for metadata in self.metastore:
            if document.source.original_path == metadata['source']['original_path'] and \
                    document.source.original_filename == metadata['source']['original_filename']:
                return True
        return False


class RemoteDocumentStore(DocumentStore, RemoteStore):

    def __init__(self, ref: str, query: str = "*"):
        self.ref: str = ref
        self.objects: Optional[List[Dict]] = None
        self.page = 1
        self.query_string: str = query

    def get_name(self):
        """
        The name of the connector

        :return: 'document-store'
        """
        return "document-store"

    def get_ref(self) -> str:
        """
        Get the reference to the store on the platform (i.e. kodexa/my-store:1.1.0)

        :return: The reference
        """
        return self.ref

    def to_dict(self):
        return {
            "type": "DOCUMENT",
            "ref": self.ref
        }

    def get(self, document_id: str) -> Optional[Document]:
        """
        Get the document from the remote store using the document's ID

        :param document_id: the ID of the document
        :return: Optionally the document, if the document is not found we will return None
        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents/{document_id}/content"
        logger.info(f"Downloading document from {url}")
        doc = requests.get(
            url,
            headers={"x-access-token": KodexaPlatform.get_access_token()})
        if doc.status_code == 200:
            return Document.from_msgpack(doc.content)
        elif doc.status_code == 404:
            return None
        else:
            logger.error("Get document failed [" + doc.text + "], response " + str(doc.status_code))
            raise Exception("Get document failed [" + doc.text + "], response " + str(doc.status_code))

    def get_source(self, document_id: str):
        """
        Gets the source for a given document ID from the document store, as per the connector protocol

        :param document_id: document id for which you what the source
        :return: either the source content (byte-array) or None if the document doesn't exist
        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents/{document_id}/content"
        logger.info(f"Downloading source from {url}")

        doc = requests.get(
            url,
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if doc.status_code == 200:
            return doc.content
        elif doc.status_code == 404:
            return None
        else:
            logger.error("Get document failed [" + doc.text + "], response " + str(doc.status_code))
            raise Exception("Get document failed [" + doc.text + "], response " + str(doc.status_code))

    def delete(self, document_id: str):
        """
        Delete the document with this document ID from the remote document store

        :param document_id: the ID of the document to delete
        """
        from kodexa import KodexaPlatform
        delete_document_response = requests.delete(
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref}/contents/{document_id}",
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if delete_document_response.status_code == 200:
            logger.info(f"Deleted document {document_id}")
        else:
            logger.error("Delete document failed [" + delete_document_response.text + "], response " + str(
                delete_document_response.status_code))
            raise Exception("Delete document failed [" + delete_document_response.text + "], response " + str(
                delete_document_response.status_code))

    def get_by_path(self, path) -> Optional[Document]:
        """
        Return the latest representation document at a given path

        :param path: the path (i.e. /my-folder/file.pdf)
        :return: The latest document representation for that path
        """
        from kodexa import KodexaPlatform
        import requests
        resp = requests.get(
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs/{path}",
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if resp.status_code == 200:
            return Document.from_msgpack(resp.content)
        if resp.status_code == 404:
            return None
        else:
            msg = f"Unable to get file from store at given path - {resp.text} - status : {resp.status_code}"
            logger.error(msg)
            raise Exception(msg)

    def put_native(self, path: str, content, force_replace=False):
        """
        Push content directly, this will create both a native object in the store and also a
        related Document that refers to it.

        :param path: the path where you want to put the native content
        :param content: the binary content for the native file
        :param force_replace: replace the content at this path completely
        :return: None
        """
        from kodexa import KodexaPlatform
        try:
            import io

            logger.info(f"Putting document with path {path}")

            files = {"file": content}
            data = {"path": path, "forceReplace": force_replace}
            content_object_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files, data=data)

            if content_object_response.status_code == 200:
                from addict import Dict
                content_object = Dict(json.loads(content_object_response.text))
            else:
                logger.error("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
                raise Exception("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
        except JSONDecodeError:
            logger.error(
                f"Unable to decode the JSON response")
            raise

    def put(self, path: str, document: Document, force_replace=False):
        """
        Put the document into the document store at the given path, note that if there is already a document
        at this path then the lineage UUID for this document must related to one of the documents the documents
        that are held at that path

        :param path: the path to the document to use
        :param document: the document
        :param force_replace: this will remove all the representations of the document at this path and replace it with this one
        """
        from kodexa import KodexaPlatform
        try:
            import io

            logger.info(f"Putting document with path {path}")

            files = {"document": document.to_msgpack()}
            data = {"path": path, "forceReplace": force_replace}
            content_object_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files, data=data)

            if content_object_response.status_code == 200:
                from addict import Dict
                content_object = Dict(json.loads(content_object_response.text))
            else:
                logger.error("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
                raise Exception("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
        except JSONDecodeError:
            logger.error(
                f"Unable to decode the JSON response")
            raise

    def get_next_objects(self):
        from kodexa import KodexaPlatform
        content_objects_response = requests.get(
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents",
            params={"query": self.query, "page": self.page, "pageSize": 20},
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if content_objects_response.status_code != 200:
            raise Exception(
                f"Exception occurred while trying to fetch objects [{content_objects_response.status_code}]")
        else:
            self.objects = content_objects_response.json()['content']

    def query_objects(self, query: str, sort_by=None, sort_direction='asc') -> List[Dict]:
        """
        Query the documents in the given document store and a list of the document metadata matches

        :param sort_direction: the sort direction (either asc - ascending or desc - descending)
        :param sort_by: the name of the metadata field to sort by (ie. createdDate)
        :param query: A lucene style query for the metadata in the document store
        :return: A list of dictionaries containing the metadata for the documents
        """
        from kodexa import KodexaPlatform
        params = {'query': query}
        if sort_by is not None:
            params['sortBy'] = sort_by
            params['sortDesc'] = sort_direction

        print(query)
        print(f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents")
        list_content = requests.get(
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents",
            params=params,
            headers={"x-access-token": KodexaPlatform.get_access_token()})
        if list_content.status_code != 200:
            raise Exception(
                f"Exception occurred while trying to fetch objects [{list_content.status_code}]")
        return list_content.json()['content']

    def list_objects(self) -> List[Dict]:
        """
        List the objects in the remote document store

        :return: a list of the dictionaries containing the metadata for the documents in the store
        """
        from kodexa import KodexaPlatform
        list_content = requests.get(
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents",
            headers={"x-access-token": KodexaPlatform.get_access_token()})
        if list_content.status_code != 200:
            raise Exception(
                f"Exception occurred while trying to fetch objects [{list_content.status_code}]")
        return list_content.json()['content']

    def __iter__(self):
        return self

    def __next__(self):

        if self.objects is None:
            self.objects = self.query_objects(self.query_string)

        if len(self.objects) == 0:
            raise StopIteration
        else:
            content_object = self.objects.pop(0)

            if content_object['content_type'] == "DOCUMENT":
                return self.get(content_object['id'])

            raise StopIteration


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


class RemoteModelStore(ModelStore, RemoteStore):

    def to_dict(self):
        return {
            "type": "MODEL",
            "ref": self.ref
        }

    def __init__(self, ref: str):
        self.ref = ref

    def get_ref(self) -> str:
        """
        Get the reference to the store on the platform (i.e. kodexa/my-store:1.1.0)

        :return: The reference
        """
        return self.ref

    def delete(self, object_path: str):
        """
        Delete the content stored in the model store at the given path

        :param object_path: the path to the content (ie. mymodel.dat)
        :return: True if deleted, False if there was no file at the path
        """
        from kodexa import KodexaPlatform
        import requests
        resp = requests.delete(
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs/{object_path}",
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if resp.status_code == 200:
            return True
        if resp.status_code == 404:
            return False
        else:
            msg = f"Unable to delete model object {resp.text}, status : {resp.status_code}"
            logger.error(msg)
            raise Exception(msg)

    def get(self, object_path: str):
        """
        Get the bytes for the object at the given path, will return None if there is no object there

        :param object_path: the object path
        :return: the bytes or None is nothing is at the path
        """
        from kodexa import KodexaPlatform
        import requests
        resp = requests.get(
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs/{object_path}",
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if resp.status_code == 200:
            return resp.content
        else:
            msg = f"Unable to get model object {resp.text}, status : {resp.status_code}"
            logger.error(msg)
            raise Exception(msg)

    def put(self, path: str, content, force_replace=False):
        """
        Put the content into the model store at the given path

        :param path: The path you wish to put the content at
        :param content: The content for that object
        :param force_replace: overwrite the existing object if it is there (defaulted to False)
        """
        from kodexa import KodexaPlatform
        import requests
        try:
            import io

            files = {"file": content}
            data = {"path": path, "forceReplace": force_replace}
            content_object_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files, data=data)

            if content_object_response.status_code == 200:
                from addict import Dict
                content_object = Dict(json.loads(content_object_response.text))
            elif content_object_response.status_code == 400:
                from addict import Dict
                bad_request = Dict(json.loads(content_object_response.text))
                for error_key in bad_request.errors.keys():
                    print(bad_request.errors[error_key] + " (" + error_key + ")")
            else:
                logger.error("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
                raise Exception("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
        except JSONDecodeError:
            logger.error(
                f"Unable to JSON decode the response?")
            raise
