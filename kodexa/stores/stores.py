import logging
import os
import shutil
from pathlib import Path

from kodexa.model import Document

logger = logging.getLogger('kodexa-stores')


class JsonDocumentStore:
    """
    An implementation of a document store that uses JSON files to store the documents and
    maintains an index.json containing some basics of the documents
    """

    def __init__(self, store_path: str, force_initialize: bool = False):
        self.store_path = store_path
        self.document_ids = []
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
            open(os.path.join(path, 'index.json'), 'a').close()
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
        with open(os.path.join(self.store_path, 'index.json')) as f:
            self.document_ids = f.readlines()

    def save_index(self):
        """
        Method to write the JSON store index back to store path
        """
        with open(os.path.join(self.store_path, 'index.json'), 'w') as f:
            f.writelines(self.document_ids)

    def reset_connector(self):
        """
        Reset the index back to the beginning
        """
        self.index = 0


class TableDataStore:
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
        self.columns = columns
        self.rows = rows

    """
    Return the store as a dict for serialization
    """

    def to_dict(self):
        return {
            "type": "table",
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


class DictDataStore:
    """
    Stores data as a list of dictionaries that can be any structure

    This is a good store when you are capturing nested or semi-structured data
    """

    def __init__(self, dicts=None):
        if dicts is None:
            dicts = []
        self.dicts = dicts

    """
    Return the store as a dict for serialization
    """

    def to_dict(self):
        return {
            "type": "dictionary",
            "data": {
                "dicts": self.dicts
            }
        }

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


class DataStoreHelper:
    """
    A small helper that can convert a dictionary back into a store
    type
    """

    @staticmethod
    def from_dict(dict):
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
