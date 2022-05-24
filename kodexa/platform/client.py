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
from pydantic_yaml import YamlModel

from kodexa.model import Store, Taxonomy, Document
from kodexa.model.base import BaseEntity
from kodexa.model.objects import PageStore, PageTaxonomy, PageProject, PageOrganization, Project, Organization, \
    PlatformOverview, DocumentFamily, DocumentContentMetadata, ModelContentMetadata, ExtensionPack, Pipeline, \
    AssistantDefinition, Action, ModelRuntime, Credential, Execution, PageAssistantDefinition, PageCredential, \
    PageProjectTemplate, PageUser, User, FeatureSet, ContentObject, Taxon, SlugBasedMetadata, DataObject, \
    PageDataObject, Assistant, ProjectTemplate, PageExtensionPack, DeploymentOptions, PageMembership, Membership, \
    PageDocumentFamily, ProjectResourcesUpdate

logger = logging.getLogger()


#
# Declare all the endpoints that we will have
#
# These wrap the objects from the model and provide a simple interface to the platform that is easier to use

class OrganizationOwned(BaseModel):
    organization: Optional["OrganizationEndpoint"] = None

    def set_organization(self, organization):
        self.organization = organization
        return self


class ClientEndpoint(YamlModel):
    client: Optional["KodexaClient"] = None

    def set_client(self, client):
        self.client = client
        if isinstance(self, ComponentInstanceEndpoint):
            self.ref = f"{self.org_slug}/{self.slug}:{self.version}"
        return self

    def to_dict(self):
        return json.loads(self.json(exclude={'client'}, by_alias=True))

    def yaml(self, **kwargs):
        if 'exclude' in kwargs:
            kwargs['exclude']['client']
        else:
            kwargs['exclude'] = {'client'}

        kwargs['exclude_unset'] = True
        kwargs['exclude_none'] = True

        return YamlModel.yaml(self, **kwargs)

    def detach(self):
        return self.copy(exclude={'client'})


class ProjectResourceEndpoint(ClientEndpoint):
    project: Optional["ProjectEndpoint"]

    def set_project(self, project: "ProjectEndpoint"):
        self.project = project
        return self

    def get_type(self) -> str:
        pass

    def get_instance_class(self, object_dict=None) -> Type[ClientEndpoint]:
        pass

    def list(self, query="*", page=1, pagesize=10, sort=None, filters: List[str] = None):
        url = f"/api/projects/{self.project.id}/{self.get_type()}"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort

        if filters is not None:
            params["filter"] = filters

        list_response = self.client.get(url, params=params)
        return [self.get_instance_class().parse_obj(item).set_client(self.client) for item in list_response.json()]

    def create(self, component):
        url = f"/api/projects/{self.project.id}/{self.get_type()}"
        get_response = self.client.post(url, component.to_dict())
        return self.get_instance_class().parse_obj(get_response.json()).set_client(self.client)


class ComponentEndpoint(ClientEndpoint, OrganizationOwned):

    def get_type(self) -> str:
        pass

    def get_instance_class(self, obj_dict=None) -> Type[BaseModel]:
        pass

    def get_page_class(self, obj_dict=None) -> Type[BaseModel]:
        pass

    def reindex(self):
        url = f"/api/{self.get_type()}/_reindex"
        self.client.post(url)

    def find_by_slug(self, slug, version=None) -> Optional[Type[BaseModel]]:
        filters = ["slug=" + slug]
        if version is not None:
            filters.append("version=" + version)
        component_page = self.list(filters=filters)
        if component_page.empty:
            return None
        else:
            return component_page.content[0]

    def list(self, query="*", page=1, pagesize=10, sort=None, filters: List[str] = None):
        url = f"/api/{self.get_type()}/{self.organization.slug}"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort

        if filters is not None:
            params["filters"] = filters

        list_response = self.client.get(url, params=params)
        return self.get_page_class(list_response.json()).parse_obj(list_response.json()).set_client(
            self.client).to_endpoints()

    def create(self, component):
        url = f"/api/{self.get_type()}/{self.organization.slug}/"
        get_response = self.client.post(url, component.to_dict())
        return self.get_instance_class(get_response.json()).parse_obj(get_response.json()).set_client(self.client)

    def get_by_slug(self, slug, version=None):
        url = f"/api/{self.get_type()}/{self.organization.slug}/{slug}"
        if version is not None:
            url += f"/{version}"

        get_response = self.client.get(url)
        return self.get_instance_class(get_response.json()).parse_obj(get_response.json())


class OrganizationsEndpoint:
    """
    Represents the organization endpoint
    """

    def __init__(self, client: "KodexaClient"):
        self.client: "KodexaClient" = client

    def reindex(self):
        url = f'/api/organizations/_reindex'
        self.client.post(url)

    def create(self, organization: Organization) -> "OrganizationEndpoint":
        url = f"/api/organizations"
        create_response = self.client.post(url, body=json.loads(organization.json(by_alias=True)))
        return OrganizationEndpoint.parse_obj(create_response.json()).set_client(self.client)

    def find_by_slug(self, slug) -> Optional["OrganizationEndpoint"]:
        organizations = self.list(filters=["slug=" + slug])
        if organizations.number_of_elements == 0:
            return None
        else:
            return organizations.content[0]

    def delete(self, id: str) -> None:
        url = f"/api/organizations/{id}"
        self.client.delete(url)

    def list(self, query: str = "*", page: int = 1, pagesize: int = 10, sort: Optional[str] = None,
             filters: Optional[List[str]] = None) -> "PageOrganizationEndpoint":
        url = f"/api/organizations"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort
        if filters is not None:
            params["filter"] = filters

        list_response = self.client.get(url, params=params)
        return PageOrganizationEndpoint.parse_obj(list_response.json()).set_client(self.client)

    def get(self, organization_id) -> "OrganizationEndpoint":
        url = f"/api/organizations/{organization_id}"
        get_response = self.client.get(url)
        return OrganizationEndpoint.parse_obj(**get_response.json()).set_client(self.client)


class PageEndpoint(ClientEndpoint):

    def get_type(self) -> Optional[str]:
        return None

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
        self.content = seq(self.content).map(
            lambda x: self.client.deserialize(x.dict(exclude={'client'}, by_alias=True),
                                              type=self.get_type())).to_list()
        return self


class PageTaxonomyEndpoint(PageTaxonomy, PageEndpoint):
    pass


class PageStoreEndpoint(PageStore, PageEndpoint):
    pass


class PageModelRuntimeEndpoint(PageStore, PageEndpoint):
    pass


class PageExtensionPackEndpoint(PageExtensionPack, PageEndpoint):
    pass


class PageAssistantDefinitionEndpoint(PageAssistantDefinition, PageEndpoint):
    pass


class PageCredentialEndpoint(PageCredential, PageEndpoint):
    pass


class PageUserEndpoint(PageUser, PageEndpoint):

    def get_type(self) -> Optional[str]:
        return "user"


class PageMembershipEndpoint(PageMembership, PageEndpoint):

    def get_type(self) -> Optional[str]:
        return "membership"


class PageProjectEndpoint(PageProject, PageEndpoint):

    def get_type(self) -> Optional[str]:
        return "project"


class PageProjectTemplateEndpoint(PageProjectTemplate, PageEndpoint):
    pass


class PageOrganizationEndpoint(PageOrganization, PageEndpoint):

    def get_type(self) -> Optional[str]:
        return "organization"


class PageDocumentFamilyEndpoint(PageDocumentFamily, PageEndpoint):

    def get_type(self) -> Optional[str]:
        return "documentFamily"


class EntityEndpoint(BaseEntity, ClientEndpoint):

    def reload(self):
        url = f"/api/{self.get_type()}/{self.id}"
        response = self.client.get(url)
        return self.parse_obj(response.json()).set_client(self.client)

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

    @property
    def projects(self) -> 'ProjectsEndpoint':
        return ProjectsEndpoint(self.client, self)

    def deploy(self, component: ComponentEndpoint) -> "ComponentInstanceEndpoint":
        url = f"/api/{component.get_type()}/{self.slug}"
        response = self.client.post(url, body=component.to_dict())
        return self.client.deserialize(response.json())

    def suspend(self):
        self.client.put(f"/api/organizations/{self.id}/suspend")

    @property
    def model_runtimes(self) -> "ModelRuntimesEndpoint":
        return ModelRuntimesEndpoint().set_organization(self).set_client(self.client)

    @property
    def extension_packs(self) -> "ExtensionPacksEndpoint":
        return ExtensionPacksEndpoint().set_organization(self).set_client(self.client)

    @property
    def project_templates(self) -> "ProjectTemplatesEndpoint":
        return ProjectTemplatesEndpoint().set_organization(self).set_client(self.client)

    @property
    def credentials(self, query="*", page=1, pagesize=10, sort=None):
        return CredentialsEndpoint().set_organization(self).set_client(self.client)

    @property
    def stores(self):
        return StoresEndpoint().set_client(self.client).set_organization(self)

    @property
    def taxonomies(self):
        return TaxonomiesEndpoint().set_client(self.client).set_organization(self)


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
            url = f"/api/{self.get_type()}/{self.org_slug}"
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

    def set_stores(self, stores: List["DocumentStoreEndpoint"]):
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/stores"
        self.client.put(url, body=[store.to_dict() for store in stores])
        return self

    def get_stores(self) -> List["DocumentStoreEndpoint"]:
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/stores"
        response = self.client.get(url)
        return [DocumentStoreEndpoint.parse_obj(store).set_client(self.client) for store in response.json()]

    def executions(self) -> List["Execution"]:
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/executions"
        response = self.client.get(url)
        return [Execution.parse_obj(execution) for execution in response.json()]


class ProjectAssistantsEndpoint(ProjectResourceEndpoint):

    def get_type(self) -> str:
        return f"assistants"

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return AssistantEndpoint


class ProjectDocumentStoresEndpoint(ProjectResourceEndpoint):

    def get_type(self) -> str:
        return f"documentStores"

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return DocumentStoreEndpoint


class ProjectTaxonomiesEndpoint(ProjectResourceEndpoint):

    def get_type(self) -> str:
        return f"taxonomies"

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return TaxonomyEndpoint


class ProjectStoresEndpoint(ProjectResourceEndpoint):

    def get_type(self) -> str:
        return f"stores"

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        if object_dict['storeType'] == "DOCUMENT":
            return DocumentStoreEndpoint
        elif object_dict['storeType'] == "MODEL":
            return ModelStoreEndpoint
        elif object_dict['storeType'] == "TABLE":
            return DataStoreEndpoint
        else:
            raise ValueError(f"Unknown store type {object_dict['storeType']}")


class ProjectDataStoresEndpoint(ProjectResourceEndpoint):

    def get_type(self) -> str:
        return f"dataStores"

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return DataStoreEndpoint


class ProjectModelStoresEndpoint(ProjectResourceEndpoint):

    def get_type(self) -> str:
        return f"modelStores"

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return DataStoreEndpoint


class ProjectEndpoint(EntityEndpoint, Project):

    def get_type(self) -> str:
        return "projects"

    def update_resources(self, stores: List["StoreEndpoint"] = None,
                         taxonomies: List["TaxonomyEndpoint"] = None) -> "ProjectEndpoint":
        project_resources_update = ProjectResourcesUpdate()
        project_resources_update.store_refs = []
        project_resources_update.taxonomy_refs = []
        project_resources_update.dashboard_refs = []

        if stores:
            project_resources_update.store_refs = [store.ref for store in stores]

        if taxonomies:
            project_resources_update.taxonomy_refs = [taxonomy.ref for taxonomy in taxonomies]

        self.client.put(f"/api/projects/{self.id}/resources",
                        body=json.loads(project_resources_update.json(by_alias=True)))

    @property
    def document_stores(self) -> ProjectDocumentStoresEndpoint:
        return ProjectDocumentStoresEndpoint().set_client(self.client).set_project(self)

    @property
    def data_stores(self) -> ProjectDataStoresEndpoint:
        return ProjectDataStoresEndpoint().set_client(self.client).set_project(self)

    @property
    def model_stores(self) -> ProjectModelStoresEndpoint:
        return ProjectModelStoresEndpoint().set_client(self.client).set_project(self)

    @property
    def taxonomies(self) -> ProjectTaxonomiesEndpoint:
        return ProjectTaxonomiesEndpoint().set_client(self.client).set_project(self)

    @property
    def assistants(self) -> ProjectAssistantsEndpoint:
        return ProjectAssistantsEndpoint().set_client(self.client).set_project(self)


class EntitiesEndpoint:

    def get_type(self) -> str:
        raise NotImplementedError()

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        raise NotImplementedError()

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        raise NotImplementedError()

    def __init__(self, client: "KodexaClient", organization: "OrganizationEndpoint" = None):
        self.client: "KodexaClient" = client
        self.organization: Optional["OrganizationEndpoint"] = organization

    def reindex(self):
        url = f'/api/{self.get_type()}/_reindex'

        self.client.post(url)

    def list(self, query="*", page=1, pagesize=10, sort=None, filters: List[str] = None):
        url = f"/api/{self.get_type()}"

        params = {"query": query,
                  "page": page,
                  "pageSize": pagesize}

        if sort is not None:
            params["sort"] = sort

        if filters is not None:
            params["filter"] = filters

        list_response = self.client.get(url, params=params)
        return self.get_page_class().parse_obj(list_response.json()).set_client(self.client)

    def find_by_organization(self, organization: Organization) -> PageProject:
        url = f"/api/{self.get_type()}/"
        get_response = self.client.get(url, params={'filter': f'organization.id={organization.id}'})
        return self.get_page_class().parse_obj(get_response.json()).set_client(self.client)

    def get(self, entity_id: str) -> "EntityEndpoint":
        url = f"/api/{self.get_type()}/{entity_id}"
        get_response = self.client.get(url)
        return self.get_instance_class().parse_obj(get_response.json()).set_client(self.client)

    def create(self, new_entity: EntityEndpoint) -> EntityEndpoint:
        url = f"/api/{self.get_type()}"

        create_response = self.client.post(url, body=json.loads(new_entity.json(exclude={'client'}, by_alias=True)))
        return self.get_instance_class().parse_obj(create_response.json()).set_client(self.client)

    def delete(self, id: str) -> None:
        url = f"/api/{self.get_type()}/{id}"
        self.client.delete(url)


class ProjectsEndpoint(EntitiesEndpoint):

    def get_type(self) -> str:
        return f"projects"

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return ProjectEndpoint

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        return PageProjectEndpoint

    def find_by_name(self, project_name: str) -> ProjectEndpoint:
        url = f"/api/{self.get_type()}/"
        get_response = self.client.get(url, params={'filter': f'name={project_name}'})
        if len(get_response.json()['content']) > 0:
            return ProjectEndpoint.parse_obj(get_response.json()['content'][0]).set_client(self.client)
        else:
            raise Exception("Project not found")

    def create(self, project: Project, template_ref: str = None) -> Project:
        url = f"/api/{self.get_type()}"

        if template_ref is not None:
            params = {"templateRef": template_ref}
        else:
            params = None

        create_response = self.client.post(url, body=json.loads(project.json(exclude={'client'}, by_alias=True)),
                                           params=params)
        return ProjectEndpoint.parse_obj(create_response.json()).set_client(self.client)


class StoresEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    def get_type(self) -> str:
        return "stores"

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        return PageStoreEndpoint

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        if object_dict['storeType'] == "DOCUMENT":
            return DocumentStoreEndpoint
        elif object_dict['storeType'] == "MODEL":
            return ModelStoreEndpoint
        elif object_dict['storeType'] == "TABLE":
            return DataStoreEndpoint
        else:
            raise ValueError(f"Unknown store type {object_dict['storeType']}")


class ExtensionPacksEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    def get_type(self) -> str:
        return "extensionPacks"

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        return PageExtensionPackEndpoint

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return ExtensionPackEndpoint

    def deploy_from_url(self, extension_pack_url: str,
                        deployment_options: DeploymentOptions) -> "ExtensionPackEndpoint":
        url = f"/api/extensionPacks/{self.organization.slug}"
        create_response = self.client.post(url, body=json.loads(deployment_options.json(by_alias=True)),
                                           params={"uri": extension_pack_url})
        return ExtensionPackEndpoint.parse_obj(create_response.json()).set_client(self.client)


class ProjectTemplatesEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    def get_type(self) -> str:
        return "projectTemplates"

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        return PageProjectTemplateEndpoint

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return ProjectTemplateEndpoint


class CredentialsEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    def get_type(self) -> str:
        return "credentials"

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        return PageCredentialEndpoint

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return CredentialEndpoint


class ModelRuntimesEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    def get_type(self) -> str:
        return "modelRuntimes"

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        return PageModelRuntimeEndpoint

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return ModelRuntimeEndpoint


class ProjectTemplateEndpoint(ComponentInstanceEndpoint, ProjectTemplate):

    def get_type(self) -> str:
        return "projectTemplates"


class CredentialEndpoint(ComponentInstanceEndpoint, Credential):

    def get_type(self) -> str:
        return "credentials"


class AssistantDefinitionEndpoint(ComponentInstanceEndpoint, AssistantDefinition):

    def get_type(self) -> str:
        return "assistants"


class PipelineEndpoint(ComponentInstanceEndpoint, Pipeline):

    def get_type(self) -> str:
        return "pipelines"


class ModelRuntimeEndpoint(ComponentInstanceEndpoint, ModelRuntime):

    def get_type(self) -> str:
        return "modelRuntimes"


class ExtensionPackEndpoint(ComponentInstanceEndpoint, ExtensionPack):

    def get_type(self) -> str:
        return "extensionPacks"


class ActionEndpoint(ComponentInstanceEndpoint, Action):

    def get_type(self) -> str:
        return "actions"


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

    def find_taxon(self, taxons, parts, use_label=False):
        for taxon in taxons:
            match_value = taxon.label if use_label else taxon.name
            if parts[0] == match_value:
                if len(parts) == 1:
                    return taxon
                else:
                    return self.find_taxon(taxon.children, parts[1:], use_label)

    def find_taxon_by_label_path(self, label_path: str) -> Taxon:
        label_path_parts = label_path.split("/")

        return self.find_taxon(self.taxons, label_path_parts, use_label=True)

    def find_taxon_by_path(self, path: str) -> Taxon:
        path_parts = path.split("/")
        return self.find_taxon(self.taxons, path_parts)


class MembershipEndpoint(Membership, EntityEndpoint):
    def get_type(self) -> str:
        return "memberships"


class UserEndpoint(User, EntityEndpoint):
    def get_type(self) -> str:
        return "users"

    def activate(self) -> "UserEndpoint":
        url = f"/api/users/{self.id}/activate"
        response = self.client.put(url)
        return UserEndpoint.parse_obj(response.json()).set_client(self.client)

    def deactivate(self) -> "UserEndpoint":
        url = f"/api/users/{self.id}/activate"
        response = self.client.put(url)
        return UserEndpoint.parse_obj(response.json()).set_client(self.client)

    def set_password(self, password: str, reset_token) -> "UserEndpoint":
        url = f"/api/users/{self.id}/password"
        response = self.client.put(url, body={"password": password, "resetToken": reset_token})
        return UserEndpoint.parse_obj(response.json()).set_client(self.client)

    def get_memberships(self) -> List[MembershipEndpoint]:
        url = f"/api/users/{self.id}/memberships"
        response = self.client.get(url)
        return [MembershipEndpoint.parse_obj(membership) for membership in response.json()]


class MembershipsEndpoint(EntitiesEndpoint):

    def get_type(self) -> str:
        return f"memberships"

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return MembershipEndpoint

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        return PageMembershipEndpoint


class UsersEndpoint(EntitiesEndpoint):

    def get_type(self) -> str:
        return f"users"

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return UserEndpoint

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        return PageUserEndpoint


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

    def export(self) -> bytes:
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/export"
        get_response = self.client.get(url)
        return get_response.content

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

            time.sleep(5)

        raise Exception(f"Not available on document family {self.id}")

    def delete(self):
        logger.info("Deleting document family %s", self.id)
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}"
        if self.client.exists(url):
            self.client.delete(url)
        else:
            raise Exception(f"Document family {self.id} does not exist")

    def get_native(self) -> bytes:
        hits = list(filter(lambda content_object: content_object.content_type == 'NATIVE', self.content_objects))
        if len(hits) == 0:
            raise Exception(f"No native content object found on document family {self.id}")

        get_response = self.client.get(
            f"api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/objects/{hits[0].id}/content")

        return get_response.content

    def add_label(self, label: str):
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/addLabel"
        return self.client.put(url, params={'label': label})

    def get_document(self, content_object: Optional[ContentObject] = None) -> Document:
        if content_object is None:
            content_object = self.content_objects[-1]
        get_response = self.client.get(
            f"api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/objects/{content_object.id}/content")
        return Document.from_kddb(get_response.content)

    def reprocess(self, assistant: Assistant):
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/reprocess"
        self.client.put(url, params={'assistantId': assistant.id})

    def add_document(self, document: Document, content_object: Optional[ContentObject] = None):
        url = f'/api/stores/{self.store_ref.replace(":", "/")}/families/{self.id}/objects'
        if content_object is None:
            content_object = self.content_objects[-1]
        self.client.post(url, params={'sourceContentObjectId': content_object.id, 'transitionType': 'DERIVED',
                                      'documentVersion': document.version},
                         files={'file': document.to_kddb()})

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
        self.client.put(f"/api/stores/{self.ref.replace(':', '/')}/metadata",
                        body=json.loads(self.metadata.json(by_alias=True)))

    def get_metadata(self):
        metadata_response = self.client.get(f"/api/stores/{self.ref.replace(':', '/')}/metadata")
        return self.get_metadata_class().parse_obj(metadata_response.json()) if self.get_metadata_class() else None

    def post_deploy(self) -> List[str]:
        if self.metadata:
            # We need to determine in the subclass if we wil be uploading the
            # contents
            self.update_metadata()
            return self.upload_contents(self.metadata)
        return []


class DataStoreEndpoint(StoreEndpoint):

    def get_data_objects_export(self, document_family: Optional[DocumentFamily] = None,
                                output_format: str = "json", path:Optional[str] = None, root_name:str="", friendly_names=True) -> str:
        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        params = {"format": output_format, "friendlyNames": friendly_names, "rootName": root_name}
        if document_family:
            params["documentFamilyId"] = document_family.id

        if output_format == 'csv' and not path:
            raise ValueError("CSV output requires a path")

        response = self.client.get(url, params=params)
        return response.text

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
        data_object_page.content = [DataObjectEndpoint.parse_obj(data_object) for data_object in
                                    data_object_page.content]
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

    def import_family(self, file_path: str):
        if Path(file_path).is_file():
            logger.info(f"Uploading {file_path}")
            with open(file_path, 'rb') as dfm_content:
                files = {"familyZip": dfm_content}
                content_object_response = self.client.post(
                    f"/api/stores/{self.ref.replace(':', '/')}/families",
                    params={'import': 'true'},
                    files=files)
                logger.info(f"Uploaded ({content_object_response.status_code})")
                return DocumentFamilyEndpoint.parse_obj(content_object_response.json()).set_client(self.client)
        else:
            raise Exception(f"{file_path} is not a file")

    def upload_file(self, file_path: str, object_path: Optional[str] = None, replace=False,
                    additional_metadata: Optional[dict] = None):
        if Path(file_path).is_file():
            logger.info(f"Uploading {file_path}")
            with open(file_path, 'rb') as path_content:
                return self.upload_bytes(path=object_path if object_path is not None else file_path,
                                         content=path_content,
                                         replace=replace, additional_metadata=additional_metadata)
        else:
            raise Exception(f"{file_path} is not a file")

    def upload_bytes(self, path: str, content, replace=False,
                     additional_metadata: Optional[dict] = None) -> DocumentFamilyEndpoint:
        """
        Put the content into the store at the given path

        Args:
          path: The path you wish to put the content at
          content: The content for that object
          replace: Replace the content if it exists
          additional_metadata: Additional metadata to store with the document (not it can't include 'path')

        Returns:
          the document family that was created
        """
        files = {"file": content}

        if additional_metadata is None:
            additional_metadata = {}

        if replace and self.client.exists(f"/api/stores/{self.ref.replace(':', '/')}/fs", params={"path": path}):
            self.client.delete(
                f"/api/stores/{self.ref.replace(':', '/')}/fs",
                params={"path": path})
            logger.info(f"Deleting {path}")

        content_object_response = self.client.post(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": path},
            data=additional_metadata,
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

    def download_document_families(self, output_dir: str):
        """Download all the document families in the store to the given directory"""

        for document_family in self.query(page_size=9999).content:
            export_bytes = document_family.export()
            with open(os.path.join(output_dir, document_family.id + ".dfm"), 'wb') as f:
                f.write(export_bytes)

    def get_metadata_class(self) -> Type[BaseModel]:
        return DocumentContentMetadata

    def get_family(self, document_family_id: str) -> DocumentFamilyEndpoint:
        logger.info(f"Getting document family id {document_family_id}")
        document_family_response = self.client.get(
            f"/api/stores/{self.ref.replace(':', '/')}/families/{document_family_id}")
        return DocumentFamilyEndpoint.parse_obj(document_family_response.json()).set_client(self.client)

    def query(self, query: str = "*", page: int = 1, page_size: int = 100, sort=None) -> PageDocumentFamilyEndpoint:
        params = {
            'page': page,
            'pageSize': page_size,
            'query': query
        }

        if sort is not None:
            params.sort = sort

        get_response = self.client.get(f"api/stores/{self.ref.replace(':', '/')}/families",
                                       params=params)

        return PageDocumentFamilyEndpoint.parse_obj(get_response.json()).set_client(self.client)

    def upload_document(self, path: str, document: "Document") -> DocumentFamilyEndpoint:
        logger.info(f"Putting document to path {path}")

        files = {"file": document.to_kddb()}
        data = {"path": path, "documentVersion": document.version, "document": True}
        document_family_response = self.client.post(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": path},
            files=files, data=data)

        return DocumentFamilyEndpoint.parse_obj(document_family_response.json()).set_client(self.client)

    def exists_by_path(self, path: str) -> bool:
        return self.client.exists(f"/api/stores/{self.ref.replace(':', '/')}/fs", params={"path": path})

    def get_by_path(self, path: str) -> DocumentFamilyEndpoint:
        get_response = self.client.get(f"api/stores/{self.ref.replace(':', '/')}/fs",
                                       params={"path": path, "meta": True})
        return DocumentFamilyEndpoint.parse_obj(get_response.json()).set_client(self.client)


class ModelStoreEndpoint(DocumentStoreEndpoint):
    IMPLEMENTATION_PREFIX = "model_implementation/"
    TRAINED_MODELS_PREFIX = "trained_models/"

    def get_metadata_class(self) -> Type[BaseModel]:
        return ModelContentMetadata

    def upload_trained_model(self, training_run_id: str, base_path: Optional[str] = None):
        results = []
        final_wildcard = "**/*" if base_path is None else f"{base_path}/**/*"
        num_hits = 0
        for path_hit in glob.glob(final_wildcard, recursive=True):
            relative_path = path_hit.replace(base_path + '/', '') if base_path else path_hit

            # We will put the implementation in one place

            relative_path = self.TRAINED_MODELS_PREFIX + training_run_id + '/' + relative_path
            if Path(path_hit).is_file():
                logger.info(f"Uploading model file {path_hit}")
                with open(path_hit, 'rb') as path_content:
                    self.upload_bytes(relative_path, path_content, replace=True)
                    num_hits += 1
        if num_hits > 0:
            results.append(f"{num_hits} files uploaded for {final_wildcard}")
        return results

    def download_trained_model(self, training_run_id: str, download_path: Optional[str] = ""):
        for path in self.list_contents():
            if path.startswith(self.TRAINED_MODELS_PREFIX + training_run_id):
                file_path = os.path.join(download_path, path.replace(self.TRAINED_MODELS_PREFIX, ''))
                logger.info(f"Downloading trained model file {file_path}")
                Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)

                with open(file_path, 'wb') as output_file:
                    output_file.write(self.get_bytes(path))

    def download_implementation(self, download_path: Optional[str] = ""):
        for path in self.list_contents():
            if path.startswith(self.IMPLEMENTATION_PREFIX):
                logger.info(f"Downloading implementation file {path}")
                file_path = os.path.join(download_path, path.replace(self.IMPLEMENTATION_PREFIX, ''))
                logger.info(f"Downloading model file {file_path}")
                Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)

                with open(file_path, 'wb') as output_file:
                    output_file.write(self.get_bytes(path))

    def upload_implementation(self, metadata):
        return self.upload_contents(metadata)

    def upload_contents(self, metadata):

        # First we are going to delete anything we have in the implementation
        for imp_file in self.list_contents():
            if imp_file.startswith(self.IMPLEMENTATION_PREFIX):
                self.delete_by_path(imp_file)

        results = []
        if metadata.contents:

            ignore_files = []
            if metadata.ignored_contents:
                for ignore_path in metadata.ignored_contents:
                    final_wildcard = os.path.join(metadata.base_dir, ignore_path) if metadata.base_dir else ignore_path
                    for path_hit in glob.glob(final_wildcard, recursive=True):
                        ignore_files.append(path_hit)

            for content_path in metadata.contents:
                final_wildcard = os.path.join(metadata.base_dir, content_path) if metadata.base_dir else content_path
                num_hits = 0

                for path_hit in glob.glob(final_wildcard, recursive=True):
                    if path_hit in ignore_files:
                        continue
                    relative_path = path_hit.replace(metadata.base_dir + '/', '') if metadata.base_dir else path_hit

                    # We will put the implementation in one place
                    relative_path = self.IMPLEMENTATION_PREFIX + relative_path
                    if Path(path_hit).is_file():
                        with open(path_hit, 'rb') as path_content:
                            results.append(f"Uploading model file {path_hit}")
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


class TaxonomiesEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):

    def get_type(self) -> str:
        return "taxonomies"

    def get_page_class(self, object_dict=None) -> Type[BaseModel]:
        return PageTaxonomyEndpoint

    def get_instance_class(self, object_dict=None) -> Type[BaseModel]:
        return TaxonomyEndpoint


def process_response(response) -> requests.Response:
    if response.status_code == 401:
        raise Exception(f"Unauthorized ({response.text})")
    if response.status_code == 404:
        raise Exception(f"Not found ({response.text})")
    if response.status_code == 405:
        raise Exception("Method not allowed")
    if response.status_code == 500:
        raise Exception("Internal server error: \n" + response.text)
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
        self.memberships = MembershipsEndpoint(self)

    @staticmethod
    def login(url, email, password):
        from requests.auth import HTTPBasicAuth
        obj_response = requests.get(f"{url}/api/account/me/token",
                                    auth=HTTPBasicAuth(email, password),
                                    headers={"content-type": "application/json"})
        if obj_response.status_code == 200:
            return KodexaClient(url, obj_response.text)
        else:
            raise Exception(f"Check your URL and password [{obj_response.status_code}]")

    @property
    def me(self):
        return UserEndpoint.parse_obj(self.get("/api/account/me").json()).set_client(self)

    @property
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

    def put(self, url, body=None, data=None, files=None, params=None) -> requests.Response:
        headers = {"x-access-token": self.access_token}
        if files is None:
            headers["content-type"] = "application/json"
        else:
            headers["content-type"] = "multipart/form-data"
        response = requests.put(self.get_url(url), json=body, data=data, files=files, params=params,
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

    def export_project(self, project: ProjectEndpoint, export_path: str):

        # We will create a directory for the project in the export path and then export the project
        # components and metadata to that directory

        # First export the project metadata

        project_export_dir = os.path.join(export_path, project.name)
        Path(project_export_dir).mkdir(parents=True, exist_ok=False)

        project_metadata_file = os.path.join(project_export_dir, "project_metadata.json")
        with open(project_metadata_file, "w") as f:
            f.write(json.dumps(project.to_dict(), indent=4))

        for assistant in project.assistants.list():
            assistant_file = os.path.join(project_export_dir, f"assistant-{assistant.id}.json")
            with open(assistant_file, "w") as f:
                f.write(json.dumps(assistant.to_dict(), indent=4))

        for data_store in project.data_stores.list():
            data_store_file = os.path.join(project_export_dir,
                                           f"data-store-{data_store.slug}-{data_store.version}.json")
            with open(data_store_file, "w") as f:
                f.write(json.dumps(data_store.to_dict(), indent=4))

        for document_store in project.document_stores.list():
            document_store_file = os.path.join(project_export_dir,
                                               f"document-store-{document_store.slug}-{document_store.version}.json")
            with open(document_store_file, "w") as f:
                f.write(json.dumps(document_store.to_dict(), indent=4))

            store_folder = os.path.join(project_export_dir,
                                        f"document-store-{document_store.slug}-{document_store.version}")
            Path(store_folder).mkdir(parents=True, exist_ok=False)
            document_store.download_document_families(store_folder)

        for model_store in project.model_stores.list():
            model_store_file = os.path.join(project_export_dir,
                                            f"model-store-{model_store.slug}-{model_store.version}.json")
            with open(model_store_file, "w") as f:
                f.write(json.dumps(model_store.to_dict(), indent=4))

            store_folder = os.path.join(project_export_dir,
                                        f"document-store-{model_store.slug}-{model_store.version}")
            Path(store_folder).mkdir(parents=True, exist_ok=False)
            model_store.download_document_families(store_folder)

        for taxonomy in project.taxonomies.list():
            taxonomy_file = os.path.join(project_export_dir,
                                         f"taxonomy-{taxonomy.slug}-{taxonomy.version}.json")
            with open(taxonomy_file, "w") as f:
                f.write(json.dumps(taxonomy.to_dict(), indent=4))

    def import_project(self, organization: OrganizationEndpoint, import_path: str):
        # The import path is the directory containing the export (or a zip file containing the export)

        project_metadata_file = os.path.join(import_path, "project_metadata.json")
        with open(project_metadata_file, "r") as f:
            project = Project.parse_obj(json.load(f))
            project.id = None
            project.uuid = None
            project.workflow = None
            project.organization = organization.detach()
            project.project_template_ref = None
            new_project = organization.projects.create(project, None)

        stores = []
        taxonomies = []

        import glob

        for assistant_file in glob.glob(os.path.join(import_path, "assistant-*.json")):
            with open(assistant_file, "r") as f:
                assistant: AssistantEndpoint = AssistantEndpoint.parse_obj(json.load(f))

                assistant.assistant_definition_ref = assistant.definition.ref.split(':')[0]
                new_project.assistants.create(assistant)

        for document_store_file in glob.glob(os.path.join(import_path, "document-store-*.json")):
            with open(document_store_file, "r") as f:
                document_store = DocumentStoreEndpoint.parse_obj(json.load(f)).set_client(self)
                document_store.org_slug = None
                document_store.ref = None
                document_store = organization.stores.create(document_store)
                stores.append(document_store)

                for doc_fam in glob.glob(os.path.join(import_path, document_store_file.replace('.json', '/*.dfm'))):
                    document_store.import_family(doc_fam)

        for data_store_file in glob.glob(os.path.join(import_path, "data-store-*.json")):
            with open(data_store_file, "r") as f:
                data_store = DataStoreEndpoint.parse_obj(json.load(f)).set_client(self)
                data_store.org_slug = None
                data_store.ref = None
                data_store = organization.stores.create(data_store)
                stores.append(data_store)

        for model_store_file in glob.glob(os.path.join(import_path, "model-store-*.json")):
            with open(model_store_file, "r") as f:
                model_store = ModelStoreEndpoint.parse_obj(json.load(f)).set_client(self)
                model_store.org_slug = None
                model_store.ref = None
                model_store = organization.stores.create(model_store)
                stores.append(model_store)

                for doc_fam in glob.glob(os.path.join(import_path, model_store_file.replace('.json', '/*.dfm'))):
                    model_store.import_family(doc_fam)

        for taxonomy_file in glob.glob(os.path.join(import_path, "taxonomy-*.json")):
            with open(taxonomy_file, "r") as f:
                taxonomy = TaxonomyEndpoint.parse_obj(json.load(f))
                taxonomy.org_slug = None
                taxonomy.ref = None
                taxonomies.append(organization.taxonomies.create(taxonomy))

        import time
        time.sleep(4)

        new_project.update_resources(stores=stores, taxonomies=taxonomies)

    def deserialize(self, component_dict: dict, type: Optional[str] = None) -> ComponentInstanceEndpoint:
        if "type" in component_dict or type is not None:
            component_type = type if type is not None else component_dict["type"]
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
            known_components = {
                "taxonomy": TaxonomyEndpoint,
                "pipeline": PipelineEndpoint,
                "action": ActionEndpoint,
                "credential": CredentialEndpoint,
                "projectTemplate": ProjectTemplateEndpoint,
                "modelRuntime": ModelRuntimeEndpoint,
                "extensionPack": ExtensionPackEndpoint,
                "user": UserEndpoint,
                "project": ProjectEndpoint,
                "membership": MembershipEndpoint,
                "documentFamily": DocumentFamilyEndpoint,
                "organization": OrganizationEndpoint
            }

            if component_type in known_components:
                return known_components[component_type].parse_obj(component_dict).set_client(self)
            else:
                raise Exception("Unknown component type: " + component_type)
        else:
            raise Exception(f"Type not found in the dictionary, unable to deserialize ({component_dict})")

    def get_project(self, project_id) -> ProjectEndpoint:
        project = self.get(f"/api/projects/{project_id}")
        return ProjectEndpoint.parse_obj(project.json()).set_client(self)
