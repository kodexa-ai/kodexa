#  Copyright (c) 2022. Kodexa Inc
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import glob
import json
import logging
import os
from pathlib import Path
from typing import Type, Optional, List

import requests
from functional import seq
from pydantic import BaseModel

from kodexa.model import Store, Taxonomy
from kodexa.model.objects import PageStore, PageTaxonomy, PageProject, PageOrganization, Project, Organization, \
    PlatformOverview, DocumentFamily, DocumentContentMetadata, ModelContentMetadata

logger = logging.getLogger()


class ComponentEndpoint:
    """
    Represents a re-usable endpoint for a component (stores, taxonomies etc)
    """

    def __init__(self, client: "KodexaClient", organization: "OrganizationEndpoint"):
        self.client: "KodexaClient" = client
        self.organization: "OrganizationEndpoint" = organization

    def get_type(self) -> str:
        pass

    def get_instance_class(self) -> Type[BaseModel]:
        pass

    def get_page_class(self) -> Type[BaseModel]:
        pass

    def find_by_slug(self, slug) -> Optional[Type[BaseModel]]:
        component_page = self.list(filters=["slug=" + slug])
        if component_page.empty:
            return None
        else:
            return component_page.content[0]

    def list(self, query="*", page=1, pagesize=10, sort=None):
        url = f"/api/{self.get_type()}/{self.organization.slug}"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort

        list_response = self.client.get(url, params=params)
        return self.get_page_class().parse_obj(**list_response.json())

    def get(self, slug, version=None):
        url = f"/api/{self.get_type()}/{self.organization.slug}/{slug}"
        if version is not None:
            url += f"/{version}"

        get_response = self.client.get(url)
        return self.get_instance_class().parse_obj(**get_response.json())


class OrganizationsEndpoint:
    """
    Represents the organization endpoint
    """

    def __init__(self, client: "KodexaClient"):
        self.client: "KodexaClient" = client

    def reindex(self):
        url = f'/api/organizations/_reindex'
        self.client.post(url)

    def create(self, organization: Organization) -> Organization:
        url = f"/api/organizations"
        create_response = self.client.post(url, body=json.loads(organization.json()))
        return Organization.parse_obj(create_response.json())

    def find_by_slug(self, slug) -> Optional["OrganizationEndpoint"]:
        organizations = self.list(filters=["slug=" + slug])
        if organizations.number_of_elements == 0:
            return None
        else:
            return OrganizationEndpoint.parse_obj(organizations.content[0].dict()).set_client(self.client)

    def delete(self, id: str) -> None:
        url = f"/api/organizations/{id}"
        self.client.delete(url)

    def list(self, query: str = "*", page: int = 1, pagesize: int = 10, sort: Optional[str] = None,
             filters: Optional[List[str]] = None) -> PageOrganization:
        url = f"/api/organizations"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort
        if filters is not None:
            params["filter"] = filters

        list_response = self.client.get(url, params=params)
        return PageOrganization.parse_obj(list_response.json())

    def get(self, organization_id) -> Organization:
        url = f"/api/organizations/{organization_id}"
        get_response = self.client.get(url)
        return OrganizationEndpoint.parse_obj(**get_response.json()).set_client(self.client)


class ClientEndpoint(BaseModel):
    client: Optional["KodexaClient"] = None

    def set_client(self, client):
        self.client = client
        return self

    def to_dict(self):
        return json.loads(self.json(exclude={'client'}, by_alias=True))


class OrganizationEndpoint(Organization, ClientEndpoint):

    def apply(self, component: ComponentEndpoint) -> "ComponentInstanceEndpoint":
        url = f"/api/{component.get_type()}/{self.slug}"
        response = self.client.post(url, body=self.to_dict())
        return self.client.deserialize(response.json())


class ComponentInstanceEndpoint(ClientEndpoint):

    def get_type(self) -> str:
        raise NotImplementedError()

    def post_deploy(self):
        pass

    def deploy(self, update=False):
        if self.org_slug is None:
            raise Exception("We can not deploy this component since it does not have an organization")
        if self.slug is None:
            raise Exception("We can not deploy this component since it does not have a slug")

        self.ref = f"{self.org_slug}/{self.slug}{f':{self.version}' if self.version is not None else ''}"

        url = f"/api/{self.get_type()}/{self.ref.replace(':', '/')}"
        exists = self.client.exists(url)
        if not update and exists:
            raise Exception("Component already exists")
        if exists:
            self.client.put(url, self.to_dict())
            self.post_deploy()
        else:
            self.client.post(url, self.to_dict())
            self.post_deploy()


class ProjectEndpoint(ClientEndpoint, Project):

    def _get_resource(self, resource_type: str) -> List[ComponentInstanceEndpoint]:
        url = f"/api/projects/{self.id}/{resource_type}"
        response = self.client.get(url)
        return [self.client.deserialize(store) for store in response.json()]

    def stores(self, store_type=None, store_purpose=None) -> List[ComponentInstanceEndpoint]:
        return (seq(self._get_resource("stores"))
                .filter(lambda store: store_type is None or store.store_type == store_type)
                .filter(lambda store: store_type is None or store.store_purpose == store_purpose))

    def taxonomies(self) -> List[ComponentInstanceEndpoint]:
        return self._get_resource("taxonomies")


class ProjectsEndpoint:

    def __init__(self, client: "KodexaClient", organization: "OrganizationEndpoint" = None):
        self.client: "KodexaClient" = client
        self.organization: Optional["OrganizationEndpoint"] = organization

    def reindex(self):
        url = f'/api/projects/_reindex'
        self.client.post(url)

    def list(self, query="*", page=1, pagesize=10, sort=None):
        url = f"/api/projects"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort

        list_response = self.client.get(url, params=params)
        return PageProject.parse_obj(**list_response.json())

    def get(self, project_id: str) -> Project:
        url = f"/api/projects/{project_id}"
        get_response = self.client.get(url)
        return ProjectEndpoint.parse_obj(**get_response.json()).set_client(self.client)

    def create(self, project: Project, template_ref: str = None) -> Project:
        url = f"/api/projects"

        if template_ref is not None:
            params = {"templateRef": template_ref}
        else:
            params = None

        create_response = self.client.post(url, body=json.loads(project.json()), params=params)
        return ProjectEndpoint.parse_obj(create_response.json()).set_client(self.client)

    def delete(self, id: str) -> None:
        url = f"/api/projects/{id}"
        self.client.delete(url)


class StoresEndpoint(ComponentEndpoint):
    def get_type(self) -> str:
        return "stores"

    def get_page_class(self) -> Type[BaseModel]:
        return PageStore


class TaxonomyEndpoint(ComponentInstanceEndpoint, Taxonomy):

    def get_type(self) -> str:
        return "taxonomies"


class StoreEndpoint(ComponentInstanceEndpoint, Store):

    def get_type(self) -> str:
        return "stores"

    def get_metadata_class(self) -> Optional[Type[BaseModel]]:
        return None

    def set_metadata(self, metadata):
        pass

    def upload_contents(self, metadata):
        pass

    def update_metadata(self):
        self.client.put(f"/api/stores/{self.ref.replace(':', '/')}/metadata", body=json.loads(self.metadata.json()))

    def get_metadata(self):
        metadata_response = self.client.get(f"/api/stores/{self.ref.replace(':', '/')}/metadata")
        return self.get_metadata_class().parse_obj(**metadata_response.json()) if self.get_metadata_class() else None

    def post_deploy(self):
        if self.metadata:
            # We need to determine in the subclass if we wil be uploading the
            # contents
            self.upload_contents(self.metadata)


class DataStoreEndpoint(StoreEndpoint):

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
        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects/{data_object.id}/attributes/{attribute.id}"
        logger.info(f"Downloading a specific data object from {url}")

        data_object_response = self.client.put(
            url, body=attribute.json(by_alias=True))
        from kodexa.model.objects import DataObject
        return DataObject(**data_object_response.json())

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

        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects/{data_object_id}"
        logger.info(f"Downloading a specific data object from {url}")

        data_object_response = self.client.get(url)
        from kodexa.model.objects import DataObject
        return DataObject(**data_object_response.json())

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
        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        logger.debug(f"Downloading a specific table from {url}")

        # We need to go through and pull all the pages
        params = {"path": path, "page": page_number, "pageSize": page_size, "query": query}

        if document_family:
            params['documentFamilyId'] = document_family.id
            params['storeRef'] = document_family.store_ref

        rows_response = self.client.get(url, params=params)

        # TODO this needs to return real objects
        return rows_response.json()

    def add_data_objects(self, rows):
        """

        Args:
          rows: A list of rows that you want to post

        Returns:

        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        logger.debug(f"Uploading data objects to store {url}")

        doc = requests.post(url, json=rows)

    def add(self, row):
        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        logger.debug(f"Uploading data objects to store {url}")

        row_dict = {}
        for idx, row_value in enumerate(row):
            if len(self.columns) == 0 or len(self.columns) <= idx:
                row_dict[f'col{idx}'] = row_value
            else:
                row_dict[self.columns[idx]] = row_value

        doc = requests.post(url, json=[{'data': row_dict}])


class DocumentStoreEndpoint(StoreEndpoint):

    def delete_by_path(self, object_path: str):
        """
        Delete the content stored in the store at the given path

        Args:
          object_path: the path to the content (ie. mymodel.dat)
          object_path: str:
        """
        self.client.delete(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": object_path})

    def upload_bytes(self, path: str, content, replace=False) -> DocumentFamily:
        """
        Put the content into the store at the given path

        Args:
          path: The path you wish to put the content at
          content: The content for that object
          replace: Replace the content if it exists

        Returns:
          the document family that was created
        """
        files = {"file": content}

        if replace and self.client.exists(f"/api/stores/{self.ref.replace(':', '/')}/fs", params={"path": path}):
            delete_response = self.client.delete(
                f"/api/stores/{self.ref.replace(':', '/')}/fs",
                params={"path": path})
            logger.info(f"Deleting {path}")

        content_object_response = self.client.post(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": path},
            files=files)
        logger.info(f"Uploaded {path} ({content_object_response.status_code})")
        return DocumentFamily.parse_obj(content_object_response.json())

    def get_bytes(self, object_path: str):
        """Get the bytes for the object at the given path, will return None if there is no object there

        Args:
          object_path: the object path
          object_path: str:

        Returns:
          the bytes or None is nothing is at the path

        """
        return self.client.get(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": object_path}).content

    def list_contents(self) -> List[str]:

        # TODO this needs to be cleaned up a bit
        params = {
            'page': 1,
            'pageSize': 1000,
            'query': '*'
        }
        get_response = self.client.get(f"api/stores/{self.ref.replace(':', '/')}/families",
                                       params=params)
        paths = []
        for fam_dict in get_response.json()['content']:
            paths.append(fam_dict['path'])
        return paths

    def get_metadata_class(self) -> Type[BaseModel]:
        return DocumentContentMetadata

    def put(self, path: str, content, replace=False) -> DocumentFamily:
        """Put the content into the store at the given path

        Args:
          path: The path you wish to put the content at
          content: The content for that object
          replace: Replace the content if it exists

        Returns:
          the document family that was created
        """
        files = {"file": content}

        if replace:
            self.client.delete(
                f"/api/stores/{self.ref.replace(':', '/')}/fs",
                params={"path": path})
            logger.info(f"Deleted {path}")

        content_object_response = self.client.post(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": path},
            files=files)
        logger.info(f"Uploaded {path}")
        return DocumentFamily.parse_obj(**content_object_response.json())


class ModelStoreEndpoint(DocumentStoreEndpoint):

    def get_metadata_class(self) -> Type[BaseModel]:
        return ModelContentMetadata

    def upload_contents(self, metadata):
        if metadata.contents:
            for content_path in metadata.contents:
                final_wildcard = os.path.join(metadata.base_dir, content_path) if metadata.base_dir else content_path
                for path_hit in glob.glob(final_wildcard):
                    path_hit = path_hit.replace(metadata.base_dir, '') if metadata.base_dir else path_hit
                    if Path(path_hit).is_file():
                        logger.info(f"Uploading {path_hit}")
                        with open(path_hit, 'rb') as path_content:
                            self.upload_bytes(path_hit, path_content, replace=True)


class TaxonomiesEndpoint(ComponentEndpoint):
    def get_type(self) -> str:
        return "taxonomies"

    def get_page_class(self) -> Type[BaseModel]:
        return PageTaxonomy

    def get_instance_class(self) -> Type[BaseModel]:
        return Taxonomy


def process_response(response) -> requests.Response:
    if response.status_code == 401:
        raise Exception("Unauthorized")
    if response.status_code == 404:
        raise Exception("Not found")
    if response.status_code == 405:
        raise Exception("Method not allowed")
    if response.status_code == 500:
        raise Exception("Internal server error")
    if response.status_code == 400:
        if response.json() and response.json().get("errors"):
            raise Exception(', '.join(response.json()["errors"].values()))
        else:
            raise Exception("Bad request " + response.text)
    return response


class KodexaClient:

    def __init__(self, url=None, access_token=None):
        from kodexa import KodexaPlatform
        self.base_url = url if url is not None else KodexaPlatform.get_url()
        self.access_token = access_token if access_token is not None else KodexaPlatform.get_access_token()
        self.organizations = OrganizationsEndpoint(self)
        self.projects = ProjectsEndpoint(self)

    def get_platform(self):
        return PlatformOverview.parse_obj(self.get(f"{self.base_url}/api").json())

    def exists(self, url, params=None) -> bool:
        response = requests.get(self.get_url(url), params=params, headers={"x-access-token": self.access_token,
                                                                           "content-type": "application/json"})
        if response.status_code == 200 or response.status_code == 404:
            return response.status_code == 200
        else:
            process_response(response)

    def get(self, url, params=None) -> requests.Response:
        response = requests.get(self.get_url(url), params=params, headers={"x-access-token": self.access_token,
                                                                           "content-type": "application/json"})
        return process_response(response)

    def post(self, url, data=None, body=None, files=None, params=None) -> requests.Response:
        response = requests.post(self.get_url(url), json=body, data=data, files=files, params=params,
                                 headers={"x-access-token": self.access_token,
                                          "content-type": "application/json"})
        return process_response(response)

    def put(self, url, body=None) -> requests.Response:
        response = requests.put(self.get_url(url), json=body, headers={"x-access-token": self.access_token,
                                                                       "content-type": "application/json"})
        return process_response(response)

    def delete(self, url, params=None) -> requests.Response:
        response = requests.delete(self.get_url(url), params=params, headers={"x-access-token": self.access_token})
        return process_response(response)

    def get_url(self, url):
        if url.startswith("/"):
            return self.base_url + url
        else:
            return self.base_url + "/" + url

    def deserialize(self, component_dict: dict) -> ComponentInstanceEndpoint:
        if "type" in component_dict:
            component_type = component_dict["type"]
            if component_type == 'store':
                if "storeType" in component_dict:
                    store_type = component_dict["storeType"]
                    if store_type.lower() == "document":
                        document_store = DocumentStoreEndpoint.parse_obj(component_dict)
                        document_store.set_client(self)

                        # We need special handling of the metadata
                        if "metadata" in component_dict:
                            document_store.metadata = DocumentContentMetadata.parse_obj(
                                component_dict["metadata"])

                        return document_store
                    elif store_type.lower() == "model":
                        model_store = ModelStoreEndpoint.parse_obj(component_dict)
                        model_store.set_client(self)

                        # We need special handling of the metadata
                        if "metadata" in component_dict:
                            model_store.metadata = ModelContentMetadata.parse_obj(
                                component_dict["metadata"])

                        return model_store
                    elif store_type.lower() == "data":
                        return DataStoreEndpoint.parse_obj(component_dict).set_client(self)
                    else:
                        raise Exception("Unknown store type: " + store_type)
                else:
                    raise Exception("A store must have a storeType")
            if component_type == 'taxonomy':
                return TaxonomyEndpoint.parse_obj(component_dict).set_client(self)
        else:
            raise Exception(f"Type not found in the dictionary, unable to deserialize ({component_dict})")
