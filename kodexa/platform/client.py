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
import time
from pathlib import Path
from typing import Type, Optional, List

import requests
from functional import seq
from pydantic import BaseModel

from kodexa import Document
from kodexa.model import Store, Taxonomy
from kodexa.model.base import BaseEntity
from kodexa.model.objects import PageStore, PageTaxonomy, PageProject, PageOrganization, Project, Organization, \
    PlatformOverview, DocumentFamily, DocumentContentMetadata, ModelContentMetadata, ExtensionPack, Pipeline, \
    AssistantDefinition, Action, ModelRuntime, Credential, Execution, PageAssistantDefinition, PageCredential, \
    PageProjectTemplate, PageUser, User, FeatureSet, ContentObject, Taxon, SlugBasedMetadata, DataObject, \
    PageDataObject, Assistant, Dashboard

logger = logging.getLogger()


#
# Declare all the endpoints that we will have
#
# These wrap the objects from the model and provide a simple interface to the platform that is easier to use


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
        return self.get_page_class().parse_obj(list_response.json())

    def get(self, slug, version=None):
        url = f"/api/{self.get_type()}/{self.organization.slug}/{slug}"
        if version is not None:
            url += f"/{version}"

        get_response = self.client.get(url)
        return self.get_instance_class().parse_obj(get_response.json())


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
        create_response = self.client.post(url, body=json.loads(organization.json(by_alias=True)))
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


class PageEndpoint(ClientEndpoint):

    def to_df(self):
        import pandas as pd
        df = pd.DataFrame(seq(self.content).map(lambda x: x.dict()).to_list())
        df.drop(columns='client', axis=1)
        return df

    def get(self, index: int) -> "ComponentInstanceEndpoint":
        if index < 0 or index >= len(self.content):
            raise IndexError(f"Index {index} out of range")
        return self.content[index]

    def set_client(self, client):
        ClientEndpoint.set_client(self, client)
        return self.to_endpoints()

    def to_endpoints(self):
        self.content = seq(self.content).map(lambda x: self.client.deserialize(x.dict(by_alias=True))).to_list()
        return self


class PageTaxonomyEndpoint(PageTaxonomy, PageEndpoint):
    pass


class PageStoreEndpoint(PageStore, PageEndpoint):
    pass


class PageModelRuntimeEndpoint(PageStore, PageEndpoint):
    pass


class PageAssistantDefinitionEndpoint(PageAssistantDefinition, PageEndpoint):
    pass


class PageCredentialEndpoint(PageCredential, PageEndpoint):
    pass


class PageUserEndpoint(PageUser, PageEndpoint):
    pass


class PageProjectTemplateEndpoint(PageProjectTemplate, PageEndpoint):
    pass


class EntityEndpoint(BaseEntity, ClientEndpoint):

    def get_type(self) -> str:
        raise NotImplementedError()

    def create(self):
        url = f"/api/{self.get_type()}"
        exists = self.client.exists(url)
        if exists:
            raise Exception("Can't create as it already exists")
        else:
            url = f"/api/{self.get_type()}"
            self.client.post(url, self.to_dict())

    def update(self):
        url = f"/api/{self.get_type()}/{self.id}"
        exists = self.client.exists(url)
        if not exists:
            raise Exception("Can't update as it doesn't exist?")
        else:
            self.client.put(url, self.to_dict())

    def delete(self):
        url = f"/api/{self.get_type()}/{self.id}"
        exists = self.client.exists(url)
        if not exists:
            raise Exception("Component doesn't exist")
        else:
            self.client.delete(url)


class OrganizationEndpoint(Organization, EntityEndpoint):

    def get_type(self) -> str:
        return "organizations"

    def projects(self) -> PageProject:
        return ProjectsEndpoint(self.client, self).find_by_organization(self)

    def deploy(self, component: ComponentEndpoint) -> "ComponentInstanceEndpoint":
        url = f"/api/{component.get_type()}/{self.slug}"
        response = self.client.post(url, body=self.to_dict())
        return self.client.deserialize(response.json())

    def model_runtimes(self, query="*", page=1, pagesize=10, sort=None):
        url = f"/api/modelRuntimes/{self.slug}"
        model_runtimes_response = self.client.get(url,
                                                  params={"query": query, "page": page, "pageSize": pagesize,
                                                          "sort": sort})
        return PageModelRuntimeEndpoint.parse_obj(model_runtimes_response.json()).set_client(self.client)

    def project_templates(self, query="*", page=1, pagesize=10, sort=None):
        url = f"/api/projectTemplates/{self.slug}"
        response = self.client.get(url,
                                   params={"query": query, "page": page, "pageSize": pagesize,
                                           "sort": sort})
        return PageProjectTemplateEndpoint.parse_obj(response.json()).set_client(self.client)

    def credentials(self, query="*", page=1, pagesize=10, sort=None):
        url = f"/api/projectTemplates/{self.slug}"
        response = self.client.get(url,
                                   params={"query": query, "page": page, "pageSize": pagesize,
                                           "sort": sort})
        return PageCredentialEndpoint.parse_obj(response.json()).set_client(self.client)

    def stores(self, query="*", page=1, pagesize=10, sort=None):
        url = f"/api/stores/{self.slug}"
        stores_response = self.client.get(url,
                                          params={"query": query, "page": page, "pageSize": pagesize, "sort": sort})
        return PageStoreEndpoint.parse_obj(stores_response.json()).set_client(self.client)

    def get_store(self, slug, version=None):
        url = f"/api/stores/{self.slug}/{slug}{'/' + version if version else ''}"
        stores_response = self.client.get(url)
        return PageStoreEndpoint.parse_obj(stores_response.json()).set_client(self.client)

    def taxonomies(self, query="*", page=1, pagesize=10, sort=None):
        url = f"/api/taxonomies/{self.slug}"
        stores_response = self.client.get(url,
                                          params={"query": query, "page": page, "pageSize": pagesize, "sort": sort})
        return PageTaxonomyEndpoint.parse_obj(stores_response.json()).set_client(self.client)


class ComponentsEndpoint(ClientEndpoint):

    def __init__(self, organization: OrganizationEndpoint):
        self.organization = organization


class ComponentInstanceEndpoint(ClientEndpoint, SlugBasedMetadata):

    def get_type(self) -> str:
        raise NotImplementedError()

    def post_deploy(self) -> List[str]:
        return []

    def create(self):
        url = f"/api/{self.get_type()}/{self.ref.replace(':', '/')}"
        exists = self.client.exists(url)
        if exists:
            raise Exception("Can't create as it already exists")
        else:
            url = f"/api/{self.get_type()}"
            self.client.post(url, self.to_dict())

    def update(self):
        url = f"/api/{self.get_type()}/{self.ref.replace(':', '/')}"
        exists = self.client.exists(url)
        if not exists:
            raise Exception("Can't update as it doesn't exist?")
        else:
            self.client.put(url, self.to_dict())

    def delete(self):
        url = f"/api/{self.get_type()}/{self.ref.replace(':', '/')}"
        exists = self.client.exists(url)
        if not exists:
            raise Exception("Component doesn't exist")
        else:
            self.client.delete(url)

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
            return self.post_deploy()
        else:
            self.client.post(f"/api/{self.get_type()}/{self.org_slug}", self.to_dict())
            return self.post_deploy()


class AssistantEndpoint(Assistant, ClientEndpoint):

    def update(self) -> "AssistantEndpoint":
        url = f"/api/projects/{self.project.id}/assistants/{self.id}"
        response = self.client.put(url, body=self.to_dict())
        return AssistantEndpoint.parse_obj(response.json()).set_client(self.client)

    def delete(self):
        url = f"/api/projects/{self.project.id}/assistants/{self.id}"
        self.client.delete(url)

    def activate(self):
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/activate"
        self.client.put(url)

    def deactivate(self):
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/deactivate"
        self.client.put(url)

    def schedule(self):
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/schedule"
        self.client.put(url)


class ProjectEndpoint(EntityEndpoint, Project):

    def get_type(self) -> str:
        return "projects"

    def _get_resource(self, resource_type: str) -> List[ComponentInstanceEndpoint]:
        url = f"/api/projects/{self.id}/{resource_type}"
        response = self.client.get(url)
        return [self.client.deserialize(store) for store in response.json()]

    def stores(self, store_type=None, store_purpose=None) -> List[ComponentInstanceEndpoint]:
        return (seq(self._get_resource("stores"))
                .filter(lambda store: store_type is None or store.store_type == store_type)
                .filter(lambda store: store_type is None or store.store_purpose == store_purpose).to_list())

    def taxonomies(self) -> List["TaxonomyEndpoint"]:
        return self._get_resource("taxonomies")

    def dashboards(self) -> List[Dashboard]:
        return self._get_resource("dashboards")

    def assistants(self):
        url = f"/api/projects/{self.id}/assistants"
        response = self.client.get(url)
        return [AssistantEndpoint.parse_obj(assistant).set_client(self.client) for assistant in response.json()]


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
        return PageProject.parse_obj(list_response.json())

    def find_by_name(self, project_name: str) -> Project:
        url = f"/api/projects/"
        get_response = self.client.get(url, params={'filter': f'name={project_name}'})
        if len(get_response.json()['content']) > 0:
            return ProjectEndpoint.parse_obj(get_response.json()).set_client(self.client)
        else:
            raise Exception("Project not found")

    def find_by_organization(self, organization: Organization) -> PageProject:
        url = f"/api/projects/"
        get_response = self.client.get(url, params={'filter': f'organization.id={organization.id}'})
        projects_page = PageProject.parse_obj(get_response.json())
        projects_page.content = [ProjectEndpoint.parse_obj(project) for project in projects_page.content]
        return projects_page

    def get(self, project_id: str) -> Project:
        url = f"/api/projects/{project_id}"
        get_response = self.client.get(url)
        return ProjectEndpoint.parse_obj(get_response.json()).set_client(self.client)

    def create(self, project: Project, template_ref: str = None) -> Project:
        url = f"/api/projects"

        if template_ref is not None:
            params = {"templateRef": template_ref}
        else:
            params = None

        create_response = self.client.post(url, body=json.loads(project.json(by_alias=True)), params=params)
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

    def get_group_taxons(self) -> List[Taxon]:

        def find_groups(taxons) -> List[Taxon]:
            group_taxons = []
            for taxon in taxons:
                if taxon.is_group:
                    group_taxons.append(taxon)
                if taxon.children:
                    group_taxons.extend(find_groups(taxon.children))
            return group_taxons

        return find_groups(self.taxons)

    def find_taxon_by_label_path(self, label_path: str) -> Taxon:
        label_path_parts = label_path.split("/")

        def find_taxon(taxons, parts):
            for taxon in taxons:
                if taxon.label == parts[0]:
                    if len(parts) == 1:
                        return taxon
                    else:
                        return find_taxon(taxon.children, parts[1:])

        return find_taxon(self.taxons, label_path_parts)


class UserEndpoint(User, EntityEndpoint):
    def get_type(self) -> str:
        return "users"

    def delete(self):
        raise Exception("You can not delete a user")


class UsersEndpoint:
    """
    Represents the organization endpoint
    """

    def __init__(self, client: "KodexaClient"):
        self.client: "KodexaClient" = client

    def reindex(self):
        url = f'/api/users/_reindex'
        self.client.post(url)

    def create(self, user: User) -> UserEndpoint:
        url = f"/api/users"
        create_response = self.client.post(url, body=json.loads(user.json(by_alias=True)))
        return UserEndpoint.parse_obj(create_response.json()).set_client(self.client)

    def delete(self, id: str) -> None:
        url = f"/api/users/{id}"
        self.client.delete(url)

    def list(self, query: str = "*", page: int = 1, pagesize: int = 10, sort: Optional[str] = None,
             filters: Optional[List[str]] = None) -> PageUser:
        url = f"/api/organizations"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort
        if filters is not None:
            params["filter"] = filters

        list_response = self.client.get(url, params=params)
        return PageUser.parse_obj(list_response.json())

    def get(self, user_id) -> UserEndpoint:
        url = f"/api/users/{user_id}"
        get_response = self.client.get(url)
        return UserEndpoint.parse_obj(get_response.json()).set_client(self.client)


class DataObjectEndpoint(DataObject, ClientEndpoint):

    def update(self):
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/dataObjects/{self.id}"
        self.client.put(url, body=self.to_dict())

    def delete(self):
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/dataObjects/{self.id}"
        self.client.delete(url)


class DocumentFamilyEndpoint(DocumentFamily, ClientEndpoint):

    def update(self):
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}"
        self.client.put(url, body=self.to_dict())

    def update_document(self, document: Document, content_object: Optional[ContentObject] = None):
        if content_object is None:
            content_object = self.content_objects[-1]
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/objects/{content_object.id}/content"
        self.client.post(url, files={'document': document.to_kddb()})

    def wait_for(self, mixin: Optional[str] = None, label: Optional[str] = None,
                 timeout: int = 60) -> "DocumentFamilyEndpoint":
        logger.info("Waiting for mixin and/or label to be available on document family %s", self.id)
        start = time.time()
        while time.time() - start < timeout:
            url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}"
            updated_document_family = DocumentFamilyEndpoint.parse_obj(self.client.get(url).json()).set_client(
                self.client)
            if mixin and mixin in updated_document_family.mixins:
                return updated_document_family
            if label and label in updated_document_family.labels:
                return updated_document_family
        raise Exception(f"Not available on document family {self.id}")

    def delete(self):
        logger.info("Deleting document family %s", self.id)
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}"
        if self.client.exists(url):
            self.client.delete(url)
        else:
            raise Exception(f"Document family {self.id} does not exist")

    def get_document(self, content_object: Optional[ContentObject] = None) -> Document:
        if content_object is None:
            content_object = self.content_objects[-1]
        get_response = self.client.get(
            f"api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/objects/{content_object.id}/content")
        return Document.from_kddb(get_response.content)

    def replace_tags(self, document: Document, content_object: Optional[ContentObject] = None):
        feature_set = FeatureSet()
        if content_object is None:
            content_object = self.content_objects[-1]
        feature_set.node_features = []
        for tagged_node in document.select('//*[hasTag()]'):
            node_feature = {
                'nodeUuid': str(tagged_node.uuid),
                'features': []
            }

            feature_set.node_features.append(node_feature)

            # TODO this needs to be cleaned up
            for feature in tagged_node.get_features():
                if feature.feature_type == 'tag':
                    feature_dict = feature.to_dict()
                    feature_dict['featureType'] = feature.feature_type
                    feature_dict['name'] = feature.name
                    node_feature['features'].append(feature_dict)

        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/objects/{content_object.id}/_replaceTags"
        print(feature_set.json())
        self.client.put(url, body=feature_set.dict(by_alias=True))


class StoreEndpoint(ComponentInstanceEndpoint, Store):

    def get_type(self) -> str:
        return "stores"

    def get_metadata_class(self) -> Optional[Type[BaseModel]]:
        return None

    def set_metadata(self, metadata):
        pass

    def upload_contents(self, metadata) -> List[str]:
        return []

    def reindex(self):
        self.client.post(f"/api/stores/{self.ref.replace(':', '/')}/_reindex")

    def update_metadata(self):
        self.client.put(f"/api/stores/{self.ref.replace(':', '/')}/metadata", body=json.loads(self.metadata.json()))

    def get_metadata(self):
        metadata_response = self.client.get(f"/api/stores/{self.ref.replace(':', '/')}/metadata")
        return self.get_metadata_class().parse_obj(metadata_response.json()) if self.get_metadata_class() else None

    def post_deploy(self) -> List[str]:
        if self.metadata:
            # We need to determine in the subclass if we wil be uploading the
            # contents
            return self.upload_contents(self.metadata)
        return []


class DataStoreEndpoint(StoreEndpoint):

    def get_taxonomies(self) -> List[Taxonomy]:
        url = f"/api/stores/{self.ref.replace(':', '/')}/taxonomies"
        taxonomy_response = self.client.get(url)
        return [TaxonomyEndpoint.parse_obj(taxonomy_response) for taxonomy_response in taxonomy_response.json()]

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
                for taxon in data_object.taxon.children:
                    if not taxon.group:
                        table_result['column_headers'].append(taxon.label)
                        table_result['columns'].append(taxon.name)

            new_row = []
            for column in table_result['columns']:
                column_value = None
                if include_id:
                    if column == 'data_object_id':
                        column_value = data_object.id
                for attribute in data_object.attributes:
                    if attribute.tag == column:
                        column_value = attribute.string_value
                new_row.append(column_value)

            table_result['rows'].append(new_row)

        return pd.DataFrame(table_result['rows'], columns=table_result['column_headers'])

    def get_data_objects(self, path: str, query: str = "*", document_family: Optional[DocumentFamily] = None) -> List[
        DataObjectEndpoint]:
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
        rows = rows + row_response.content
        total_pages = row_response.total_pages

        for page in range(2, total_pages):
            row_response = self.get_data_objects_page_request(path, page, query=query, document_family=document_family)
            rows = rows + row_response.content

        return rows

    def get_data_object(self, data_object_id: str):

        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects/{data_object_id}"
        logger.info(f"Downloading a specific data object from {url}")

        data_object_response = self.client.get(url)
        return DataObjectEndpoint.parse_obj(data_object_response.json())

    def get_data_objects_page_request(self, path: str, page_number: int = 1, page_size=5000, query="*",
                                      document_family: Optional[DocumentFamily] = None) -> PageDataObject:
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

        data_objects_response = self.client.get(url, params=params)
        data_object_page = PageDataObject.parse_obj(data_objects_response.json())
        data_object_page.content = [DataObjectEndpoint.parse_obj(data_object) for data_object in data_object_page]
        return data_object_page

    def create_data_objects(self, data_objects: List[DataObject]) -> List[DataObjectEndpoint]:
        """

        Args:
          data_objects: A list of data objects that you want to create

        Returns:

        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        logger.debug(f"Creating data objects in store {url}")

        create_response = requests.post(url, json=[data_object.dict(by_alias=True) for data_object in data_objects])
        return [DataObjectEndpoint.parse_obj(data_object) for data_object in create_response.json()]


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

    def upload_file(self, file_path: str, object_path: Optional[str] = None, replace=False):
        if Path(file_path).is_file():
            logger.info(f"Uploading {file_path}")
            with open(file_path, 'rb') as path_content:
                return self.upload_bytes(path=object_path if object_path is not None else file_path,
                                         content=path_content,
                                         replace=replace)
        else:
            raise Exception(f"{file_path} is not a file")

    def upload_bytes(self, path: str, content, replace=False) -> DocumentFamilyEndpoint:
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
            self.client.delete(
                f"/api/stores/{self.ref.replace(':', '/')}/fs",
                params={"path": path})
            logger.info(f"Deleting {path}")

        content_object_response = self.client.post(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": path},
            files=files)
        logger.info(f"Uploaded {path} ({content_object_response.status_code})")
        return DocumentFamilyEndpoint.parse_obj(content_object_response.json()).set_client(self.client)

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

    def get_family(self, document_family_id: str) -> DocumentFamilyEndpoint:
        logger.info(f"Getting document family id {document_family_id}")
        document_family_response = self.client.get(
            f"/api/stores/{self.ref.replace(':', '/')}/families/{document_family_id}")
        return DocumentFamilyEndpoint.parse_obj(document_family_response.json()).set_client(self.client)

    def query(self, query: str = "*", page: int = 1, page_size: int = 100, sort=None) -> List[DocumentFamilyEndpoint]:
        params = {
            'page': page,
            'pageSize': page_size,
            'query': query
        }

        if sort is not None:
            params.sort = sort

        get_response = self.client.get(f"api/stores/{self.ref.replace(':', '/')}/families",
                                       params=params)
        families = []
        for fam_dict in get_response.json()['content']:
            families.append(DocumentFamilyEndpoint.parse_obj(fam_dict).set_client(self.client))
        return families

    def upload_document(self, path: str, document: "Document") -> DocumentFamilyEndpoint:
        logger.info(f"Putting document to path {path}")

        files = {"file": document.to_kddb()}
        data = {"path": path, "documentVersion": document.version, "document": True}
        document_family_response = self.client.post(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": path},
            files=files, data=data)

        return DocumentFamilyEndpoint.parse_obj(document_family_response.json()).set_client(self.client)

    def get_by_path(self, path: str) -> DocumentFamilyEndpoint:
        get_response = self.client.get(f"api/stores/{self.ref.replace(':', '/')}/fs",
                                       params={"path": path, "meta": True})
        return DocumentFamilyEndpoint.parse_obj(get_response.json()).set_client(self.client)


class ModelStoreEndpoint(DocumentStoreEndpoint):

    def get_metadata_class(self) -> Type[BaseModel]:
        return ModelContentMetadata

    def upload_contents(self, metadata):
        results = []
        if metadata.contents:
            for content_path in metadata.contents:
                final_wildcard = os.path.join(metadata.base_dir, content_path) if metadata.base_dir else content_path
                num_hits = 0
                for path_hit in glob.glob(final_wildcard):
                    relative_path = path_hit.replace(metadata.base_dir + '/', '') if metadata.base_dir else path_hit
                    if Path(path_hit).is_file():
                        logger.info(f"Uploading {path_hit}")
                        with open(path_hit, 'rb') as path_content:
                            self.upload_bytes(relative_path, path_content, replace=True)
                            num_hits += 1
                if num_hits > 0:
                    results.append(f"{num_hits} files uploaded for {final_wildcard}")
        return results

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
        print(response.text)
        raise Exception("Internal server error")
    if response.status_code == 400:
        if response.json() and response.json().get("errors"):
            messages = []
            for key, value in response.json()["errors"].items():
                messages.append(f"{key}: {value}")
            raise Exception(', '.join(messages))
        else:
            raise Exception("Bad request " + response.text)
    return response


#
#  The Kodexa Client is the way that brings everything together
#
#

OBJECT_TYPES = {
    "extensionPacks": {
        "name": "extension pack",
        "plural": "extension packs",
        "type": ExtensionPack
    },
    "pipelines": {
        "name": "pipeline",
        "plural": "pipelines",
        "type": Pipeline
    },
    "assistants": {
        "name": "assistant",
        "plural": "assistants",
        "type": AssistantDefinition
    },
    "actions": {
        "name": "action",
        "plural": "actions",
        "type": Action
    },
    "modelRuntimes": {
        "name": "modelRuntime",
        "plural": "modelRuntimes",
        "type": ModelRuntime
    },
    "credentials": {
        "name": "credential",
        "plural": "credentials",
        "type": Credential
    },
    "taxonomies": {
        "name": "taxonomy",
        "plural": "taxonomies",
        "type": TaxonomyEndpoint
    },
    "stores": {
        "name": "store",
        "plural": "stores"
    },
    "projects": {
        "name": "project",
        "plural": "projects",
        "type": ProjectEndpoint,
        "global": True
    },
    "executions": {
        "name": "execution",
        "plural": "executions",
        "type": Execution,
        "global": True,
        "sort": "startDate:desc"
    }
}


def resolve_object_type(obj_type):
    """Takes part of an object type (ie. pipeline) and then resolves the object type (pipelines)

    Args:
      obj_type: part of the object type

    Returns:
      The object type dict (if found)

    """
    hits = []
    keys = []

    if not isinstance(obj_type, str):
        obj_type = str(obj_type).lower()

    for target_type in OBJECT_TYPES.keys():
        if obj_type in target_type:
            hits.append(OBJECT_TYPES[target_type])
            keys.append(target_type)

    if len(hits) == 1:
        return keys[0], hits[0]

    if len(hits) == 0:
        raise Exception(f"Unable to find object type {obj_type}")
    else:
        raise Exception(f"Too many potential matches for object type ({','.join(keys)}")


class KodexaClient:

    def __init__(self, url=None, access_token=None):
        from kodexa import KodexaPlatform
        self.base_url = url if url is not None else KodexaPlatform.get_url()
        self.access_token = access_token if access_token is not None else KodexaPlatform.get_access_token()
        self.organizations = OrganizationsEndpoint(self)
        self.projects = ProjectsEndpoint(self)
        self.users = UsersEndpoint(self)

    def platform(self) -> PlatformOverview:
        return PlatformOverview.parse_obj(self.get('/api').json())

    def reindex(self):
        self.post("/api/indices/_reindex")

    def __build_object(self, ref, object_type_metadata):
        url = f"/api/{object_type_metadata['plural']}/{ref.replace(':', '/')}"
        response = self.get(url)

        # We need to merge the use of the object type metadata
        # and the deserialize method better

        if 'type' not in object_type_metadata:
            return self.deserialize(response.json())
        else:
            instance = object_type_metadata['type'](**response.json())
            if isinstance(instance, ClientEndpoint):
                instance.set_client(self)

            return instance

    def get_object_by_ref(self, object_type: str, ref: str) -> BaseModel:
        return self.__build_object(ref, resolve_object_type(object_type)[1])

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

    def post(self, url, body=None, data=None, files=None, params=None) -> requests.Response:
        headers = {"x-access-token": self.access_token}
        if files is None:
            headers["content-type"] = "application/json"
        response = requests.post(self.get_url(url), json=body, data=data, files=files, params=params,
                                 headers=headers)
        return process_response(response)

    def put(self, url, body=None, data=None, files=None) -> requests.Response:
        headers = {"x-access-token": self.access_token}
        if files is None:
            headers["content-type"] = "application/json"
        else:
            headers["content-type"] = "multipart/form-data"
        response = requests.put(self.get_url(url), json=body, data=data, files=files,
                                headers=headers)
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
                        if "metadata" in component_dict and component_dict["metadata"] is not None:
                            document_store.metadata = DocumentContentMetadata.parse_obj(
                                component_dict["metadata"])

                        return document_store
                    elif store_type.lower() == "model":
                        model_store = ModelStoreEndpoint.parse_obj(component_dict)
                        model_store.set_client(self)

                        # We need special handling of the metadata
                        if "metadata" in component_dict and component_dict["metadata"] is not None:
                            model_store.metadata = ModelContentMetadata.parse_obj(
                                component_dict["metadata"])

                        return model_store
                    elif store_type.lower() == "data" or store_type.lower() == "table":
                        return DataStoreEndpoint.parse_obj(component_dict).set_client(self)
                    else:
                        raise Exception("Unknown store type: " + store_type)
                else:
                    raise Exception("A store must have a storeType")
            if component_type == 'taxonomy':
                return TaxonomyEndpoint.parse_obj(component_dict).set_client(self)
        else:
            raise Exception(f"Type not found in the dictionary, unable to deserialize ({component_dict})")
