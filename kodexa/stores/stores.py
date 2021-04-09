"""
Remote stores allow you to interact with an instance of the Kodexa platform
"""

import json
import logging
from json import JSONDecodeError
from typing import Any, List, Optional

import requests
from requests import Response

from kodexa.model import ContentObject, Document, DocumentFamily, DocumentStore, DocumentTransition, ModelStore, \
    RemoteStore
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

    def get_parent_df(self, parent: str, query: str = "*", document_family: Optional[DocumentFamily] = None):
        """

        Args:
          parent (str): The parent taxon (/ is root)
          query (str): A query to limit the results (Defaults to *)
          document_family (Optional[DocumentFamily): Optionally the document family to limit results to
        Returns:

        """
        import pandas as pd

        table_result = self.get_parent(parent, query, document_family)
        return pd.DataFrame(table_result['rows'], columns=table_result['columns'])

    def get_parent(self, parent: str, query: str = "*", document_family: Optional[DocumentFamily] = None):
        """

        Args:
          parent (str): The parent taxon (/ is root)
          query (str): A query to limit the results (Default *)
          document_family (Optional[DocumentFamily): Optionally the document family to limit results to
        Returns:

        """

        # We need to get the first set of rows,
        rows: List = []
        row_response = self.get_parent_page_request(parent, 1, document_family=document_family)

        # lets work out the last page
        rows = rows + row_response['content']
        total_pages = row_response['totalPages']

        for page in range(2, total_pages):
            row_response = self.get_parent_page_request(parent, page, query=query, document_family=document_family)
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

    def get_parent_page_request(self, parent: str, page_number: int = 1, page_size=5000, query="*",
                                document_family: Optional[DocumentFamily] = None):
        """

        Args:
          parent (str): The parent taxon (/ is root)
          page_number (int):  (Default value = 1)
          page_size (int):  (Default value = 5000)
          query (str): The query to limit results (Default *)
          document_family (Optional[DocumentFamily): Optionally the document family to limit results to

        Returns:

        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/rows"
        logger.debug(f"Downloading a specific table from {url}")

        # We need to go through and pull all the pages
        params = {"parent": parent, "page": page_number, "pageSize": page_size, "query": query}

        if document_family:
            params['documentFamilyId'] = document_family.id
            params['storeRef'] = document_family.store_ref

        rows_response = requests.get(
            url,
            params=params,
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
          rows: A list of rows that you want to post

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
          TableDataStore, DictDataStore, or None: A TableDataStore or DictDataStore - driven from 'type' in doc_dict.
          If 'type' is not present or does not align with one of these two types, None is returend.

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

    def __init__(self, ref: str):

        self.ref: str = ref

        get_response = self._base_get(
            f"api/stores/{self.ref.replace(':', '/')}")

        if get_response is not None:
            self.store_type = get_response.json()['storeType']
            self.store_purpose = get_response.json()['storePurpose']
        else:
            # we couldn't find metadata for this store, so we're setting default values
            self.store_type = 'DOCUMENT'
            self.store_purpose = 'OPERATIONAL'

        super().__init__(self.store_type, self.store_purpose)

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
            "ref": self.ref,
            "storeType": self.store_type,
            "storePurpose": self.store_purpose
        }

    def delete(self, path: str):
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Deleting document family at path {path}")

            document_family_response = requests.delete(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs/{path}",
                headers={"x-access-token": KodexaPlatform.get_access_token()}, )

            if document_family_response.status_code == 200:
                return True
            else:
                return False
        except JSONDecodeError:
            logger.error(
                "Unable to decode the JSON response")
            raise

    def get_family(self, document_family_id: str) -> Optional[DocumentFamily]:
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Getting document family id {document_family_id}")
            document_family_response = requests.get(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/families/{document_family_id}",
                headers={"x-access-token": KodexaPlatform.get_access_token()})

            if document_family_response.status_code == 200:
                return DocumentFamily.from_dict(document_family_response.json())
            else:
                msg = "Get document family failed [" + document_family_response.text + "], response " + str(
                    document_family_response.status_code)
                logger.error(msg)
                raise Exception(msg)
        except JSONDecodeError:
            logger.error(
                "Unable to decode the JSON response")
            raise

    def add_related_document_to_family(self, document_family_id: str, transition: DocumentTransition,
                                       document: Document):
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Putting document to family id {document_family_id}")

            data = {'transitionType': str(transition.transition_type),
                    'sourceContentObjectId': transition.source_content_object_id}
            files = {"document": document.to_msgpack()}
            document_family_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/families/{document_family_id}/objects",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                data=data,
                files=files)

            if document_family_response.status_code == 200:
                return DocumentFamily.from_dict(document_family_response.json())
            else:
                msg = "Document family create failed [" + document_family_response.text + "], response " + str(
                    document_family_response.status_code)
                logger.error(msg)
                raise Exception(msg)
        except JSONDecodeError:
            logger.error(
                "Unable to decode the JSON response")
            raise

    def get_document_by_content_object(self, document_family: DocumentFamily, content_object: ContentObject) -> \
            Optional[Document]:
        get_response = self._base_get(
            f"api/stores/{self.ref.replace(':', '/')}/families/{document_family.id}/objects/{content_object.id}/content")
        return Document.from_msgpack(get_response.content) if get_response is not None else None

    def get_source_by_content_object(self, document_family: DocumentFamily, content_object: ContentObject) -> \
            Any:
        get_response = self._base_get(
            f"api/stores/{self.ref.replace(':', '/')}/families/{document_family.id}/objects/{content_object.id}/content")
        return get_response.content if get_response is not None else None

    def register_listener(self, listener):
        pass

    def query_families(self, query: str = "*", page: int = 1, page_size: int = 100) -> List[DocumentFamily]:
        params = {
            'page': page,
            'pageSize': page_size,
            'query': query
        }
        get_response = self._base_get(f"api/stores/{self.ref.replace(':', '/')}/families", params=params)
        if get_response is not None:
            families = []
            for fam_dict in get_response.json()['content']:
                families.append(DocumentFamily.from_dict(fam_dict))
            return families
        else:
            return []

    def replace_content_object(self, document_family: DocumentFamily, content_object_id: str,
                               document: Document) -> DocumentFamily:
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Replacing document in family {document_family.id} content object {content_object_id}")

            files = {"document": document.to_msgpack()}
            content_object_replace = requests.put(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/families/{document_family.id}/objects/{content_object_id}/content",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files)

            if content_object_replace.status_code == 200:
                return DocumentFamily.from_dict(content_object_replace.json())
            else:
                msg = "Document replace failed [" + content_object_replace.text + "], response " + str(
                    content_object_replace.status_code)
                logger.error(msg)
                raise Exception(msg)
        except JSONDecodeError:
            logger.error(
                "Unable to decode the JSON response")
            raise

    def put(self, path: str, document: Document, force_replace: bool = False) -> DocumentFamily:
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Putting document to path {path}")

            files = {"document": document.to_msgpack()}
            data = {"path": path, "forceReplace": force_replace}
            document_family_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs/{path}",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files, data=data)

            if document_family_response.status_code == 200:
                return DocumentFamily.from_dict(document_family_response.json())
            else:
                msg = "Document family create failed [" + document_family_response.text + "], response " + str(
                    document_family_response.status_code)
                logger.error(msg)
                raise Exception(msg)
        except JSONDecodeError:
            logger.error(
                "Unable to decode the JSON response")
            raise

    def put_native(self, path: str, content, force_replace: bool = False) -> DocumentFamily:
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Putting native content to path {path}")

            files = {"file": content}
            data = {"path": path, "forceReplace": force_replace}
            document_family_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs/{path}",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files, data=data)

            if document_family_response.status_code == 200:
                return DocumentFamily.from_dict(document_family_response.json())
            else:
                msg = "Document family create failed [" + document_family_response.text + "], response " + str(
                    document_family_response.status_code)
                logger.error(msg)
                raise Exception(msg)
        except JSONDecodeError:
            logger.error(
                "Unable to decode the JSON response")
            raise

    def get_family_by_path(self, path: str) -> Optional[DocumentFamily]:
        get_response = self._base_get(f"api/stores/{self.ref.replace(':', '/')}/fs/{path}", params={"meta": True})
        return DocumentFamily.from_dict(get_response.json()) if get_response is not None else None

    def count(self) -> int:
        get_response = self._base_get(f"api/stores/{self.ref.replace(':', '/')}/families")
        if get_response is not None:
            return get_response.json()['totalElements']
        else:
            return 0

    def get_by_content_object_id(self, document_family: DocumentFamily, content_object_id: str) -> Optional[Document]:
        get_response = self._base_get(
            f"api/stores/{self.ref.replace(':', '/')}/families/{document_family.id}/objects/{content_object_id}/content")
        if get_response is not None:
            return Document.from_msgpack(get_response.content)
        else:
            return None

    def _base_get(self, api_path: str, params: Optional[dict] = None) -> Optional[Response]:
        if params is None:
            params = {}
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/{api_path}"
        logger.info(f"Accessing {url}")

        get_response = requests.get(
            url,
            params=params,
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if get_response.status_code == 200:
            return get_response
        elif get_response.status_code == 404:
            return None
        else:
            msg = "Get failed [" + get_response.text + "], response " + str(get_response.status_code)
            logger.error(msg)
            raise Exception(msg)


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
        """
        Delete the content stored in the model store at the given path

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
