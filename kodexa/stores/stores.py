import logging
import os
import shutil
from pathlib import Path
from typing import List, Dict, Optional

from kodexa.model import Document, Store
from kodexa.pipeline import PipelineContext

logger = logging.getLogger('kodexa-stores')


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
            logging.info(f"Creating new store in {store_path}")
            path.mkdir(parents=True)

            # Create an empty index file
            open(os.path.join(path, 'index.idx'), 'a').close()
        self.read_index()

        logging.info(f"Found {len(self.document_ids)} documents in {store_path}")

    def get_name(self):
        return f"JSON Document Store [{self.store_path}]"

    def sink(self, document: Document):
        self.add(document)

    def __iter__(self):
        return self

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
            "type": "table",
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

    def set_pipeline_context(self, pipeline_context: PipelineContext):
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
            "type": "dictionary",
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
            if 'table' == dict['type']:
                columns = dict['data']['columns'] if 'columns' in dict['data'] else None
                rows = dict['data']['rows'] if 'rows' in dict['data'] else None
                return TableDataStore(columns=columns, rows=rows)
            elif 'dictionary' == dict['type']:
                return DictDataStore(dict['data']['dicts'])
            else:
                return None
        else:
            logger.info(f"Unknown store")
            return None
