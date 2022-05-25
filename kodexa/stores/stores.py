"""
Remote stores allow you to interact with an instance of the Kodexa platform
"""

import json
import logging
from json import JSONDecodeError
from typing import Any, List, Optional

import requests

from kodexa.model import ContentObject, Document, DocumentFamily, DocumentStore, DocumentTransition, ModelStore, Store
from kodexa.model.model import ModelContentMetadata

logger = logging.getLogger()


class RemoteDataStore(Store):
    """ """

    def get_ref(self):
        """ """
        return self.ref

    def get_data_objects_df(self, path: str, query: str = "*", document_family: Optional[DocumentFamily] = None,
                            include_id: bool = False):
        """

        Args:
          path (str): The path to the data object
          query (str): A query to limit the results (Defaults to *)
          document_family (Optional[DocumentFamily): Optionally the document family to limit results to
          include_id (Optional[bool]): Include the data object ID as a column (defaults to False)
        Returns:

        """
        import pandas as pd

        data_objects = self.get_data_objects(path, query, document_family)

        table_result = {
            'rows': [],
            'columns': [],
            'column_headers': []
        }

        for data_object in data_objects:
            if len(table_result['columns']) == 0:
                if include_id:
                    table_result['column_headers'].append('Data Object ID')
                    table_result['columns'].append('data_object_id')
                for taxon in data_object['taxon']['children']:
                    if not taxon['group']:
                        table_result['column_headers'].append(taxon['label'])
                        table_result['columns'].append(taxon['name'])

            new_row = []
            for column in table_result['columns']:
                column_value = None
                if include_id:
                    if column == 'data_object_id':
                        column_value = data_object['id']
                for attribute in data_object['attributes']:
                    if attribute['tag'] == column:
                        column_value = attribute['stringValue']
                new_row.append(column_value)

            table_result['rows'].append(new_row)

        return pd.DataFrame(table_result['rows'], columns=table_result['column_headers'])

    def update_data_object_attribute(self, data_object, attribute):
        """

        Args:
          data_object (DataObject): The data object to update
          attribute (Attribute): The attribute to update

        Returns:

        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/dataObjects/{data_object.id}/attributes/{attribute.id}"
        logger.info(f"Downloading a specific data object from {url}")

        data_object_response = requests.put(
            url,
            data=attribute.json(by_alias=True),
            headers={"x-access-token": KodexaPlatform.get_access_token(), "content-type": "application/json"})

        if data_object_response.status_code == 200:
            from kodexa.model.objects import DataObject
            return DataObject(**data_object_response.json())

        logger.warning(
            "Unable to update data attribute status [" + data_object_response.text + "], response " + str(
                data_object_response.status_code))
        raise Exception(
            "Unable to update data attribute status [" + data_object_response.text + "], response " + str(
                data_object_response.status_code))

    def get_data_objects(self, path: str, query: str = "*", document_family: Optional[DocumentFamily] = None):
        """

        Args:
          path (str): The path to the data object
          query (str): A query to limit the results (Default *)
          document_family (Optional[DocumentFamily): Optionally the document family to limit results to
        Returns:

        """

        # We need to get the first set of rows,
        rows: List = []
        row_response = self.get_data_objects_page_request(path, 1, document_family=document_family)

        # lets work out the last page
        rows = rows + row_response['content']
        total_pages = row_response['totalPages']

        for page in range(2, total_pages):
            row_response = self.get_data_objects_page_request(path, page, query=query, document_family=document_family)
            rows = rows + row_response['content']

        return rows

    def get_data_object(self, data_object_id: str):
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/dataObjects/{data_object_id}"
        logger.info(f"Downloading a specific data object from {url}")

        data_object_response = requests.get(
            url,
            headers={"x-access-token": KodexaPlatform.get_access_token(), "content-type": "application/json"})

        print(data_object_response)
        if data_object_response.status_code == 200:
            from kodexa.model.objects import DataObject
            return DataObject(**data_object_response.json())

        logger.warning(
            "Unable to get data object from remote store [" + data_object_response.text + "], response " + str(
                data_object_response.status_code))
        raise Exception(
            "Unable to get data object from remote store  [" + data_object_response.text + "], response " + str(
                data_object_response.status_code))

    def get_data_objects_page_request(self, path: str, page_number: int = 1, page_size=5000, query="*",
                                      document_family: Optional[DocumentFamily] = None):
        """

        Args:
          path (str): The parent taxon (/ is root)
          page_number (int):  (Default value = 1)
          page_size (int):  (Default value = 5000)
          query (str): The query to limit results (Default *)
          document_family (Optional[DocumentFamily): Optionally the document family to limit results to

        Returns:

        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        logger.debug(f"Downloading a specific table from {url}")

        # We need to go through and pull all the pages
        params = {"path": path, "page": page_number, "pageSize": page_size, "query": query}

        if document_family:
            params['documentFamilyId'] = document_family.id
            params['storeRef'] = document_family.store_ref

        rows_response = requests.get(
            url,
            params=params,
            headers={"x-access-token": KodexaPlatform.get_access_token(), "content-type": "application/json"})

        if rows_response.status_code == 200:
            return rows_response.json()

        logger.warning("Unable to get table from remote store [" + rows_response.text + "], response " + str(
            rows_response.status_code))
        raise Exception("Unable to get table from remote store  [" + rows_response.text + "], response " + str(
            rows_response.status_code))

    def add_data_objects(self, rows):
        """

        Args:
          rows: A list of rows that you want to post

        Returns:

        """
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        logger.debug(f"Uploading rows to store {url}")

        doc = requests.post(
            url,
            json=rows,
            headers={"x-access-token": KodexaPlatform.get_access_token(), "content-type": "application/json"})
        if doc.status_code == 200:
            return

        logger.warning(
            "Unable to post data objects to remote store [" + doc.text + "], response " + str(doc.status_code))
        raise Exception(
            "Unable to post data objects to remote store [" + doc.text + "], response " + str(doc.status_code))

    def add(self, row):
        from kodexa import KodexaPlatform

        url = f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        logger.debug(f"Uploading data objects to store {url}")

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

        logger.warning("Unable to post rows to remote store [" + doc.text + "], response " + str(doc.status_code))
        raise Exception("Unable to post rows to remote store [" + doc.text + "], response " + str(doc.status_code))


class RemoteDocumentStore(DocumentStore):
    """
    Remote Document Stores provide you with all the capabilities of Document storage and relationships
    in an instance of the Kodexa platform
    """

    def get_ref(self) -> str:
        return self.ref

    def delete(self, path: str):
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Deleting document family at path {path}")

            document_family_response = requests.delete(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs",
                params={"path": path},
                headers={"x-access-token": KodexaPlatform.get_access_token()}, )

            if document_family_response.status_code == 200:
                return True

            return False
        except JSONDecodeError:
            logger.warning(
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
                return DocumentFamily.parse_obj(document_family_response.json())

            msg = "Get document family failed [" + document_family_response.text + "], response " + str(
                document_family_response.status_code)
            logger.warning(msg)
            raise Exception(msg)
        except JSONDecodeError:
            logger.warning(
                "Unable to decode the JSON response")
            raise

    def update_document_family_status(self, document_family, status):
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Updating the status of {document_family.id}")
            document_family_response = requests.put(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/families/{document_family.id}/status",
                headers={"x-access-token": KodexaPlatform.get_access_token(), "content-type": "application/json"},
                data=status.json(by_alias=True))

            if document_family_response.status_code == 200:
                return DocumentFamily(**document_family_response.json())

            msg = "Document family update failed [" + document_family_response.text + "], response " + str(
                document_family_response.status_code)
            logger.warning(msg)
            raise Exception(msg)
        except JSONDecodeError:
            logger.warning(
                "Unable to decode the JSON response")
            raise

    def add_related_document_to_family(self, document_family_id: str, transition: DocumentTransition,
                                       document: Document) -> ContentObject:
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Putting document to family id {document_family_id}")

            data = {'transitionType': transition.transition_type.value,
                    'documentVersion': document.version,
                    'document': True,
                    'sourceContentObjectId': transition.source_content_object_id}
            files = {"file": document.to_kddb()}
            document_family_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/families/{document_family_id}/objects",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                data=data,
                files=files)

            if document_family_response.status_code == 200:
                return ContentObject.parse_obj(document_family_response.json())

            msg = "Document family create failed [" + document_family_response.text + "], response " + str(
                document_family_response.status_code)
            logger.warning(msg)
            raise Exception(msg)
        except JSONDecodeError:
            logger.warning(
                "Unable to decode the JSON response")
            raise

    def get_document_by_content_object(self, document_family: DocumentFamily, content_object: ContentObject) -> \
            Optional[Document]:
        from kodexa import KodexaPlatform
        get_response = KodexaPlatform.get_client().get(
            f"api/stores/{self.ref.replace(':', '/')}/families/{document_family.id}/objects/{content_object.id}/content")
        return Document.from_kddb(get_response.content) if get_response is not None else None

    def get_source_by_content_object(self, document_family: DocumentFamily, content_object: ContentObject) -> \
            Any:
        from kodexa import KodexaPlatform
        get_response = KodexaPlatform.get_client().get(
            f"api/stores/{self.ref.replace(':', '/')}/families/{document_family.id}/objects/{content_object.id}/content")
        return get_response.content if get_response is not None else None

    def register_listener(self, listener):
        pass

    def query_families(self, query: str = "*", page: int = 1, page_size: int = 100, sort=None) -> List[DocumentFamily]:
        params = {
            'page': page,
            'pageSize': page_size,
            'query': query
        }

        if sort is not None:
            params.sort = sort

        from kodexa import KodexaPlatform
        get_response = KodexaPlatform.get_client().get(f"api/stores/{self.ref.replace(':', '/')}/families",
                                                       params=params)
        if get_response is not None:
            families = []
            for fam_dict in get_response.json()['content']:
                families.append(DocumentFamily.parse_obj(fam_dict))
            return families

        return []

    def replace_content_object(self, document_family: DocumentFamily, content_object_id: str,
                               document: Document) -> DocumentFamily:
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Replacing document in family {document_family.id} content object {content_object_id}")

            files = {"file": document.to_kddb()}
            content_object_replace = requests.put(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/families/{document_family.id}/objects/{content_object_id}/content",

                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files)

            if content_object_replace.status_code == 200:
                return DocumentFamily.parse_obj(content_object_replace.json())

            msg = "Document replace failed [" + content_object_replace.text + "], response " + str(
                content_object_replace.status_code)
            logger.warning(msg)
            raise Exception(msg)
        except JSONDecodeError:
            logger.warning(
                "Unable to decode the JSON response")
            raise

    def put(self, path: str, document: Document) -> DocumentFamily:
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Putting document to path {path}")

            files = {"file": document.to_kddb()}
            data = {"path": path, "documentVersion": document.version, "document": True}
            document_family_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs",
                params={"path": path},
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files, data=data)

            if document_family_response.status_code == 200:
                return DocumentFamily.parse_obj(document_family_response.json())

            msg = "Document family create failed [" + document_family_response.text + "], response " + str(
                document_family_response.status_code)
            logger.warning(msg)
            raise Exception(msg)
        except JSONDecodeError:
            logger.warning(
                "Unable to decode the JSON response")
            raise

    def put_native(self, path: str, content) -> DocumentFamily:
        from kodexa import KodexaPlatform
        try:
            logger.info(f"Putting native content to path {path}")

            files = {"file": content}
            document_family_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs",
                params={"path": path, "document": False},
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files)

            if document_family_response.status_code == 200:
                return DocumentFamily.parse_obj(document_family_response.json())

            msg = "Document family create failed [" + document_family_response.text + "], response " + str(
                document_family_response.status_code)
            logger.warning(msg)
            raise Exception(msg)
        except JSONDecodeError:
            logger.warning(
                "Unable to decode the JSON response")
            raise

    def get_family_by_path(self, path: str) -> Optional[DocumentFamily]:
        from kodexa import KodexaPlatform
        get_response = KodexaPlatform.get_client().get(f"api/stores/{self.ref.replace(':', '/')}/fs",
                                                       params={"path": path, "meta": True})
        return DocumentFamily.parse_obj(get_response.json()) if get_response is not None else None

    def count(self) -> int:
        from kodexa import KodexaPlatform
        get_response = KodexaPlatform.get_client().get(f"api/stores/{self.ref.replace(':', '/')}/families")
        if get_response is not None:
            return get_response.json()['totalElements']

        return 0

    def get_by_content_object_id(self, document_family: DocumentFamily, content_object_id: str) -> Optional[Document]:
        from kodexa import KodexaPlatform
        get_response = KodexaPlatform.get_client().get(
            f"api/stores/{self.ref.replace(':', '/')}/families/{document_family.id}/objects/{content_object_id}/content")
        if get_response is not None:
            return Document.from_kddb(get_response.content)

        return None


class RemoteModelStore(ModelStore):
    """
    A remote model store allows you to store artifacts from your model
    """

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
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": object_path},
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if resp.status_code == 200:
            return True
        if resp.status_code == 404:
            return False

        msg = f"Unable to delete model object {resp.text}, status : {resp.status_code}"
        logger.warning(msg)
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
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": object_path},
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if resp.status_code == 200:
            return resp.content

        msg = f"Unable to get model object {resp.text}, status : {resp.status_code}"
        logger.warning(msg)
        raise Exception(msg)

    def put(self, path: str, content, replace=False) -> DocumentFamily:
        """Put the content into the model store at the given path

        Args:
          path: The path you wish to put the content at
          content: The content for that object
          replace: Replace the content if it exists

        Returns:
          the document family that was created
        """
        from kodexa import KodexaPlatform
        import requests
        try:
            files = {"file": content}

            if replace:
                delete_response = requests.delete(
                    f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs",
                    params={"path": path},
                    headers={"x-access-token": KodexaPlatform.get_access_token()})
                logger.info(f"Deleting {path} ({delete_response.status_code})")

            content_object_response = requests.post(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/fs",
                params={"path": path},
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                files=files)
            logger.info(f"Uploaded {path} ({content_object_response.status_code})")
            if content_object_response.status_code == 200:
                return DocumentFamily.parse_obj(content_object_response.json())
            if content_object_response.status_code == 400:
                from addict import Dict
                bad_request = Dict(json.loads(content_object_response.text))
                for error_key in bad_request.errors.keys():
                    print(bad_request.errors[error_key] + " (" + error_key + ")")
                raise Exception("Invalid request")

            msg = "Execution creation failed [" + content_object_response.text + "], response " + str(
                content_object_response.status_code)
            logger.warning(msg)
            raise Exception(msg)
        except JSONDecodeError:
            logger.warning(
                "Unable to JSON decode the response?")
            raise

    def set_content_metadata(self, model_content_metadata: ModelContentMetadata):
        """
        Updates the model content metadata for the model store

        :param model_content_metadata: The metadata object
        """
        from kodexa import KodexaPlatform
        import requests
        try:
            model_content_metadata.type = "model"
            content_object_response = requests.put(
                f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/metadata",
                headers={"x-access-token": KodexaPlatform.get_access_token()},
                json=model_content_metadata.dict(by_alias=True))

            if content_object_response.status_code == 200:
                return model_content_metadata
            if content_object_response.status_code == 400:
                from addict import Dict
                bad_request = Dict(json.loads(content_object_response.text))
                for error_key in bad_request.errors.keys():
                    print(bad_request.errors[error_key] + " (" + error_key + ")")
                raise Exception("Invalid request")

            msg = "Execution creation failed [" + content_object_response.text + "], response " + str(
                content_object_response.status_code)
            logger.warning(msg)
            raise Exception(msg)
        except JSONDecodeError:
            logger.warning(
                "Unable to JSON decode the response?")
            raise

    def get_content_metadata(self) -> ModelContentMetadata:
        """
        Gets the latest model content metadata for the model store

        :return: the model content metadata
        """
        from kodexa import KodexaPlatform
        import requests
        resp = requests.get(
            f"{KodexaPlatform.get_url()}/api/stores/{self.ref.replace(':', '/')}/metadata",
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if resp.status_code == 200:
            return ModelContentMetadata.parse_obj(resp.json())

        msg = f"Unable to get model object {resp.text}, status : {resp.status_code}"
        logger.warning(msg)
        raise Exception(msg)

    def list_contents(self) -> List[str]:

        # TODO this needs to be cleaned up a bit
        params = {
            'page': 1,
            'pageSize': 1000,
            'query': '*'
        }
        from kodexa import KodexaPlatform
        get_response = KodexaPlatform.get_client().get(f"api/stores/{self.ref.replace(':', '/')}/families",
                                                       params=params)
        if get_response is not None:
            paths = []
            for fam_dict in get_response.json()['content']:
                paths.append(fam_dict['path'])
            return paths

        return []