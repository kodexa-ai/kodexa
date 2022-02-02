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
from typing import Type, Optional

import requests
from pydantic import BaseModel

from kodexa.model import Store, Taxonomy
from kodexa.model.objects import PageStore, PageTaxonomy, PageProject, PageOrganization, Project, Organization, \
    PlatformOverview

logger = logging.getLogger('kodexa.platform')


class ComponentEndpoint:
    """
    Represents a re-usable endpoint for a component (stores, taxonomies etc)
    """

    def __init__(self, client: "KodexaClient", organization: "KodexaOrganization"):
        self.client: "KodexaClient" = client
        self.organization: "KodexaOrganization" = organization

    def get_type(self) -> str:
        pass

    def get_instance_class(self) -> Type[BaseModel]:
        pass

    def get_page_class(self) -> Type[BaseModel]:
        pass

    def find_by_slug(self, slug) -> Optional[Type[BaseModel]]:
        component_page = self.list(query=f"slug:'{slug}'")
        if component_page.empty:
            return None
        else:
            return component_page.content[0]

    def list(self, query="*", page=1, pagesize=10, sort=None):
        url = f"{self.client.url}/api/{self.get_type()}/{self.organization.organization_slug}"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort

        list_response = self.client.get(url, params=params)
        return self.get_page_class().parse_obj(**list_response.json())

    def get(self, slug, version=None):
        url = f"{self.client.url}/api/{self.get_type()}/{self.organization.organization_slug}/{slug}"
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

    def create(self, organization: Organization) -> Organization:
        url = f"{self.client.url}/api/organizations"
        create_response = self.client.post(url, body=json.loads(organization.json()))
        return Organization.parse_obj(create_response.json())

    def find_by_slug(self, slug) -> Optional[Organization]:
        organizations = self.list(query=f"slug:'{slug}'")
        if organizations.number_of_elements == 0:
            return None
        else:
            return organizations.content[0]

    def delete(self, id: str) -> None:
        url = f"{self.client.url}/api/organizations/{id}"
        self.client.delete(url)

    def list(self, query="*", page=1, pagesize=10, sort=None) -> PageOrganization:
        url = f"{self.client.url}/api/organizations"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort

        list_response = self.client.get(url, params=params)
        return PageOrganization.parse_obj(list_response.json())

    def get(self, organization_id) -> Organization:
        url = f"{self.client.url}/api/organizations/{organization_id}"
        get_response = self.client.get(url)
        return Organization.parse_obj(**get_response.json())


class ProjectsEndpoint:

    def __init__(self, client: "KodexaClient", organization: "KodexaOrganization" = None):
        self.client: "KodexaClient" = client
        self.organization: Optional["KodexaOrganization"] = organization

    def list(self, query="*", page=1, pagesize=10, sort=None):
        url = f"{self.client.url}/api/projects"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort

        list_response = self.client.get(url, params=params)
        return PageProject.parse_obj(**list_response.json())

    def get(self, project_id: str) -> Project:
        url = f"{self.client.url}/api/projects/{project_id}"
        get_response = self.client.get(url)
        return Project.parse_obj(**get_response.json())

    def create(self, project: Project, template_ref: str = None) -> Project:
        url = f"{self.client.url}/api/projects"

        if template_ref is not None:
            params = {"templateRef": template_ref}
        else:
            params = None

        create_response = self.client.post(url, body=json.loads(project.json()), params=params)
        return Project.parse_obj(create_response.json())

    def delete(self, id: str) -> None:
        url = f"{self.client.url}/api/projects/{id}"
        self.client.delete(url)


class StoresEndpoint(ComponentEndpoint):
    def get_type(self) -> str:
        return "stores"

    def get_page_class(self) -> Type[BaseModel]:
        return PageStore

    def get_instance_class(self) -> Type[BaseModel]:
        return Store


class TaxonomiesEndpoint(ComponentEndpoint):
    def get_type(self) -> str:
        return "taxonomies"

    def get_page_class(self) -> Type[BaseModel]:
        return PageTaxonomy

    def get_instance_class(self) -> Type[BaseModel]:
        return Taxonomy


class KodexaOrganization:
    def __init__(self, client, organization_slug):
        self.client = client
        self.organization_slug = organization_slug
        self.stores = StoresEndpoint(client, self)
        self.taxonomies = TaxonomiesEndpoint(client, self)


def process_response(response) -> requests.Response:
    if response.status_code == 401:
        raise Exception("Unauthorized")
    if response.status_code == 404:
        raise Exception("Not found")
    if response.status_code == 500:
        raise Exception("Internal server error")
    if response.status_code == 400:
        raise Exception("Bad request " + response.text)
    return response


class KodexaClient:

    def __init__(self, url=None, access_token=None):
        from kodexa import KodexaPlatform
        self.url = url if url is not None else KodexaPlatform.get_url()
        self.access_token = access_token if access_token is not None else KodexaPlatform.get_access_token()
        self.organizations = OrganizationsEndpoint(self)
        self.projects = ProjectsEndpoint(self)

    def get_platform(self):
        return PlatformOverview.parse_obj(self.get(f"{self.url}/api").json())

    def get(self, url, params=None) -> requests.Response:
        response = requests.get(url, params=params, headers={"x-access-token": self.access_token,
                                                             "content-type": "application/json"})
        return process_response(response)

    def post(self, url, data=None, body=None, files=None, params=None) -> requests.Response:
        response = requests.post(url, json=body, data=data, files=files, params=params,
                                 headers={"x-access-token": self.access_token,
                                          "content-type": "application/json"})
        return process_response(response)

    def put(self, url, body=None) -> requests.Response:
        response = requests.put(url, json=body, headers={"x-access-token": self.access_token,
                                                         "content-type": "application/json"})
        return process_response(response)

    def delete(self, url, params=None) -> requests.Response:
        response = requests.delete(url, params=params, headers={"x-access-token": self.access_token})
        return process_response(response)
