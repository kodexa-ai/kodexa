"""
Remote stores allow you to interact with an instance of the Kodexa platform
"""

import json
import logging
from json import JSONDecodeError
from typing import Dict, List, Optional

import requests

from kodexa.model import ContentObject, Document, DocumentFamily, DocumentStore, ModelStore, RemoteStore
from kodexa.stores.local import LocalModelStore, TableDataStore

logger = logging.getLogger('kodexa.stores')


class RemoteTableDataStore(RemoteStore):
    """ """

    def __init__(self, ref: str, columns=None):
        if columns is None:
            columns = []
        self.ref = ref
        self.columns = columns

    def get_ref(self):
        """ """
        return self.ref

    def get_table_df(self, table: str):
        """

        Args:
          table: str:

        Returns:

        """
        import pandas as pd

        table_result = self.get_table(table)
        return pd.DataFrame(table_result['rows'], columns=table_result['columns'])

    def get_table(self, table: str):
        """

        Args:
          table: str:

        Returns:

        """

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
        """

        Args:
          table: str:
          page_number: int:  (Default value = 1)
          page_size:  (Default value = 5000)

        Returns:

        """
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
        """

        Args:
          rows:

        Returns:

        """
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
        """

        Args:
          row:

        Returns:

        """
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


class DataStoreHelper:
    """A small helper that can convert a dictionary back into a store
    type

    Args:

    Returns:

    """

    @staticmethod
    def from_dict(dict):
        """Build a new TableDataStore or DictDataStore from a dictionary.

        Args:
          dict: doc_dict: A dictionary representation of a Kodexa Document.

        Returns:
          TableDataStore, DictDataStore, or None: A TableDataStore or DictDataStore - driven from 'type' in doc_dict.  If 'type' is not present or does not align with one of these two types, None is returend.

        >>> Document.from_dict(doc_dict)
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
            logger.info("Unknown store")
            return None


class RemoteDocumentStore(DocumentStore, RemoteStore):
    """
    Remote Document Stores provide you with all the capabilities of Document storage and relationships
    in an instance of the Kodexa platform
    """

    def __init__(self, ref: str, query: str = "*"):
        self.ref: str = ref
        self.objects: Optional[List[Dict]] = None
        self.page = 1
        self.query_string: str = query

    def get_document_by_content_object(self, content_object: ContentObject) -> Optional[Document]:
        """
        Returns (if found) an instance of the Kodexa document based on the content object

        Args:
            content_object: The content object you are looking for the document for

        Returns:
            Document or None if not found
        """
        return self.get(content_object.id)

    def register_listener(self, listener):
        """
        You can not register a listener with a remote document store

        Args:
            listener: The listener you wish to register

        Returns:
            NotImplementedError

        """
        raise NotImplementedError

    def count(self) -> int:
        """
        A count of the document families in the store

        Returns:
          A count of the documents in the store

        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/families"
        logger.info(f"Downloading source from {url}")

        count_response = requests.get(
            url,
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if count_response.status_code == 200:
            return count_response.json()['totalElements']
        elif count_response.status_code == 404:
            return 0
        else:
            msg = "Get document failed [" + count_response.text + "], response " + str(count_response.status_code)
            logger.error(msg)
            raise Exception(msg)

    def get_by_uuid(self, uuid_value: str) -> Optional[Document]:
        """
        Returns a document (if present) by the UUID (which should match the ID of the content object)

        Args:
            uuid_value: of the document which should match the content object ID

        Returns:
            A document, or None if not found
        """
        return self.get(uuid_value)

    def get_name(self):
        """The name of the connector

        Returns:
            The name of the document store

        """
        return self.get_ref()

    def get_ref(self) -> str:
        """Get the reference to the store on the platform (i.e. kodexa/my-store:1.1.0)

        :return: The reference

        Args:

        Returns:

        """
        return self.ref

    def to_dict(self):
        """
        Convert the document store to its metadata dictionary

        Returns:
            A dictionary representing the metadata for the store
        """
        return {
            "type": "DOCUMENT",
            "ref": self.ref
        }

    def get(self, content_object_id: str) -> Optional[Document]:
        """
        Get the document from the remote store using the content object's ID

        Args:
          content_object_id:str the ID of the content object

        Returns:
          Optionally the document, if the document is not found we will return None

        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents/{content_object_id}/content"
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

    def get_source(self, content_object_id: str):
        """
        Gets the source for a given content object ID from the document store, as per the connector protocol

        Args:
          content_object_id:str content_object_id for which you what the source (native)

        Returns:
          either the source content (byte-array) or None if the document doesn't exist

        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents/{content_object_id}/content"
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

        Args:
          document_id: str: the ID of the document to delete

        Returns:

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

        Args:
          path: the path (i.e. /my-folder/file.pdf)

        Returns:
          The latest document representation for that path

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

    def put_native(self, path: str, content, force_replace=False) -> ContentObject:
        """
        Push content directly, this will create both a native object in the store and also a
        related Document that refers to it.

        Args:
          path:str the path where you want to put the native content
          content: the binary content for the native file
          force_replace: replace the content at this path completely (Default value = False)

        Returns:
          The content object that was created

        """
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Putting document with path {path}")

            files = {"file": content}
            data = {"path": path, "forceReplace": force_replace}
            content_object_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files, data=data)

            if content_object_response.status_code == 200:
                return ContentObject.from_dict(content_object_response.json())
            else:
                logger.error("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
                raise Exception("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
        except JSONDecodeError:
            logger.error("Unable to decode the JSON response")
            raise

    def put(self, path: str, document: Document, force_replace=False) -> DocumentFamily:
        """
        Put the document into the document store at the given path, note that if there is already a document
        at this path then the lineage UUID for this document must related to one of the documents the documents
        that are held at that path

        Args:
          path: the path to the document to use
          document: the document
          force_replace: this will remove all the representations of the document at this path and replace it with this one (Default value = False)
          path: str:
          document: Document:

        Returns:
            ContentObject: the content object
        """
        from kodexa import KodexaPlatform
        try:
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
                return ContentObject.from_dict(content_object)
            else:
                logger.error("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
                raise Exception("Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code))
        except JSONDecodeError:
            logger.error(
                "Unable to decode the JSON response")
            raise

    def get_next_objects(self):
        """ """
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
        """Query the documents in the given document store and a list of the document metadata matches

        Args:
          sort_direction: the sort direction (either asc - ascending or desc - descending) (Default value = 'asc')
          sort_by: the name of the metadata field to sort by (ie. createdDate) (Default value = None)
          query: A lucene style query for the metadata in the document store
          query: str:

        Returns:
          A list of content objects

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

        Args:

        Returns:

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

    def get_family_by_path(self, path: str) -> Optional[DocumentFamily]:
        from kodexa import KodexaPlatform
        import requests
        resp = requests.get(
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs/{path}",
            params={'meta': True},
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if resp.status_code == 200:
            return DocumentFamily.from_dict(resp.json())
        if resp.status_code == 404:
            return None
        else:
            msg = f"Unable to get file from store at given path - {resp.text} - status : {resp.status_code}"
            logger.error(msg)
            raise Exception(msg)

    def add_related_document_to_family(self, document_family_id: str, document_relationship,
                                       document: Document):
        """Add a document to a family as a new transition

        Args:
          document_family_id: the ID for the document family
          document_relationship: the document transition
          document: the document
          document_family_id: str:
          document: Document:

        Returns:
          None

        """
        pass


class RemoteModelStore(ModelStore, RemoteStore):
    """
    A remote model store allows you to store artifacts from your model
    """

    def to_dict(self):
        """ """
        return {
            "type": "MODEL",
            "ref": self.ref
        }

    def __init__(self, ref: str):
        self.ref = ref

    def get_ref(self) -> str:
        """
        Get the reference to the store on the platform (i.e. kodexa/my-store:1.1.0)

        Returns:
            The reference to the store
        """
        return self.ref

    def delete(self, object_path: str):
        """Delete the content stored in the model store at the given path

        Args:
          object_path: the path to the content (ie. mymodel.dat)
          object_path: str:

        Returns:
          True if deleted, False if there was no file at the path

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
        """Get the bytes for the object at the given path, will return None if there is no object there

        Args:
          object_path: the object path
          object_path: str:

        Returns:
          the bytes or None is nothing is at the path

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

    def put(self, path: str, content, force_replace=False) -> ContentObject:
        """Put the content into the model store at the given path

        Args:
          path: The path you wish to put the content at
          content: The content for that object
          force_replace: overwrite the existing object if it is there (defaulted to False)
          path: str:

        Returns:

        """
        from kodexa import KodexaPlatform
        import requests
        try:
            files = {"file": content}
            data = {"path": path, "forceReplace": force_replace}
            content_object_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/contents",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files, data=data)

            if content_object_response.status_code == 200:
                return ContentObject.from_dict(content_object_response.json())
            elif content_object_response.status_code == 400:
                from addict import Dict
                bad_request = Dict(json.loads(content_object_response.text))
                for error_key in bad_request.errors.keys():
                    print(bad_request.errors[error_key] + " (" + error_key + ")")
                raise Exception("Invalid request")
            else:
                msg = "Execution creation failed [" + content_object_response.text + "], response " + str(
                    content_object_response.status_code)
                logger.error(msg)
                raise Exception(msg)
        except JSONDecodeError:
            logger.error(
                "Unable to JSON decode the response?")
            raise
