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
import json
import logging
from typing import Type, Optional, List

import requests
from kodexa.model import Store, Taxonomy
from kodexa.model.objects import PageStore, PageTaxonomy, PageProject, PageOrganization, Project, Organization, \
    PlatformOverview
from pydantic import BaseModel

logger = logging.getLogger('kodexa.platform')


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

    client:Optional["KodexaClient"] = None

    def set_client(self, client):
        self.client = client
        return self


class OrganizationEndpoint(Organization, ClientEndpoint):

    def apply(self, component: ComponentEndpoint) -> ComponentEndpoint:
        url = f"/api/{component.get_type()}/{self.slug}"
        response = self.client.post(url, body=json.loads(component.json()))
        return self.client.deserialize(response.json())


class ComponentInstanceEndpoint(ClientEndpoint):

    def get_type(self) -> str:
        raise NotImplementedError()


class ProjectEndpoint(ClientEndpoint, Project):

    def stores(self) -> List[Store]:
        pass

    def taxonomies(self) -> List[Store]:
        pass

    def models(self) -> List[Store]:
        pass


class ProjectsEndpoint:

    def __init__(self, client: "KodexaClient", organization: "KodexaOrganization" = None):
        self.client: "KodexaClient" = client
        self.organization: Optional["KodexaOrganization"] = organization

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


class StoreEndpoint(ComponentInstanceEndpoint, Store):

    def get_type(self) -> str:
        return "stores"


class DataStoreEndpoint(StoreEndpoint):
    pass


class ModelStoreEndpoint(StoreEndpoint):
    pass


class DocumentStoreEndpoint(StoreEndpoint):
    pass


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
                        document_store = DocumentStoreEndpoint.parse_obj(**component_dict)
                        document_store.set_client(self)
                        return document_store
                    elif store_type.lower() == "model":
                        model_store = ModelStoreEndpoint.parse_obj(**component_dict)
                        model_store.set_client(self)
                        return model_store
                    elif store_type.lower() == "data":
                        data_store = DataStoreEndpoint.parse_obj(**component_dict)
                        data_store.set_client(self)
                        return data_store
                    else:
                        raise Exception("Unknown store type: " + store_type)
                else:
                    raise Exception("A store must have a storeType")
            if component_type == 'taxonomy':
                return Taxonomy.parse_obj(**component_dict)
        else:
            raise Exception("Type not found in the dictionary, unable to deserialize")
