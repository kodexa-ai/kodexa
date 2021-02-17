import json
import logging
from json import JSONDecodeError
from typing import List, Dict, Optional

import requests

from kodexa.model import Document, DocumentStore, RemoteStore, ModelStore, ContentObject
from kodexa.stores.local import LocalModelStore, TableDataStore

logger = logging.getLogger('kodexa.stores')


class RemoteTableDataStore(RemoteStore):

    def __init__(self, ref: str, columns: List[str] = []):
        self.ref = ref
        self.columns = columns

    def get_ref(self):
        return self.ref

    def get_table_df(self, table: str):
        import pandas as pd

        table_result = self.get_table(table)
        return pd.DataFrame(table_result['rows'], columns=table_result['columns'])

    def get_table(self, table: str):

        # We need to get the first set of rows,
        rows: List = []
        row_response = self.get_table_page_request(table, 1)

        # lets work out the last page
        rows = rows + row_response['content']
        total_pages = row_response['totalPages']

        for page in range(2, total_pages):
            row_response = self.get_table_page_request(table, page)
            rows = rows + row_response['content']

        # Once we have all the rows we will then get a list of all the columns
        # and convert this into a more nature form for structured data

        column_names: List[str] = []
        for row in rows:
            for key in row['data'].keys():
                if key not in column_names:
                    column_names.append(key)

        # Now lets get all the rows and make sure we put them in the same
        # order as the columns

        new_rows: List[List[str]] = []

        for row in rows:
            new_row = []
            for column_name in column_names:
                new_row.append(row['data'].get(column_name, None))
            new_rows.append(new_row)

        return {
            "columns": column_names,
            "rows": new_rows
        }

    def get_table_page_request(self, table: str, page_number: int = 1, page_size=5000):
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/rows"
        logger.debug(f"Downloading a specific table from {url}")

        # We need to go through and pull all the pages
        rows_response = requests.get(
            url,
            params={"table": table, "page": page_number, "pageSize": page_size},
            headers={"x-access-token": KodexaPlatform.get_access_token(), "content-type": "application/json"})

        if rows_response.status_code == 200:
            return rows_response.json()
        else:
            logger.error("Unable to get table from remote store [" + rows_response.text + "], response " + str(
                rows_response.status_code))
            raise Exception("Unable to get table from remote store  [" + rows_response.text + "], response " + str(
                rows_response.status_code))

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
            elif 'DOCUMENT' == dict['type']:
                if 'ref' in dict:
                    return RemoteDocumentStore(dict['ref'])
                else:
                    from kodexa import LocalDocumentStore
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
                return content_object
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

    def query_objects(self, query: str, sort_by=None, sort_direction='asc') -> List[ContentObject]:
        """
        Query the documents in the given document store and a list of the document metadata matches

        :param sort_direction: the sort direction (either asc - ascending or desc - descending)
        :param sort_by: the name of the metadata field to sort by (ie. createdDate)
        :param query: A lucene style query for the metadata in the document store
        :return: A list of content objects
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
        results: List[ContentObject] = []
        for co_dict in list_content.json()['content']:
            results.append(ContentObject.from_dict(co_dict))
        return results

    def list_objects(self) -> List[ContentObject]:
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

        results: List[ContentObject] = []
        for co_dict in list_content.json()['content']:
            results.append(ContentObject.from_dict(co_dict))
        return results

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
