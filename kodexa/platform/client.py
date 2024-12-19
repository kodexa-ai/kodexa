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
from typing import Optional, List, ClassVar, Dict, Any

import requests
from functional import seq
from pydantic import BaseModel, Field, ConfigDict
from pydantic_yaml import to_yaml_str

from kodexa.model import Document
from kodexa.model.objects import (
    PageUser,
    PageMembership,
    PageExecution,
    PageAction,
    PagePipeline,
    PageProject,
    PageAssistant,
    PageWorkspace,
    PageChannel,
    PageMessage,
    PageProjectTemplate,
    PageDataForm,
    PageDashboard,
    PageDataException,
    PageDocumentFamily,
    Organization,
    SlugBasedMetadata,
    Assistant,
    Execution,
    CustomEvent,
    Message,
    Channel,
    Workspace,
    DocumentFamily,
    Project,
    ProjectResourcesUpdate,
    ProjectTag,
    ProjectTemplate,
    Pipeline,
    CredentialDefinition,
    DataForm,
    Dashboard,
    ModelRuntime,
    ExtensionPack,
    Taxonomy,
    Taxon,
    Membership,
    User,
    DataAttribute,
    DataObject,
    ContentObject,
    DocumentStatus,
    Store,
    PageDataObject,
    DocumentContentMetadata,
    ModelContentMetadata,
    ModelTraining,
    PageModelTraining,
    ContentException,
    PlatformOverview,
    Action,
    PageStore,
    PageTaxonomy,
    PageAssistantDefinition,
    PageCredentialDefinition,
    DeploymentOptions,
    AssistantDefinition,
    DataException,
    ReprocessRequest,
    PageExtensionPack,
    PageOrganization,
    DocumentFamilyStatistics, MessageContext, PagePrompt, Prompt, GuidanceSet, PageGuidanceSet, DocumentEmbedding,
    DocumentExternalData, Task, PageTask, RetainedGuidance, PageRetainedGuidance,
)

logger = logging.getLogger()


class Notifier:
    """
    A class used to represent a Notifier.

    This class provides methods to log messages and handle exit events.
    """

    def __init__(self):
        pass

    def log(self, message: str):
        """
        Logs the provided message.

        Args:
            message (str): The message to be logged.
        """
        print(message)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Done")


#
# Declare all the endpoints that we will have
#
# These wrap the objects from the model and provide a simple interface to the platform that is easier to use


class OrganizationOwned(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A base class for objects that are owned by an organization.

    Attributes:
        organization (Optional[OrganizationEndpoint]): The organization that owns the object.
    """

    organization: Optional["OrganizationEndpoint"] = None

    def set_organization(self, organization):
        """
        Set the organization that this object belongs to.

        Args:
            organization (OrganizationEndpoint): The organization to set as owner.

        Returns:
            self: The instance of the class.
        """
        self.organization = organization
        return self


class ClientEndpoint(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Represents a client endpoint.
    """

    """
    Represents a client endpoint
    """
    client: Optional[Any] = Field(None, exclude=True)
    ref: Optional[str] = Field(None, exclude=False)

    def set_client(self, client):
        """
        Set the client that this endpoint is associated with.

        Args:
            client: The client to set.

        Returns:
            The endpoint.
        """
        self.client = client
        if isinstance(self, ComponentInstanceEndpoint):
            self.ref = f"{self.org_slug}/{self.slug}:{self.version}"
        return self

    def yaml(self, **kwargs):
        """
        Convert the client endpoint to a yaml string.

        Returns:
            A yaml string representation of the endpoint.
        """
        kwargs["exclude_unset"] = True
        kwargs["exclude_none"] = True

        return to_yaml_str(self, **kwargs)

    def detach(self):
        """
        Detach the client from the endpoint.

        Returns:
            A copy of the model with the client detached.
        """
        return self.model_copy()


class ProjectResourceEndpoint(ClientEndpoint):
    """
    Represents a project resource endpoint.
    """

    """
    Represents a project resource endpoint
    """
    project: Optional["ProjectEndpoint"] = Field(None)

    def set_project(self, project: "ProjectEndpoint"):
        """
        Set the project that this endpoint is associated with.

        Args:
            project (ProjectEndpoint): The project to associate with this endpoint.

        Returns:
            self: The instance of the class.
        """
        self.project = project
        return self

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        pass

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): The dictionary of the object. Defaults to None.

        Returns:
            The instance class of the endpoint.
        """
        pass

    def to_df(
            self, query="*", page=1, page_size=10, sort=None, filters: List[str] = None
    ):
        """
        Convert resources to data frame.

        Args:
            query (str, optional): The query to filter the resources. Defaults to "*".
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The size of the page. Defaults to 10.
            sort (str, optional): The sorting order. Defaults to None.
            filters (List[str], optional): The list of filters. Defaults to None.

        Returns:
            DataFrame: The DataFrame of the resources.
        """
        import pandas as pd

        df = pd.DataFrame(
            seq(self.list(query, page, page_size, sort, filters))
            .map(lambda x: x.dict())
            .to_list()
        )

        if "client" in df:
            df.drop(columns="client", axis=1)
        return df

    def stream_list(self, query="*", sort=None, filters: List[str] = None):
        return self.stream(query, sort=sort, filters=filters)

    def stream(self, query="*", sort=None, filters: List[str] = None):
        """
        Stream the list of resources.

        Args:
            query (str, optional): The query to filter the resources. Defaults to "*".
            sort (str, optional): The sorting order. Defaults to None.
            filters (List[str], optional): The list of filters. Defaults to None.

        Yields:
            The list of resources.
        """
        page_size = 5
        page = 1

        if not sort:
            sort = "id"

        while True:
            page_response = self.list(
                query=query, page=page, page_size=page_size, sort=sort, filters=filters
            )
            for resource in page_response:
                yield resource
            page += 1

    def list(
            self, query="*", page=1, page_size=10, sort=None, filters: List[str] = None
    ):
        """
        List the resources.

        Args:
            query (str, optional): The query to filter the resources. Defaults to "*".
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The size of the page. Defaults to 10.
            sort (str, optional): The sorting order. Defaults to None.
            filters (List[str], optional): The list of filters. Defaults to None.

        Returns:
            list: The list of resources.
        """

        url = f"/api/projects/{self.project.id}/{self.get_type()}"

        params = {
            "query": requests.utils.quote(query),
            "page": page,
            "pageSize": page_size,
        }

        if sort is not None:
            params["sort"] = sort

        if filters is not None:
            params["filter"] = filters

        list_response = self.client.get(url, params=params)
        return [
            self.get_instance_class().model_validate(item).set_client(self.client)
            for item in list_response.json()
        ]

    def replace(self, components):
        """
        Replace the components.

        Args:
            components (list): The list of components to replace.

        Returns:
            list: The list of replaced components.
        """
        url = f"/api/projects/{self.project.id}/{self.get_type()}"
        replace_response = self.client.put(
            url,
            [
                component.model_dump(mode="json", by_alias=True)
                for component in components
            ],
        )
        return [
            self.get_instance_class().model_validate(item).set_client(self.client)
            for item in replace_response.json()
        ]

    def find_by_name(self, name) -> Optional[Any]:
        """
        Find resource by name.

        Args:
            name (str): The name of the resource.

        Returns:
            Optional[Any]: The resource if found, None otherwise.
        """
        for resource in self.list():
            if resource.name == name:
                return resource
        return None


class ComponentEndpoint(ClientEndpoint, OrganizationOwned):
    """
    Represents a component endpoint.

    This class provides methods to interact with the component endpoint, including
    getting the type of the component, reindexing the component, finding a component
    by its slug, streaming a list of components, listing components, creating a new
    component, and getting a component by its slug.
    """

    """
    Represents a component endpoint
    """

    def get_type(self) -> str:
        """
        Get the type of the component.

        Returns:
            str: The type of the component.
        """
        pass

    def get_instance_class(self, obj_dict=None):
        """
        Get the instance class of the component.

        Args:
            obj_dict (dict, optional): The object dictionary.

        Returns:
            The instance class of the component.
        """
        pass

    def get_page_class(self, obj_dict=None):
        """
        Get the page class of the component.

        Args:
            obj_dict (dict, optional): The object dictionary.

        Returns:
            The page class of the component.
        """
        pass

    def reindex(self):
        """
        Reindex the component.
        """
        url = f"/api/{self.get_type()}/_reindex"
        self.client.post(url)

    def find_by_slug(self, slug, version=None):
        """
        Find a component by its slug.

        Args:
            slug (str): The slug of the component.
            version (str, optional): The version of the component.

        Returns:
            The component with the given slug and version, or None if no such component exists.
        """
        filters = ["slug: '" + slug + "'"]
        if version is not None:
            filters.append("version: '" + version + "'")
        component_page = self.list(filters=filters)
        if component_page.empty:
            return None
        return component_page.content[0]

    def stream_list(self, query="*", sort=None, filters: List[str] = None):
        return self.stream(query, sort, filters)

    def stream(self, query="*", sort=None, filters: List[str] = None):
        """
        Stream components matching query, sort and filters.

        Args:
            query (str, optional): The query string.
            sort (str, optional): The sort order.
            filters (List[str], optional): The list of filters.

        Yields:
            The components in the current page.
        """
        url = f"/api/{self.get_type()}/{self.organization.slug}"

        params = {
            "query": requests.utils.quote(query),
        }

        if sort is not None:
            params["sort"] = sort

        if filters is not None:
            params["filter"] = filters

        while True:
            list_response = self.client.get(url, params=params)

            # If there are no more results, exit the loop
            if not list_response.json()["content"]:
                break

            # Yield each endpoint in the current page
            for endpoint in (
                    self.get_page_class(list_response.json())
                            .model_validate(list_response.json())
                            .set_client(self.client)
                            .to_endpoints().content
            ):
                yield endpoint

            # Move to the next page
            params["page"] += 1

    def list(
            self, query="*", page=1, page_size=10, sort=None, filters: List[str] = None
    ):
        """
        List the components.

        Args:
            query (str, optional): The query string.
            page (int, optional): The page number.
            page_size (int, optional): The size of the page.
            sort (str, optional): The sort order.
            filters (List[str], optional): The list of filters.

        Returns:
            The list of components.
        """
        url = f"/api/{self.get_type()}/{self.organization.slug}"

        params = {
            "query": requests.utils.quote(query),
            "page": page,
            "pageSize": page_size,
        }

        if sort is not None:
            params["sort"] = sort

        if filters is not None:
            params["filter"] = filters

        list_response = self.client.get(url, params=params)
        return (
            self.get_page_class(list_response.json())
            .model_validate(list_response.json())
            .set_client(self.client)
            .to_endpoints()
        )

    def create(self, component):
        """
        Create a new component.

        Args:
            component: The component to be created.

        Returns:
            The created component.
        """
        url = f"/api/{self.get_type()}/{self.organization.slug}"
        get_response = self.client.post(
            url, component.model_dump(mode="json", by_alias=True)
        )
        return (
            self.get_instance_class(get_response.json())
            .model_validate(get_response.json())
            .set_client(self.client)
        )

    def get_by_slug(self, slug, version=None):
        """
        Get a component by its slug.

        Args:
            slug (str): The slug of the component.
            version (str, optional): The version of the component.

        Returns:
            The component with the given slug and version.
        """
        url = f"/api/{self.get_type()}/{self.organization.slug}/{slug}"
        if version is not None:
            url += f"/{version}"

        get_response = self.client.get(url)
        return self.get_instance_class(get_response.json()).model_validate(
            get_response.json()
        )


class EntityEndpoint(ClientEndpoint):
    """
    Represents an entity endpoint.
    """

    """
    Represents an entity endpoint
    """

    def reload(self):
        """
        Reloads the entity.

        Returns:
            The reloaded entity.
        """
        url = f"/api/{self.get_type()}/{self.id}"
        response = self.client.get(url)
        return self.model_validate(response.json()).set_client(self.client)

    def get_type(self) -> str:
        """
        Gets the type of the entity.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError()

    def create(self) -> "EntityEndpoint":
        """
        Creates the entity.

        Returns:
            EntityEndpoint: The created entity (with the ID in place)

        Raises:
            Exception: If the entity already exists.
        """
        if self.id is not None:
            raise Exception("Can't create as it already exists")

        url = f"/api/{self.get_type()}"
        response = self.client.post(url, self.model_dump(mode="json", by_alias=True))

        # We need to update the id
        self.id = response.json()["id"]
        return self.reload()

    def update(self):
        """
        Updates the entity.

        Raises:
            Exception: If the entity doesn't exist.
        """
        url = f"/api/{self.get_type()}/{self.id}"
        exists = self.client.exists(url)
        if not exists:
            raise Exception("Can't update as it doesn't exist?")
        self.client.put(url, self.model_dump(mode="json", by_alias=True))
        return self.reload()

    def delete(self):
        """
        Deletes the entity.

        Raises:
            Exception: If the entity doesn't exist.
        """
        url = f"/api/{self.get_type()}/{self.id}"
        exists = self.client.exists(url)
        if not exists:
            raise Exception("Component doesn't exist")
        self.client.delete(url)


class EntitiesEndpoint:
    """Represents an entities endpoint"""

    """Represents an entities endpoint"""

    def get_type(self) -> str:
        """Abstract method to get the type of the entity.

        Returns:
            str: The type of the entity.
        """
        raise NotImplementedError()

    def get_instance_class(self, object_dict=None):
        """Abstract method to get the instance class of the entity.

        Args:
            object_dict (dict, optional): The dictionary object of the entity.

        Returns:
            The instance class of the entity.
        """
        raise NotImplementedError()

    def get_page_class(self, object_dict=None):
        """Abstract method to get the page class of the entity.

        Args:
            object_dict (dict, optional): The dictionary object of the entity.

        Returns:
            The page class of the entity.
        """
        raise NotImplementedError()

    def __init__(
            self, client: "KodexaClient", organization: "OrganizationEndpoint" = None
    ):
        """Initialize the entities endpoint by client and organization"""
        self.client: "KodexaClient" = client
        self.organization: Optional["OrganizationEndpoint"] = organization

    def stream_list(self, query="*", sort=None, filters: List[str] = None):
        return self.stream(query, sort=sort, filters=filters)

    def stream(self, query="*", sort=None, filters: List[str] = None):
        """Stream the list of resources.

        Args:
            query (str, optional): The query to filter the resources.
            sort (str, optional): The field to sort the resources.
            filters (List[str], optional): The list of filters to apply on the resources.

        Yields:
            The resources matching the query, sort and filters.
        """
        page_size = 5
        page = 1
        if not sort:
            sort = "id"

        while True:
            page_response = self.list(
                query=query, page=page, page_size=page_size, sort=sort, filters=filters
            )
            if not page_response.content:
                break
            for resource in page_response.content:
                yield resource
            page += 1

    def list(
            self, query="*", page=1, page_size=10, sort=None, filters: List[str] = None
    ):
        """List the resources.

        Args:
            query (str, optional): The query to filter the resources.
            page (int, optional): The page number to fetch the resources.
            page_size (int, optional): The number of resources to fetch per page.
            sort (str, optional): The field to sort the resources.
            filters (List[str], optional): The list of filters to apply on the resources.

        Returns:
            The page of resources matching the query, sort and filters.
        """
        url = f"/api/{self.get_type()}"

        params = {"query": query, "page": page, "pageSize": page_size}

        if sort is not None:
            params["sort"] = sort

        if filters is not None:
            params["filter"] = filters

        if self.organization is not None:
            if "filter" not in params:
                params["filter"] = [f"organization.id: '{self.organization.id}'"]
            else:
                params["filter"].append(f"organization.id: '{self.organization.id}'")

        list_response = self.client.get(url, params=params)
        return (
            self.get_page_class()
            .model_validate(list_response.json())
            .set_client(self.client)
        )

    def find_by_organization(self, organization: Organization) -> PageProject:
        """Find projects by organization.

        Args:
            organization (Organization): The organization to find the projects.

        Returns:
            PageProject: The page of projects belonging to the organization.
        """
        url = f"/api/{self.get_type()}"
        get_response = self.client.get(
            url, params={"filter": f"organization.id: '{organization.id}'"}
        )
        return (
            self.get_page_class()
            .model_validate(get_response.json())
            .set_client(self.client)
        )

    def get(self, entity_id: str) -> "EntityEndpoint":
        """Get an entity by id.

        Args:
            entity_id (str): The id of the entity.

        Returns:
            EntityEndpoint: The entity matching the id.
        """
        url = f"/api/{self.get_type()}/{entity_id}"
        get_response = self.client.get(url)
        return (
            self.get_instance_class()
            .model_validate(get_response.json())
            .set_client(self.client)
        )

    def create(self, new_entity: EntityEndpoint) -> EntityEndpoint:
        """Create an entity.

        Args:
            new_entity (EntityEndpoint): The new entity to create.

        Returns:
            EntityEndpoint: The created entity.
        """
        url = f"/api/{self.get_type()}"

        create_response = self.client.post(
            url, body=json.loads(new_entity.model_dump_json(by_alias=True))
        )
        return (
            self.get_instance_class()
            .model_validate(create_response.json())
            .set_client(self.client)
        )

    def delete(self, self_id: str) -> None:
        """Delete an entity by id.

        Args:
            self_id (str): The id of the entity to delete.
        """
        url = f"/api/{self.get_type()}/{self_id}"
        self.client.delete(url)


class OrganizationsEndpoint(EntitiesEndpoint):
    """
    Represents the organization endpoint
    """

    """
    Represents the organization endpoint
    """

    def get_page_class(self, object_dict=None):
        """
        Get the page class for the organization endpoint.

        Args:
            object_dict (dict, optional): Dictionary of object data. Defaults to None.

        Returns:
            PageOrganizationEndpoint: The page class for the organization endpoint.
        """
        return PageOrganizationEndpoint

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class for the organization endpoint.

        Args:
            object_dict (dict, optional): Dictionary of object data. Defaults to None.

        Returns:
            OrganizationEndpoint: The instance class for the organization endpoint.
        """
        return OrganizationEndpoint

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, 'organizations'.
        """
        return "organizations"

    def find_by_slug(self, slug) -> Optional["OrganizationEndpoint"]:
        """
        Find an organization by its slug.

        Args:
            slug (str): The slug of the organization.

        Returns:
            Optional[OrganizationEndpoint]: The organization with the given slug, or None if no such organization exists.
        """
        organizations = self.list(filters=["slug: '" + slug + "'"])
        if organizations.number_of_elements == 0:
            return None
        return organizations.content[0]


class PageEndpoint(ClientEndpoint):
    """
    Represents a page endpoint.
    """

    """
    Represents a page endpoint
    """

    def get_type(self) -> Optional[str]:
        """
        Get the type of the page endpoint.

        Returns:
            Optional[str]: The type of the page endpoint. None if not set.
        """
        return None

    def to_df(self):
        """
        Convert the page to a dataframe.

        Returns:
            DataFrame: The page converted to a dataframe.
        """
        import pandas as pd

        df = pd.DataFrame(seq(self.content).map(lambda x: x.dict()).to_list())

        if "client" in df:
            df.drop(columns="client", axis=1)
        return df

    def get(self, index: int) -> "ComponentInstanceEndpoint":
        """
        Get a component by index.

        Args:
            index (int): The index of the component to get.

        Returns:
            ComponentInstanceEndpoint: The component at the given index.

        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index >= len(self.content):
            raise IndexError(f"Index {index} out of range")
        return self.content[index]

    def set_client(self, client):
        """
        Set the client for the page.

        Args:
            client: The client to set.

        Returns:
            The page with the client set.
        """
        ClientEndpoint.set_client(self, client)
        return self.to_endpoints()

    def to_endpoints(self):
        """
        Convert the page to endpoints.

        Returns:
            The page converted to endpoints.
        """
        self.content = (
            seq(self.content)
            .map(
                lambda x: self.client.deserialize(
                    x.model_dump(by_alias=True), component_type=self.get_type()
                )
            )
            .to_list()
        )
        return self


class PageTaxonomyEndpoint(PageTaxonomy, PageEndpoint):
    """Handles the endpoint requests for the Page Taxonomy.

    This class inherits from both the PageTaxonomy and PageEndpoint classes.
    It is used to manage the endpoint requests related to the taxonomy of a page.

    Note:
        Currently, this class doesn't have any methods or attributes.
        It's a placeholder for future methods and attributes related to
        the endpoint requests of the page taxonomy.
    """

    pass


class PageStoreEndpoint(PageStore, PageEndpoint):
    """This class inherits from the PageStore and PageEndpoint classes.

    It doesn't have any additional attributes or methods.

    Attributes:
        None

    Methods:
        None
    """

    pass


class PageModelRuntimeEndpoint(PageStore, PageEndpoint):
    """A class that inherits from PageStore and PageEndpoint.

    This class is used to create a runtime endpoint for a page model.

    Attributes:
        None

    Methods:
        None
    """

    pass


class PageExtensionPackEndpoint(PageExtensionPack, PageEndpoint):
    """Handles the endpoint for the Page Extension Pack.

    This class inherits from both the PageExtensionPack and PageEndpoint classes.
    Currently, it doesn't add any additional functionality to its parent classes.

    Note:
        This class is currently a placeholder and may have additional methods and attributes
        added in the future.
    """

    pass


class PageAssistantDefinitionEndpoint(PageAssistantDefinition, PageEndpoint):
    """Handles the endpoint definitions for the Page Assistant.

    This class is a combination of the PageAssistantDefinition and PageEndpoint classes.
    It is used to define the endpoints for the Page Assistant.

    Note:
        This class does not have any methods or attributes. It is used only for inheritance purposes.

    """

    pass


class PageCredentialDefinitionEndpoint(PageCredentialDefinition, PageEndpoint):
    """Handles the endpoint for the Page Credential Definition.

    This class inherits from the PageCredentialDefinition and PageEndpoint classes.

    Attributes:
        None

    Methods:
        None
    """

    pass


class PageUserEndpoint(PageUser, PageEndpoint):
    """
    This class represents a page user endpoint. It inherits from both PageUser and PageEndpoint classes.
    """

    """
    Represents a page user endpoint
    """

    def get_type(self) -> Optional[str]:
        """
        Get the type of the page user.

        Returns:
            Optional[str]: Returns the type of the page user. In this case, it returns "user".
        """
        return "user"


class PageMembershipEndpoint(PageMembership, PageEndpoint):
    """
    Represents a page membership endpoint.

    Attributes:
        None

    Methods:
        get_type: Get the type of the endpoint.
    """

    """Represents a page membership endpoint"""

    def get_type(self) -> Optional[str]:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, "membership".
        """
        return "membership"


class PageExecutionEndpoint(PageExecution, PageEndpoint):
    """Represents a page execution endpoint.

    This class is used to represent a page execution endpoint. It inherits from
    both PageExecution and PageEndpoint classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a page execution endpoint"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case, it
        will always return "execution".

        Returns:
            str: The type of the endpoint, "execution".
        """
        return "execution"


class PageActionEndpoint(PageAction, PageEndpoint):
    """Represents a page action endpoint.

    This class is used to represent a page action endpoint which is a combination of
    PageAction and PageEndpoint. It provides a method to get the type of the endpoint.
    """

    """Represents a page action endpoint"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case, it will always
        return "action".

        Returns:
            Optional[str]: The type of the endpoint, in this case "action".
        """
        return "action"


class PagePipelineEndpoint(PagePipeline, PageEndpoint):
    """
    Represents a page pipeline endpoint.

    This class is used to represent a page pipeline endpoint. It inherits from both
    the PagePipeline and PageEndpoint classes.
    """

    """Represents a page pipeline endpoint"""

    def get_type(self) -> Optional[str]:
        """
        Get the type of the endpoint.

        This method is used to get the type of the endpoint. It returns a string
        that represents the type of the endpoint.

        Returns:
            Optional[str]: The type of the endpoint. Returns "pipeline" for this class.
        """
        return "pipeline"


class PageTaskEndpoint(PageTask, PageEndpoint):
    def get_type(self) -> Optional[str]:
        return "task"


class PageRetainedGuidanceEndpoint(PageRetainedGuidance, PageEndpoint):
    """Represents a page retained guidance endpoint.

    This class is used to represent a page retained guidance endpoint which is a
    combination of a page retained guidance and a page endpoint.

    Attributes:
        None
    """

    """Represents a page retained guidance endpoint"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case,
        it will always return "retainedGuidance".

        Returns:
            str: The type of the endpoint, which is "retainedGuidance".
        """
        return "retainedGuidance"


class PageProjectEndpoint(PageProject, PageEndpoint):
    """Represents a page project endpoint.

    This class is used to represent a page project endpoint which is a
    combination of a page project and a page endpoint.

    Attributes:
        None
    """

    """Represents a page project endpoint"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case,
        it will always return "project".

        Returns:
            str: The type of the endpoint, which is "project".
        """
        return "project"


class PageAssistantEndpoint(PageAssistant, PageEndpoint):
    """
    Represents a page assistant endpoint.

    This class is used to represent a page assistant endpoint which is a
    combination of a page assistant and a page endpoint.
    """

    """Represents a page assistant endpoint"""

    def get_type(self) -> Optional[str]:
        """
        Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case,
        the type is always "assistant".

        Returns:
            Optional[str]: The type of the endpoint, which is "assistant".
        """
        return "assistant"


class PageWorkspaceEndpoint(PageWorkspace, PageEndpoint):
    """Represents a page workspace endpoints

    This class is used to represent the endpoints of a page workspace. It inherits from
    the PageWorkspace and PageEndpoint classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a page workspace endpoints"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint. In this case, it will always
        return "workspace".

        Returns:
            str: The type of the endpoint, "workspace".
        """
        return "workspace"


class PageChannelEndpoint(PageChannel, PageEndpoint):
    """Represents a page channel endpoints.

    This class is used to represent the endpoints of a page channel. It inherits from
    the PageChannel and PageEndpoint classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a page channel endpoints"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. It returns a string
        representing the type of the endpoint.

        Returns:
            str: The type of the endpoint. Returns "channel".
        """
        return "channel"


class PageMessageEndpoint(PageMessage, PageEndpoint):
    """
    Represents a page message endpoints.

    Attributes:
        None

    Methods:
        get_type: Get the type of the endpoint.
    """

    """Represents a page message endpoints"""

    def get_type(self) -> Optional[str]:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, "message".
        """
        return "message"


class PageProjectTemplateEndpoint(PageProjectTemplate, PageEndpoint):
    """This class inherits from the PageProjectTemplate and PageEndpoint classes.

    It doesn't contain any additional attributes or methods.

    Attributes:
        None

    Methods:
        None
    """

    pass


class PageOrganizationEndpoint(PageOrganization, PageEndpoint):
    """Represents a page organization endpoint

    This class is used to represent a page organization endpoint. It inherits from
    the PageOrganization and PageEndpoint classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a page organization endpoint"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint. In this case, it will
        always return "organization".

        Args:
            None

        Returns:
            Optional[str]: The type of the endpoint, which is "organization".
        """
        return "organization"


class PageDataFormEndpoint(PageDataForm, PageEndpoint):
    """Represents a page data form endpoint.

    This class is used to represent a page data form endpoint. It inherits from
    both the PageDataForm and PageEndpoint classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a page data form endpoint"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case, it
        will always return the string "dataForm".

        Returns:
            str: The type of the endpoint, "dataForm".
        """
        return "dataForm"


class PageDashboardEndpoint(PageDashboard, PageEndpoint):
    """Represents a page data form endpoint.

    This class is used to represent a page data form endpoint. It inherits from
    the PageDashboard and PageEndpoint classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a page data form endpoint"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case, it
        always returns "dashboard".

        Returns:
            str: The type of the endpoint, "dashboard".
        """
        return "dashboard"


class PageDataExceptionEndpoint(PageDataException, PageEndpoint):
    """Represents a page of data exceptions endpoint.

    This class is used to represent a page of data exceptions endpoint. It is a subclass of
    both PageDataException and PageEndpoint.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a page of data exceptions endpoint"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. It returns a string that
        represents the type of the endpoint.

        Args:
            None

        Returns:
            Optional[str]: The type of the endpoint. Returns "exception" for this class.
        """
        return "exception"


class PageDocumentFamilyEndpoint(PageDocumentFamily, PageEndpoint):
    """Represents a page document family endpoint.

    This class is used to represent a page document family endpoint. It inherits from
    PageDocumentFamily and PageEndpoint classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a page document family endpoint"""

    def get_type(self) -> Optional[str]:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. It returns a string
        representing the type of the endpoint.

        Returns:
            Optional[str]: The type of the endpoint, "documentFamily".
        """
        return "documentFamily"


class OrganizationEndpoint(Organization, EntityEndpoint):
    """
    Represents an organization endpoint.

    This class inherits from the Organization and EntityEndpoint classes.
    """

    """
    Represents an organization endpoint
    """

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "organizations".
        """
        return "organizations"

    @property
    def projects(self) -> "ProjectsEndpoint":
        """
        Get the projects endpoint of the organization.

        Returns:
            ProjectsEndpoint: The projects endpoint of the organization.
        """
        return ProjectsEndpoint(self.client, self)

    def suspend(self):
        """
        Suspend the organization.

        This method sends a PUT request to the organization's suspend endpoint.
        """
        self.client.put(f"/api/organizations/{self.id}/suspend")

    def deploy(self, component: ComponentEndpoint) -> "ComponentInstanceEndpoint":
        """
        Deploy a component to the organization.

        Args:
            component (ComponentEndpoint): The component to be deployed.

        Returns:
            ComponentInstanceEndpoint: The endpoint of the deployed component instance.
        """
        url = f"/api/{component.get_type()}/{self.slug}"
        response = self.client.post(
            url, body=component.model_dump(mode="json", by_alias=True)
        )
        return self.client.deserialize(response.json())

    @property
    def model_runtimes(self) -> "ModelRuntimesEndpoint":
        """
        Get the model runtimes endpoint of the organization.

        Returns:
            ModelRuntimesEndpoint: The model runtimes endpoint of the organization.
        """
        return ModelRuntimesEndpoint().set_organization(self).set_client(self.client)

    @property
    def extension_packs(self) -> "ExtensionPacksEndpoint":
        """
        Get the extension packs endpoint of the organization.

        Returns:
            ExtensionPacksEndpoint: The extension packs endpoint of the organization.
        """
        return ExtensionPacksEndpoint().set_organization(self).set_client(self.client)

    @property
    def project_templates(self) -> "ProjectTemplatesEndpoint":
        """
        Get the project templates endpoint of the organization.

        Returns:
            ProjectTemplatesEndpoint: The project templates endpoint of the organization.
        """
        return ProjectTemplatesEndpoint().set_organization(self).set_client(self.client)

    @property
    def assistant_definitions(self) -> "AssistantDefinitionsEndpoint":
        """
        Get the assistant definitions endpoint of the organization.

        Returns:
            AssistantDefinitionsEndpoint: The assistant definitions endpoint of the organization.
        """
        return (
            AssistantDefinitionsEndpoint()
            .set_organization(self)
            .set_client(self.client)
        )

    @property
    def guidance_sets(self) -> "GuidanceSetsEndpoint":
        """
        Get the guidance sets endpoint of the organization.

        Returns:
            GuidanceSetsEndpoint: The guidance sets endpoint of the organization.
        """
        return (
            GuidanceSetsEndpoint()
            .set_organization(self)
            .set_client(self.client)
        )

    @property
    def credentials(self):
        """
        Get the credentials endpoint of the organization.

        Returns:
            CredentialDefinitionsEndpoint: The credentials endpoint of the organization.
        """
        return (
            CredentialDefinitionsEndpoint()
            .set_organization(self)
            .set_client(self.client)
        )

    @property
    def data_forms(self):
        """
        Get the data forms endpoint of the organization.

        Returns:
            CredentialDefinitionsEndpoint: The data forms endpoint of the organization.
        """
        return (
            CredentialDefinitionsEndpoint()
            .set_organization(self)
            .set_client(self.client)
        )

    @property
    def stores(self):
        """
        Get the stores endpoint of the organization.

        Returns:
            StoresEndpoint: The stores endpoint of the organization.
        """
        return StoresEndpoint().set_client(self.client).set_organization(self)

    @property
    def taxonomies(self):
        """
        Get the taxonomies endpoint of the organization.

        Returns:
            TaxonomiesEndpoint: The taxonomies endpoint of the organization.
        """
        return TaxonomiesEndpoint().set_client(self.client).set_organization(self)

    @property
    def available_templates(self, page=1, page_size=10, query="*"):
        """
        Get the available templates for the organization.

        Returns:
            MarketplaceEndpoint: The marketplace endpoint of the organization.
        """
        url = f"/api/organizations/{self.id}/availableTemplates"
        response = self.client.get(url, params={"page": page, "pageSize": page_size, "query": query})
        return PageProjectTemplateEndpoint.model_validate(response.json()).set_client(self.client)

    @property
    def available_models(self, page=1, page_size=10, query="*"):
        """
        Get the available models for the organization.

        Returns:
            MarketplaceEndpoint: The marketplace endpoint of the organization.
        """
        url = f"/api/organizations/{self.id}/availableModels"
        response = self.client.get(url, params={"page": page, "pageSize": page_size, "query": query})
        return PageStoreEndpoint.model_validate(response.json()).set_client(self.client)

    @property
    def available_assistants(self, page=1, page_size=10, query="*"):
        """
        Get the available assistants for the organization.

        Returns:
            MarketplaceEndpoint: The marketplace endpoint of the organization.
        """
        url = f"/api/organizations/{self.id}/availableAssistants"
        response = self.client.get(url, params={"page": page, "pageSize": page_size, "query": query})
        return PageAssistantDefinitionEndpoint.model_validate(response.json()).set_client(self.client)

    def get_subscriptions(self, page: int = 1, page_size: int = 10) -> "PageProductSubscriptionEndpoint":
        """
        Get the subscriptions of the organization.

        Returns:
            The subscriptions of the organization.
        """
        url = f"/api/productSubscriptions"
        params = {
            "filter": f"organization.id: '{self.id}'",
            "page": page,
            "pageSize": page_size
        }
        response = self.client.get(url, params=params)

        from kodexa.model.entities.product_subscription import PageProductSubscriptionEndpoint
        return PageProductSubscriptionEndpoint.model_validate(response.json()).set_client(self.client)

    def remove_subscription(self, subscription: "ProductSubscription") -> None:
        """
        Remove a subscription from the organization.

        Args:
            subscription_id (str): The id of the subscription to remove.
        """
        url = f"/api/productSubscriptions/{subscription.id}"
        self.client.delete(url)

    def add_subscription(self, product: "Product") -> None:
        """
        Add a subscription to the organization.

        Args:
            product (Product): The product to subscribe to.
        """
        url = f"/api/productSubscriptions"
        from kodexa.model.entities.product_subscription import ProductSubscription
        new_product_subscription = ProductSubscription(organization=self.detach(), product=product)
        print(new_product_subscription.model_dump_json(by_alias=True))
        self.client.post(url, body=json.loads(new_product_subscription.model_dump_json(by_alias=True)))


class ComponentsEndpoint(ClientEndpoint):
    """
    Represents a components endpoint.

    Attributes:
        organization (OrganizationEndpoint): The organization endpoint that the components endpoint belongs to.
    """

    """
    Represents a components endpoint
    """

    def __init__(self, organization: OrganizationEndpoint):
        """Initialize the components endpoint by setting the organization"""
        self.organization = organization


class ComponentInstanceEndpoint(ClientEndpoint, SlugBasedMetadata):
    """
    Represents a component instance endpoint.
    """

    """
    Represents a component instance endpoint
    """

    def get_type(self) -> str:
        """
        Get the type of the component instance.

        Raises:
            NotImplementedError: This method should be overridden in a subclass.

        Returns:
            str: The type of the component instance.
        """
        raise NotImplementedError()

    def post_deploy(self) -> List[str]:
        """
        Perform actions after the deployment of the component instance.

        Returns:
            List[str]: A list of strings representing the post-deployment actions.
        """
        return []

    def create(self):
        """
        Create the component instance.

        Raises:
            Exception: If the component instance already exists.

        Returns:
            ComponentInstanceEndpoint: The created component instance.
        """
        url = f"/api/{self.get_type()}/{self.ref.replace(':', '/')}"
        exists = self.client.exists(url)
        if exists:
            raise Exception("Can't create as it already exists")
        url = f"/api/{self.get_type()}/{self.org_slug}"
        self.client.post(url, self.model_dump(mode="json", by_alias=True))
        return self

    def update(self):
        """
        Update the component instance.

        Raises:
            Exception: If the component instance does not exist.

        Returns:
            ComponentInstanceEndpoint: The updated component instance.
        """
        url = f"/api/{self.get_type()}/{self.ref.replace(':', '/')}"
        exists = self.client.exists(url)
        if not exists:
            raise Exception("Can't update as it doesn't exist?")
        self.client.put(url, self.model_dump(mode="json", by_alias=True))
        return self

    def delete(self):
        """
        Delete the component instance.

        Raises:
            Exception: If the component instance does not exist.
        """
        url = f"/api/{self.get_type()}/{self.ref.replace(':', '/')}"
        exists = self.client.exists(url)
        if not exists:
            raise Exception("Component doesn't exist")
        self.client.delete(url)

    def deploy(self, update=False):
        """
        Deploy the component instance.

        Args:
            update (bool, optional): Whether to update the component instance if it already exists. Defaults to False.

        Raises:
            Exception: If the component instance does not have an organization or a slug, or if the component instance
            already exists and update is False.

        Returns:
            List[str]: A list of strings representing the post-deployment actions.
        """
        if self.org_slug is None:
            raise Exception(
                "We can not deploy this component since it does not have an organization"
            )
        if self.slug is None:
            raise Exception(
                "We can not deploy this component since it does not have a slug"
            )

        self.ref = f"{self.org_slug}/{self.slug}{f':{self.version}' if self.version is not None else ''}"

        url = f"/api/{self.get_type()}/{self.ref.replace(':', '/')}"
        exists = self.client.exists(url)
        if not update and exists:
            raise Exception(f"Component {self.ref} already exists")

        if exists:
            response = self.client.put(url, self.model_dump(mode="json", by_alias=True))
            process_response(response)
            return self.post_deploy()

        response = self.client.post(
            f"/api/{self.get_type()}/{self.org_slug}",
            self.model_dump(mode="json", by_alias=True),
        )
        process_response(response)
        return self.post_deploy()


class AssistantEndpoint(Assistant, ClientEndpoint):
    """Represents an assistant endpoint.

    This class provides methods to manage an assistant endpoint including updating, deleting,
    activating, deactivating, scheduling, setting stores, getting stores, getting executions,
    getting event types, getting event type options, and sending events.
    """

    """Represents an assistant endpoint"""

    def update(self) -> "AssistantEndpoint":
        """Update the assistant.

        Returns:
            AssistantEndpoint: The updated assistant endpoint.
        """
        url = f"/api/projects/{self.project.id}/assistants/{self.id}"
        response = self.client.put(
            url, body=self.model_dump(mode="json", by_alias=True)
        )
        return AssistantEndpoint.model_validate(response.json()).set_client(self.client)

    def set_memory(self, key: str, data: dict):
        """
        Set the memory of the assistant.

        :param key:
        :param data:
        :return:
        """
        url = f"/api/assistants/{self.id}/memory/{key}"
        response = self.client.put(url, body={
            'key': key,
            'data': data
        })
        return response.json()

    def get_memory(self, key: str):
        """
        Get the memory of the assistant.
        :param key:
        :return:
        """
        url = f"/api/assistants/{self.id}/memory/{key}"
        response = self.client.get(url)
        return response.json()["data"]

    def delete(self):
        """Delete the assistant."""
        url = f"/api/projects/{self.project.id}/assistants/{self.id}"
        self.client.delete(url)

    def activate(self):
        """Activate the assistant."""
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/activate"
        response = self.client.put(url)
        self.change_sequence = response.json().get("changeSequence")

    def deactivate(self):
        """Deactivate the assistant."""
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/deactivate"
        response = self.client.put(url)
        self.change_sequence = response.json().get("changeSequence")

    def schedule(self):
        """Schedule the assistant."""
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/schedule"
        self.client.put(url)

    def set_stores(self, stores: List["DocumentStoreEndpoint"]):
        """Set the stores of the assistant.

        Args:
            stores (List[DocumentStoreEndpoint]): The list of stores to be set.

        Returns:
            AssistantEndpoint: The updated assistant endpoint.
        """
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/stores"
        response = self.client.put(
            url, body=[store.model_dump(mode="json", by_alias=True) for store in stores]
        )
        self.change_sequence = response.json().get("changeSequence")
        return self

    def get_stores(self) -> List["DocumentStoreEndpoint"]:
        """Get the stores of the assistant.

        Returns:
            List[DocumentStoreEndpoint]: The list of stores of the assistant.
        """
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/stores"
        response = self.client.get(url)
        return [
            DocumentStoreEndpoint.model_validate(store).set_client(self.client)
            for store in response.json()
        ]

    def executions(self) -> List["Execution"]:
        """Get the executions of the assistant.

        Returns:
            List[Execution]: The list of executions of the assistant.
        """
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/executions"
        response = self.client.get(url)
        return [Execution.model_validate(execution) for execution in response.json()]

    def get_event_type(self, event_type: str) -> Optional["CustomEvent"]:
        """Get the event type of the assistant.

        Args:
            event_type (str): The name of the event type.

        Returns:
            Optional[CustomEvent]: The custom event if found, None otherwise.
        """
        for event_type in self.definition.event_types:
            if event_type.name == event_type:
                return event_type

        return None

    def get_event_type_options(
            self, event_type: str, training: bool = False
    ) -> Dict[str, Any]:
        """Get the event type options of the assistant.

        Args:
            event_type (str): The name of the event type.
            training (bool, optional): Whether to get training options. Defaults to False.

        Returns:
            Dict[str, Any]: The event type options.
        """
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/events/{event_type}/options"
        event_type_options = self.client.get(url, params={"training": training})
        return event_type_options.json()

    def send_event(self, event_type: str, options: dict) -> "ExecutionEndpoint":
        """Send an event to the assistant.

        Args:
            event_type (str): The type of the event.
            options (dict): The options of the event.

        Returns:
            ExecutionEndpoint: The execution endpoint of the event.
        """
        url = f"/api/projects/{self.project.id}/assistants/{self.id}/ekodexsavents"
        event_object = {"eventType": event_type, "options": json.dumps(options)}
        response = self.client.post(url, data=event_object, files={})
        process_response(response)
        return ExecutionEndpoint.model_validate(response.json()).set_client(self.client)


class ProjectAssistantsEndpoint(ProjectResourceEndpoint):
    """Represents a project assistants endpoint.

    This class is used to interact with the project assistants endpoint of the API.
    """

    """Represents a project assistants endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case 'assistants'.
        """
        return "assistants"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the project assistants endpoint.

        Args:
            object_dict (dict, optional): Dictionary representation of the object. Defaults to None.

        Returns:
            AssistantEndpoint: The instance class of the project assistants endpoint.
        """
        return AssistantEndpoint

    def get_names(self):
        """Get the names of the assistants.

        Returns:
            list: A list of names of the assistants.
        """
        return [assistant.name for assistant in self.list()]

    def find_by_id(self, id: str) -> Optional[AssistantEndpoint]:
        """Find assistant by ID.

        Args:
            id (str): The ID of the assistant to find.

        Returns:
            Optional[AssistantEndpoint]: The assistant with the given ID, or None if not found.
        """
        for resource in self.list():
            if resource.id == id:
                return resource
        return None

    def create(self, assistant: Assistant) -> AssistantEndpoint:
        """Create an assistant.

        Args:
            assistant (Assistant): The assistant to create.

        Returns:
            AssistantEndpoint: The created assistant.
        """
        url = f"/api/projects/{self.project.id}/assistants"
        response = self.client.post(
            url, body=assistant.model_dump(mode="json", by_alias=True)
        )
        return AssistantEndpoint.model_validate(response.json()).set_client(self.client)


class ProjectDocumentStoresEndpoint(ProjectResourceEndpoint):
    """Represents a project document stores endpoint.

    This class is used to represent a project document stores endpoint in the system.
    """

    """Represents a project document stores endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "documentStores"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the project document stores endpoint.

        This method is used to get the instance class of the project document stores endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            DocumentStoreEndpoint: The instance class of the project document stores endpoint.
        """
        return DocumentStoreEndpoint


class ProjectDashboardsEndpoint(ProjectResourceEndpoint):
    """Represents a project dashboards endpoint.

    This class is used to represent a project document stores endpoint in the system.
    """

    """Represents a project document stores endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "dashboards"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the project document stores endpoint.

        This method is used to get the instance class of the project document stores endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            DocumentStoreEndpoint: The instance class of the project document stores endpoint.
        """
        return DashboardEndpoint


class GuidanceSetEndpoint(ComponentInstanceEndpoint, GuidanceSet):

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, "guidance".
        """
        return "guidance"


class PageGuidanceSetEndpoint(PageGuidanceSet, PageEndpoint):
    """Handles the endpoint for the Page GuidanceSetEndpoint

    This class inherits from both the GuidanceSetEndpoint and PageEndpoint classes.
    Currently, it doesn't add any additional functionality to its parent classes.

    Note:
        This class is currently a placeholder and may have additional methods and attributes
        added in the future.
    """

    pass


class PromptEndpoint(ComponentInstanceEndpoint, Prompt):

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, "prompts".
        """
        return "prompts"


class PagePromptEndpoint(PagePrompt, PageEndpoint):
    """Handles the endpoint for the Page Prompt

    This class inherits from both the PromptEndpoint and PageEndpoint classes.
    Currently, it doesn't add any additional functionality to its parent classes.

    Note:
        This class is currently a placeholder and may have additional methods and attributes
        added in the future.
    """

    pass


class ProjectDataFormsEndpoint(ProjectResourceEndpoint):
    """Represents a project data forms endpoint.

    This class is used to represent a project taxonomies endpoint in the system.
    """

    """Represents a project taxonomies endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "dataForms"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the project data form endpoint.

        This method is used to get the instance class of the project dataform endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            TaxonomyEndpoint: The instance class of the project taxonomies endpoint.
        """
        return DataFormEndpoint


class ProjectTaxonomiesEndpoint(ProjectResourceEndpoint):
    """Represents a project taxonomies endpoint.

    This class is used to represent a project taxonomies endpoint in the system.
    """

    """Represents a project taxonomies endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "taxonomies"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the project taxonomies endpoint.

        This method is used to get the instance class of the project taxonomies endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            TaxonomyEndpoint: The instance class of the project taxonomies endpoint.
        """
        return TaxonomyEndpoint


class ProjectGuidanceSetsEndpoint(ProjectResourceEndpoint):

    def get_type(self) -> str:
        return "guidance"

    def get_instance_class(self, object_dict=None):
        return GuidanceSetEndpoint


class ProjectDataFormEndpoint(ProjectResourceEndpoint):

    def get_type(self) -> str:
        return "dataForms"

    def get_instance_class(self, object_dict=None):
        return DataFormEndpoint


class ProjectDashboardEndpoint(ProjectResourceEndpoint):

    def get_type(self) -> str:
        return "dashboards"

    def get_instance_class(self, object_dict=None):
        return DashboardEndpoint


class ProjectStoresEndpoint(ProjectResourceEndpoint):
    """Represents a project stores endpoint"""

    """Represents a project stores endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case 'stores'.
        """
        return "stores"

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the project stores endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the store type. Defaults to None.

        Returns:
            DocumentStoreEndpoint/ModelStoreEndpoint/DataStoreEndpoint: The instance class of the project stores endpoint.

        Raises:
            ValueError: If the store type is unknown.
        """
        if object_dict["storeType"] == "DOCUMENT":
            return DocumentStoreEndpoint
        elif object_dict["storeType"] == "MODEL":
            return ModelStoreEndpoint
        elif object_dict["storeType"] == "TABLE":
            return DataStoreEndpoint
        else:
            raise ValueError(f"Unknown store type {object_dict['storeType']}")


class ProjectDataStoresEndpoint(ProjectResourceEndpoint):
    """Represents a project data stores endpoint.

    This class is used to represent a project data stores endpoint in the system.
    """

    """Represents a project data stores endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "dataStores"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the project data stores endpoint.

        This method is used to get the instance class of the project data stores endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            DataStoreEndpoint: The instance class of the project data stores endpoint.
        """
        return DataStoreEndpoint


class ProjectModelStoresEndpoint(ProjectResourceEndpoint):
    """Represents a project model stores endpoint.

    This class is used to represent a project model stores endpoint in the system.

    Attributes:
        None
    """

    """Represents a project model stores endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Args:
            None

        Returns:
            str: The type of the endpoint.
        """
        return "modelStores"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the project model stores endpoint.

        This method is used to get the instance class of the project model stores endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data. Defaults to None.

        Returns:
            ModelStoreEndpoint: The instance class of the project model stores endpoint.
        """
        return ModelStoreEndpoint


class MessageEndpoint(EntityEndpoint, Message):
    """Represents a message endpoint.

    This class is used to represent a message endpoint which is a combination of EntityEndpoint and Message.
    """

    """Represents a message endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "messages".
        """
        return "messages"


class ChannelEndpoint(EntityEndpoint, Channel):
    """Represents a channel endpoint.

    This class is used to represent a channel endpoint in a communication system.
    It provides methods to get the type of the endpoint and to send a text message.
    """

    """Represents a channel endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case, it will always return 'channels'.

        Returns:
            str: The type of the endpoint, 'channels'.
        """
        return "channels"

    def send_text_message(self, content: str) -> MessageEndpoint:
        """Send a text message.

        This method is used to send a text message through the channel endpoint. It creates a new message,
        sets the client, channel, content, and message type, and then creates the message.

        Args:
            content (str): The content of the message to be sent.

        Returns:
            MessageEndpoint: The created message endpoint.
        """
        new_message = MessageEndpoint().set_client(self.client)
        new_message.channel = self.detach()
        new_message.content = content
        new_message.message_type = "TEXT"
        return new_message.create()

    def send_message(self, message: Message) -> MessageEndpoint:
        """Send a message.

        This method is used to send a message through the channel endpoint. It sets the client, channel,
        and message type, and then creates the message.

        Args:
            message (Message): The message to be sent.
        """

        # We need to convert the Message into a MessageEndpoint
        message_endpoint = MessageEndpoint().set_client(self.client)
        message_endpoint.channel = self.detach()
        message_endpoint.message_type = message.message_type
        message_endpoint.content = message.content
        message_endpoint.block = message.block
        message_endpoint.feedback = message.feedback
        message_endpoint.assistant = message.assistant
        message_endpoint.user = message.user
        message_endpoint.context = message.context
        return message_endpoint.create()


class WorkspaceEndpoint(EntityEndpoint, Workspace):
    """Represents a workspace endpoint"""

    """Represents a workspace endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "workspaces"

    def add_document_family(self, document_family: DocumentFamily):
        """
        Add a document family to the workspace.

        Args:
            document_family (DocumentFamily): The document family to be added.
        """
        url = f"/api/workspaces/{self.id}/documentFamilies"
        response = self.client.post(
            url, body=document_family.model_dump(mode="json", by_alias=True)
        )
        process_response(response)

    def remove_document_family(self, document_family: DocumentFamily):
        """
        Remove a document family from the workspace.

        Args:
            document_family (DocumentFamily): The document family to be removed.
        """
        url = f"/api/workspaces/{self.id}/documentFamilies/{document_family.id}"
        response = self.client.delete(url)
        process_response(response)

    def list_document_families(
            self, page_size=10, page=1
    ) -> PageDocumentFamilyEndpoint:
        """
        List all document families in the workspace.

        Args:
            page_size (int, optional): The number of document families per page. Defaults to 10.
            page (int, optional): The page number. Defaults to 1.

        Returns:
            PageDocumentFamilyEndpoint: The endpoint for the page of document families.
        """
        url = f"/api/workspaces/{self.id}/documentFamilies"
        response = self.client.get(url, {"pageSize": page_size, "page": page})
        process_response(response)
        return PageDocumentFamilyEndpoint.model_validate(response.json()).set_client(
            self.client
        )

    def get_channel(self):
        """
        Get the channel of the workspace.

        Returns:
            ChannelEndpoint: The endpoint for the channel.

        Raises:
            ValueError: If the workspace has no channel.
        """
        if self.channel is not None:
            return ChannelEndpoint.model_validate(self.channel).set_client(self.client)
        else:
            raise ValueError("Workspace has no channel")


class TaskEndpoint(EntityEndpoint, Task):
    """Represents a task endpoint.

    This class is used to interact with the task endpoint of the API.
    """

    def get_type(self) -> str:
        """Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "projects".
        """
        return "tasks"


class RetainedGuidanceEndpoint(EntityEndpoint, RetainedGuidance):
    """Represents a retained guidance endpoint.

    This class is used to interact with the retained guidance endpoint of the API.
    """

    def get_type(self) -> str:
        """Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "retainedGuidance".
        """
        return "retainedGuidance"


class ProjectEndpoint(EntityEndpoint, Project):
    """Represents a project endpoint.

    This class is used to interact with the project endpoint of the API.
    """

    def get_type(self) -> str:
        """Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "projects".
        """
        return "projects"

    def update_resources(
            self,
            stores: List["StoreEndpoint"] = None,
            taxonomies: List["TaxonomyEndpoint"] = None,
            data_forms: List["DataFormEndpoint"] = None,
            guidance: List["GuidanceSetEndpoint"] = None,
            dashboards: List["DashboardEndpoint"] = None,
    ):
        """Update the resources of the project.

        Args:
            stores (List["StoreEndpoint"], optional): List of store endpoints to update.
            taxonomies (List["TaxonomyEndpoint"], optional): List of taxonomy endpoints to update.
            data_forms (List["DataFormEndpoint"], optional): List of data form endpoints to update.
            guidance (List["GuidanceSetEndpoint"], optional): List of guidance set endpoints to update.
            dashboards (List["DashboardEndpoint"], optional): List of dashboard endpoints to update.
        """
        project_resources_update = ProjectResourcesUpdate()
        project_resources_update.store_refs = []
        project_resources_update.taxonomy_refs = []
        project_resources_update.dashboard_refs = []
        project_resources_update.data_form_refs = []
        project_resources_update.guidance_set_refs = []

        if stores:
            project_resources_update.store_refs = [store.ref for store in stores]

        if taxonomies:
            project_resources_update.taxonomy_refs = [
                taxonomy.ref for taxonomy in taxonomies
            ]
        if data_forms:
            project_resources_update.data_form_refs = [
                data_form.ref for data_form in data_forms
            ]
        if guidance:
            project_resources_update.guidance_set_refs = [
                guidance.ref for guidance in guidance
            ]
        if dashboards:
            project_resources_update.dashboard_refs = [
                dashboard.ref for dashboard in dashboards
            ]

        self.client.put(
            f"/api/projects/{self.id}/resources",
            body=json.loads(project_resources_update.json(by_alias=True)),
        )

    @property
    def dashboards(self) -> ProjectDashboardsEndpoint:
        """Get the document stores endpoint of the project.

        Returns:
            ProjectDocumentStoresEndpoint: The document stores endpoint of the project.
        """
        return ProjectDashboardsEndpoint().set_client(self.client).set_project(self)

    @property
    def document_stores(self) -> ProjectDocumentStoresEndpoint:
        """Get the document stores endpoint of the project.

        Returns:
            ProjectDocumentStoresEndpoint: The document stores endpoint of the project.
        """
        return ProjectDocumentStoresEndpoint().set_client(self.client).set_project(self)

    @property
    def data_stores(self) -> ProjectDataStoresEndpoint:
        """Get the data stores endpoint of the project.

        Returns:
            ProjectDataStoresEndpoint: The data stores endpoint of the project.
        """
        return ProjectDataStoresEndpoint().set_client(self.client).set_project(self)

    @property
    def model_stores(self) -> ProjectModelStoresEndpoint:
        """Get the model stores endpoint of the project.

        Returns:
            ProjectModelStoresEndpoint: The model stores endpoint of the project.
        """
        return ProjectModelStoresEndpoint().set_client(self.client).set_project(self)

    @property
    def taxonomies(self) -> ProjectTaxonomiesEndpoint:
        """Get the taxonomies endpoint of the project.

        Returns:
            ProjectTaxonomiesEndpoint: The taxonomies endpoint of the project.
        """
        return ProjectTaxonomiesEndpoint().set_client(self.client).set_project(self)

    @property
    def guidance(self) -> "ProjectGuidanceSetsEndpoint":
        """Get the guidance sets endpoint of the project.

        Returns:
            GuidanceSetsEndpoint: The guidance sets endpoint of the project.
        """
        return ProjectGuidanceSetsEndpoint().set_client(self.client).set_project(self)

    @property
    def data_forms(self) -> "ProjectDataFormsEndpoint":
        """Get the guidance sets endpoint of the project.

        Returns:
            GuidanceSetsEndpoint: The guidance sets endpoint of the project.
        """
        return ProjectDataFormsEndpoint().set_client(self.client).set_project(self)

    @property
    def assistants(self) -> ProjectAssistantsEndpoint:
        """Get the assistants endpoint of the project.

        Returns:
            ProjectAssistantsEndpoint: The assistants endpoint of the project.
        """
        return ProjectAssistantsEndpoint().set_client(self.client).set_project(self)

    def get_tags(self) -> List[ProjectTag]:
        """Get the tags of the project.

        Returns:
            List[ProjectTag]: A list of tags associated with the project.
        """
        response = self.client.get(f"/api/projects/{self.id}/tags")
        return [ProjectTag.model_validate(tag) for tag in response.json()]

    def update_tags(self, tags: List[ProjectTag]) -> List[ProjectTag]:
        """Update the tags of the project.

        Args:
            tags (List[ProjectTag]): A list of new tags to associate with the project.

        Returns:
            List[ProjectTag]: A list of updated tags associated with the project.
        """
        response = self.client.put(
            f"/api/projects/{self.id}/tags",
            body=[tag.model_dump(by_alias=True) for tag in tags],
        )
        return [ProjectTag.model_validate(tag) for tag in response.json()]


class MessagesEndpoint(EntitiesEndpoint):
    """Represents a message endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "messages".
        """
        return "messages"

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            MessageEndpoint: The instance class of the endpoint.
        """
        return MessageEndpoint

    def get_page_class(self, object_dict=None):
        """
        Get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            PageMessageEndpoint: The page class of the endpoint.
        """
        return PageMessageEndpoint


class ChannelsEndpoint(EntitiesEndpoint):
    """Represents a channels endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "channels".
        """
        return "channels"

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            ChannelEndpoint: The instance class of the endpoint.
        """
        return ChannelEndpoint

    def get_page_class(self, object_dict=None):
        """
        Get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            PageChannelEndpoint: The page class of the endpoint.
        """
        return PageChannelEndpoint


class WorkspacesEndpoint(EntitiesEndpoint):
    """Represents a workspaces endpoint

    This class is used to represent a workspaces endpoint in the system.

    Attributes:
        object_dict: A dictionary containing the details of the object.
    """

    """Represents a workspaces endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "workspaces"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the details of the object.

        Returns:
            WorkspaceEndpoint: The instance class of the endpoint.
        """
        return WorkspaceEndpoint

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the details of the object.

        Returns:
            PageWorkspaceEndpoint: The page class of the endpoint.
        """
        return PageWorkspaceEndpoint


class AssistantsEndpoint(EntitiesEndpoint):
    """Represents a assistants endpoint

    This class is used to represent the assistants endpoint in the system.

    Attributes:
        object_dict: A dictionary containing the object data.
    """

    """Represents a assistants endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "assistants"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            AssistantEndpoint: The instance class of the endpoint.
        """
        return AssistantEndpoint

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            PageAssistantEndpoint: The page class of the endpoint.
        """
        return PageAssistantEndpoint


class TasksEndpoint(EntitiesEndpoint):
    """Represents a projects endpoint"""

    """Represents a projects endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "tasks"

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the endpoint.

        Returns:
            ProjectEndpoint: The instance class of the endpoint.
        """
        return TaskEndpoint

    def get_page_class(self, object_dict=None):
        """
        Get the page class of the endpoint.

        Returns:
            PageProjectEndpoint: The page class of the endpoint.
        """
        return PageTaskEndpoint


class RetainedGuidancesEndpoint(EntitiesEndpoint):
    """Represents a projects endpoint"""

    """Represents a projects endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "retainedGuidance"

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the endpoint.

        Returns:
            ProjectEndpoint: The instance class of the endpoint.
        """
        return RetainedGuidanceEndpoint

    def get_page_class(self, object_dict=None):
        """
        Get the page class of the endpoint.

        Returns:
            PageProjectEndpoint: The page class of the endpoint.
        """
        return PageRetainedGuidanceEndpoint


class ProjectsEndpoint(EntitiesEndpoint):
    """Represents a projects endpoint"""

    """Represents a projects endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "projects"

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the endpoint.

        Returns:
            ProjectEndpoint: The instance class of the endpoint.
        """
        return ProjectEndpoint

    def get_page_class(self, object_dict=None):
        """
        Get the page class of the endpoint.

        Returns:
            PageProjectEndpoint: The page class of the endpoint.
        """
        return PageProjectEndpoint

    def find_by_name(self, project_name: str, organization: Optional[Organization] = None) -> Optional[ProjectEndpoint]:
        """
        Find a project by name.

        Args:
            project_name (str): The name of the project to find.
            organization (Organization, optional): The organization to search in. Defaults to None.

        Returns:
            Optional[ProjectEndpoint]: The project endpoint if found, None otherwise.
        """

        url = f"/api/{self.get_type()}"
        filters = {"filter": [f"name: '{project_name}'"]}
        if organization is not None:
            filters["filter"].append(f"organization.id: '{organization.id}'")
        get_response = self.client.get(url, params=filters)
        if len(get_response.json()["content"]) > 0:
            return ProjectEndpoint.model_validate(
                get_response.json()["content"][0]
            ).set_client(self.client)
        return None

    def stream_query(self, query: str = "*", sort=None, limit=None):
        """
        Stream the query for the project endpoints.

        Args:
            query (str, optional): The query to run. Defaults to "*".
            sort (str, optional): Sorting order of the query. Defaults to None.
            limit (int, optional): The maximum number of results to return. Defaults to None.

        Yields:
            ProjectEndpoint: A generator of the project endpoints.
        """
        page_size = 5
        page = 1
        counter = 0

        if not sort:
            sort = "id"

        while True:
            page_response = self.query(
                query=query, page=page, page_size=page_size, sort=sort
            )
            if not page_response.content:
                break
            for project_endpoint in page_response.content:
                yield project_endpoint
                counter += 1
                if limit and counter >= limit:
                    break
            page += 1

    def query(
            self, query: str = "*", page: int = 1, page_size: int = 100, sort=None
    ) -> Optional[PageProjectEndpoint]:
        """
        Query the project endpoints.

        Args:
            query (str, optional): The query to run. Defaults to "*".
            page (int, optional): The page number to query. Defaults to 1.
            page_size (int, optional): The number of results per page. Defaults to 100.
            sort (str, optional): Sorting order of the query. Defaults to None.

        Returns:
            Optional[PageProjectEndpoint]: The page project endpoint if found, None otherwise.
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "query": requests.utils.quote(query),
            "filter": [],
        }

        if sort is not None:
            params["sort"] = sort

        if self.organization is not None:
            params["filter"].append(f"organization.id: '{self.organization.id}'")

        get_response = self.client.get(f"/api/{self.get_type()}", params=params)

        return PageProjectEndpoint.model_validate(get_response.json()).set_client(
            self.client
        )

    def create(self, project: Project, template_ref: str = None) -> Project:
        """
        Create a project.

        Args:
            project (Project): The project to create.
            template_ref (str, optional): The template reference. Defaults to None.

        Returns:
            Project: The created project.
        """
        url = f"/api/{self.get_type()}"

        if self.organization is not None and project.organization is None:
            project.organization = self.organization.detach()
        else:
            if project.organization is None:
                raise Exception("Organization not set on the project")

        if template_ref is not None:
            params = {"templateRef": template_ref}
        else:
            params = None

        create_response = self.client.post(
            url, body=json.loads(project.model_dump_json(by_alias=True)), params=params
        )
        return ProjectEndpoint.model_validate(create_response.json()).set_client(
            self.client
        )


class StoresEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """Represents a stores endpoint

    This class is used to represent a stores endpoint. It inherits from ComponentEndpoint,
    ClientEndpoint, and OrganizationOwned classes.

    Attributes:
        None
    """

    """Represents a stores endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case, "stores".
        """
        return "stores"

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            PageStoreEndpoint: The page class of the endpoint.
        """
        return PageStoreEndpoint

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint based on the 'storeType'
        key in the object_dict.

        Args:
            object_dict (dict, optional): A dictionary object that contains the 'storeType' key.
            Defaults to None.

        Returns:
            DocumentStoreEndpoint/ModelStoreEndpoint/DataStoreEndpoint: The instance class of the endpoint.

        Raises:
            ValueError: If the 'storeType' key in the object_dict is not "DOCUMENT", "MODEL", or "TABLE".
        """
        if object_dict["storeType"] == "DOCUMENT":
            return DocumentStoreEndpoint
        elif object_dict["storeType"] == "MODEL":
            return ModelStoreEndpoint
        elif object_dict["storeType"] == "TABLE":
            return DataStoreEndpoint
        else:
            raise ValueError(f"Unknown store type {object_dict['storeType']}")


class GuidanceSetsEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """
    Represents a guidance set endpoint.

    This class is used to interact with the guidance endpoint of the API.
    It provides methods to get the type, page class, and instance class of the endpoint,
    as well as to deploy an extension pack from a URL.
    """

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, "guidance".
        """
        return "guidance"

    def get_page_class(self, object_dict=None):
        """
        Get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary of objects.

        Returns:
            PageGuidanceSetEndpoint: The page class of the endpoint.
        """
        return PageGuidanceSetEndpoint

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary of objects.

        Returns:
            GuidanceSetEndpoint: The instance class of the endpoint.
        """
        return GuidanceSetEndpoint


class PromptsEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """
    Represents a prompts endpoint.

    This class is used to interact with the prompts endpoint of the API.
    It provides methods to get the type, page class, and instance class of the endpoint,
    as well as to deploy an extension pack from a URL.
    """

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, "prompts".
        """
        return "prompts"

    def get_page_class(self, object_dict=None):
        """
        Get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary of objects.

        Returns:
            PagePromptEndpoint: The page class of the endpoint.
        """
        return PagePromptEndpoint

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary of objects.

        Returns:
            PromptEndpoint: The instance class of the endpoint.
        """
        return PromptEndpoint


class ExtensionPacksEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """
    Represents an extension packs endpoint.

    This class is used to interact with the extension packs endpoint of the API.
    It provides methods to get the type, page class, and instance class of the endpoint,
    as well as to deploy an extension pack from a URL.
    """

    """Represents an extension packs endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, "extensionPacks".
        """
        return "extensionPacks"

    def get_page_class(self, object_dict=None):
        """
        Get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary of objects.

        Returns:
            PageExtensionPackEndpoint: The page class of the endpoint.
        """
        return PageExtensionPackEndpoint

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary of objects.

        Returns:
            ExtensionPackEndpoint: The instance class of the endpoint.
        """
        return ExtensionPackEndpoint

    def deploy_from_url(
            self, extension_pack_url: str, deployment_options: DeploymentOptions
    ) -> "ExtensionPackEndpoint":
        """
        Deploy an extension pack from a url.

        Args:
            extension_pack_url (str): The URL of the extension pack to deploy.
            deployment_options (DeploymentOptions): The deployment options for the extension pack.

        Returns:
            ExtensionPackEndpoint: The deployed extension pack endpoint.
        """
        url = f"/api/extensionPacks/{self.organization.slug}"
        create_response = self.client.post(
            url,
            body=json.loads(deployment_options.json(by_alias=True)),
            params={"uri": extension_pack_url},
        )
        return ExtensionPackEndpoint.model_validate(create_response.json()).set_client(
            self.client
        )


class ProjectTemplatesEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """Represents a project templates endpoint

    This class is used to represent a project templates endpoint. It inherits from
    ComponentEndpoint, ClientEndpoint, and OrganizationOwned classes.

    Attributes:
        None
    """

    """Represents a project templates endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint, which is "projectTemplates".
        """
        return "projectTemplates"

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary parameter. Defaults to None.

        Returns:
            PageProjectTemplateEndpoint: The page class of the endpoint.
        """
        return PageProjectTemplateEndpoint

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary parameter. Defaults to None.

        Returns:
            ProjectTemplateEndpoint: The instance class of the endpoint.
        """
        return ProjectTemplateEndpoint


class CredentialDefinitionsEndpoint(
    ComponentEndpoint, ClientEndpoint, OrganizationOwned
):
    """Represents a credentials endpoint.

    This class is used to represent a credentials endpoint. It inherits from
    ComponentEndpoint, ClientEndpoint, and OrganizationOwned classes.

    Attributes:
        None
    """

    """Represents a credentials endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "credentialDefinitions"

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint.

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            PageCredentialDefinitionEndpoint: The page class of the endpoint.
        """
        return PageCredentialDefinitionEndpoint

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint.

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            CredentialDefinitionEndpoint: The instance class of the endpoint.
        """
        return CredentialDefinitionEndpoint


class DataFormsEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """
    A class used to represent the DataFormsEndpoint.

    This class inherits from the ComponentEndpoint, ClientEndpoint, and OrganizationOwned classes.
    """

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "dataForms".
        """
        return "dataForms"

    def get_page_class(self, object_dict=None):
        """
        Get the page class for the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            PageDataFormEndpoint: The page class for the endpoint.
        """
        return PageDataFormEndpoint

    def get_instance_class(self, object_dict=None):
        """
        Get the instance class for the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            DataFormEndpoint: The instance class for the endpoint.
        """
        return DataFormEndpoint


class DashboardsEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """
    A class used to represent DashboardsEndpoint which inherits from ComponentEndpoint, ClientEndpoint, and OrganizationOwned.
    """

    def get_type(self) -> str:
        """
        Method to get the type of the dashboard.

        Returns:
            str: The string "dashboards".
        """
        return "dashboards"

    def get_page_class(self, object_dict=None):
        """
        Method to get the page class of the dashboard.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            PageDashboardEndpoint: The class 'PageDashboardEndpoint'.
        """
        return PageDashboardEndpoint

    def get_instance_class(self, object_dict=None):
        """
        Method to get the instance class of the dashboard.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            DashboardEndpoint: The class 'DashboardEndpoint'.
        """
        return DashboardEndpoint


class AssistantDefinitionsEndpoint(
    ComponentEndpoint, ClientEndpoint, OrganizationOwned
):
    """Represents a model runtimes endpoint

    This class is used to represent a model runtimes endpoint. It inherits from
    ComponentEndpoint, ClientEndpoint, and OrganizationOwned classes.

    Attributes:
        None
    """

    """Represents a model runtimes endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint, which is "assistantDefinitions".
        """
        return "assistantDefinitions"

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary parameter. Defaults to None.

        Returns:
            PageAssistantDefinitionEndpoint: The page class of the endpoint.
        """
        return PageAssistantDefinitionEndpoint

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary parameter. Defaults to None.

        Returns:
            AssistantDefinitionEndpoint: The instance class of the endpoint.
        """
        return AssistantDefinitionEndpoint


class PipelinesEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """Represents a model runtimes endpoint

    This class is used to represent a model runtimes endpoint. It inherits from
    ComponentEndpoint, ClientEndpoint, and OrganizationOwned classes.

    Attributes:
        None
    """

    """Represents a model runtimes endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "pipelines".
        """
        return "pipelines"

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary parameter. Defaults to None.

        Returns:
            PagePipelineEndpoint: The page class of the endpoint.
        """
        return PagePipelineEndpoint

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary parameter. Defaults to None.

        Returns:
            PipelineEndpoint: The instance class of the endpoint.
        """
        return PipelineEndpoint


class ActionsEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """Represents a model runtimes endpoint.

    This class is used to represent a model runtimes endpoint. It inherits from
    ComponentEndpoint, ClientEndpoint, and OrganizationOwned classes.

    """

    """Represents a model runtimes endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint, which is "actions".
        """
        return "actions"

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint.

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): The dictionary object. Defaults to None.

        Returns:
            PageActionEndpoint: The page class of the endpoint.
        """
        return PageActionEndpoint

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint.

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): The dictionary object. Defaults to None.

        Returns:
            ActionEndpoint: The instance class of the endpoint.
        """
        return ActionEndpoint


class ModelRuntimesEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """Represents a model runtimes endpoint.

    This class is used to represent a model runtimes endpoint which is a
    component endpoint, a client endpoint and owned by an organization.

    Attributes:
        None
    """

    """Represents a model runtimes endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint which is "modelRuntimes".
        """
        return "modelRuntimes"

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint.

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            PageModelRuntimeEndpoint: The page class of the endpoint.
        """
        return PageModelRuntimeEndpoint

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint.

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            ModelRuntimeEndpoint: The instance class of the endpoint.
        """
        return ModelRuntimeEndpoint


class ProjectTemplateEndpoint(ComponentInstanceEndpoint, ProjectTemplate):
    """Represents a project template endpoint.

    This class is used to represent a project template endpoint. It inherits from
    ComponentInstanceEndpoint and ProjectTemplate.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a project template endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. It returns a string
        that represents the type of the endpoint.

        Returns:
            str: The type of the endpoint, "projectTemplates".
        """
        return "projectTemplates"


class PipelineEndpoint(ComponentInstanceEndpoint, Pipeline):
    """
    Represents a pipeline endpoint.

    This class is used to represent a pipeline endpoint. It inherits from both
    ComponentInstanceEndpoint and Pipeline classes.
    """

    """Represents a pipeline endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case, it will always
        return the string "pipelines".

        Returns:
            str: The type of the endpoint, in this case "pipelines".
        """
        return "pipelines"


class AssistantDefinitionEndpoint(ComponentInstanceEndpoint, AssistantDefinition):
    """Represents an assistant definition endpoint.

    This class is used to represent an endpoint for an assistant definition. It inherits from
    both ComponentInstanceEndpoint and AssistantDefinition classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a assistant definition endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case, it will always return
        the string "assistants".

        Returns:
            str: The type of the endpoint, "assistants".
        """
        return "assistants"


class ActionEndpoint(ComponentInstanceEndpoint, Action):
    """Represents a pipeline endpoint

    This class is used to represent a pipeline endpoint in the system. It inherits from
    both ComponentInstanceEndpoint and Action classes.

    Attributes:
        None
    """

    """Represents a pipeline endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint. In this case, it will always
        return the string "actions".

        Returns:
            str: The type of the endpoint, always "actions" in this case.
        """
        return "actions"


class CredentialDefinitionEndpoint(ComponentInstanceEndpoint, CredentialDefinition):
    """Represents a credential endpoint.

    This class is a combination of ComponentInstanceEndpoint and CredentialDefinition.
    It is used to represent a credential endpoint.

    Attributes:
        None
    """

    """Represents a credential endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method returns the type of the endpoint which is "credentialDefinitions".

        Returns:
            str: The type of the endpoint.
        """
        return "credentialDefinitions"


class DataFormEndpoint(ComponentInstanceEndpoint, DataForm):
    """A class used to represent the endpoint of a data form component instance.

    This class inherits from the ComponentInstanceEndpoint and DataForm classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the component instance.
    """

    def get_type(self) -> str:
        """Gets the type of the component instance.

        This method returns the type of the component instance as a string.

        Returns:
            str: The type of the component instance.
        """
        return "dataForms"


class DashboardEndpoint(ComponentInstanceEndpoint, Dashboard):
    """A class that represents the dashboard endpoint.

    This class inherits from the ComponentInstanceEndpoint and Dashboard classes.

    Attributes:
        None
    """

    def get_type(self) -> str:
        """Gets the type of the dashboard.

        This method returns the type of the dashboard as a string.

        Returns:
            str: The type of the dashboard.
        """
        return "dashboards"


class ModelRuntimeEndpoint(ComponentInstanceEndpoint, ModelRuntime):
    """
    Represents a model runtime endpoint.

    This class is used to represent a model runtime endpoint. It inherits from
    ComponentInstanceEndpoint and ModelRuntime classes.
    """

    """Represents a model runtime endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        This method is used to get the type of the endpoint. It returns a string
        that represents the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "modelRuntimes".
        """
        return "modelRuntimes"


class ExtensionPackEndpoint(ComponentInstanceEndpoint, ExtensionPack):
    """Represents an extension pack endpoint.

    This class is used to represent an extension pack endpoint. It inherits from
    both ComponentInstanceEndpoint and ExtensionPack classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents an extension pack endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. It returns a string
        that represents the type of the endpoint.

        Args:
            None

        Returns:
            str: The type of the endpoint, which is "extensionPacks".
        """
        return "extensionPacks"

    def undeploy(self):
        """
        Undeploy the extension pack.

        Returns:
            None
        """
        response = self.client.put(f"/api/extensionPacks/{self.ref}/_undeploy")
        process_response(response)

    def deploy(self):
        """
        Deploy the extension pack.

        :return: None
        """
        response = self.client.put(f"/api/extensionPacks/{self.ref}/_deploy")
        process_response(response)

    def repack(self):
        """
        Repack the extension pack.

        :return: None
        """
        response = self.client.put(f"/api/extensionPacks/{self.ref}/_repack")
        process_response(response)


class TaxonomyEndpoint(ComponentInstanceEndpoint, Taxonomy):
    """Represents a taxonomy endpoint"""

    """Represents a taxonomy endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, "taxonomies".
        """
        return "taxonomies"

    def get_group_taxons(self) -> List[Taxon]:
        """
        Get the group taxons of the taxonomy.

        Returns:
            List[Taxon]: A list of group taxons.
        """

        def find_groups(taxons) -> List[Taxon]:
            """
            Finds and returns the group taxons from the given list of taxons.

            Args:
                taxons (List[Taxon]): A list of taxon objects.

            Returns:
                List[Taxon]: A list of group taxons.

            Raises:
                None

            Note:
                This function uses recursion to find group taxons in child taxons.
            """
            group_taxons = []
            for taxon in taxons:
                if taxon.is_group:
                    group_taxons.append(taxon)
                if taxon.children:
                    group_taxons.extend(find_groups(taxon.children))
            return group_taxons

        return find_groups(self.taxons)

    def find_taxon(self, taxons, parts, use_label=False):
        """
        Finds a taxon in a list of taxons that matches a given path.

        Args:
            taxons (list): A list of taxon objects to search through.
            path (str): The path of the taxon to find.

        Returns:
            Taxon: The taxon object if found, None otherwise.
        """
        for taxon in taxons:
            match_value = taxon.label if use_label else taxon.name
            if parts[0] == match_value:
                if len(parts) == 1:
                    return taxon
                return self.find_taxon(taxon.children, parts[1:], use_label)

    def find_taxon_by_label_path(self, label_path: str) -> Taxon:
        """
        Find a taxon in the taxonomy by its label path.

        Args:
            label_path (str): The label path of the taxon.

        Returns:
            Taxon: The matched taxon.
        """
        label_path_parts = label_path.split("/")

        return self.find_taxon(self.taxons, label_path_parts, use_label=True)

    def find_taxon_by_path(self, path: str) -> Taxon:
        """
        Find a taxon in the taxonomy by its path.

        Args:
            path (str): The path of the taxon.

        Returns:
            Taxon: The matched taxon.
        """
        path_parts = path.split("/")
        return self.find_taxon(self.taxons, path_parts)

    def to_xsd(self) -> str:
        """
        Convert the taxonomy to an XSD.

        Returns:
            str: The XSD representation of the taxonomy.
        """
        return self.client.get(
            f'/api/taxonomies/{self.ref.replace(":", "/")}/export',
            params={"format": "xsd"},
        ).text

    def to_json_schema(self) -> dict:
        """
        Convert the taxonomy to an XSD.

        Returns:
            str: The XSD representation of the taxonomy.
        """
        return self.client.get(
            f'/api/taxonomies/{self.ref.replace(":", "/")}/export',
            params={"format": "json-schema"},
        ).json()

    def get_taxon_by_path(self, path) -> Optional[Taxon]:
        """
        Get a taxon by its path.

        Args:
            path (str): The path of the taxon.

        Returns:
            Taxon: The taxon object if found, None otherwise.
        """

        def find_taxon(taxons, path):
            """
            Finds a taxon in a list of taxons that matches a given path.

            This function iterates over a list of taxons, checking if each taxon's path matches the given path.
            If a match is found, the taxon is returned. If no match is found in the top level of the list,
            the function recursively searches through the children of each taxon. If no taxon is found after
            searching through all taxons and their children, the function returns None.

            Args:
                taxons (list): A list of taxon objects to search through.
                path (str): The path of the taxon to find.

            Returns:
                Taxon object if found, None otherwise.
            """
            for taxon in taxons:
                if taxon.path == path:
                    return taxon
                if taxon.children:
                    found_taxon = find_taxon(taxon.children, path)
                    if found_taxon:
                        return found_taxon
            return None

        return find_taxon(self.taxons, path)


class MembershipEndpoint(Membership, EntityEndpoint):
    """Represents a membership endpoint.

    This class is used to represent a membership endpoint which is a combination of
    Membership and EntityEndpoint classes.

    Attributes:
        None

    Methods:
        get_type: Returns the type of the endpoint.
    """

    """Represents a membership endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        This method is used to get the type of the endpoint. In this case, it will always
        return "memberships".

        Returns:
            str: The type of the endpoint, "memberships".
        """
        return "memberships"


class ExecutionEndpoint(Execution, EntityEndpoint):
    """Represents a execution endpoint"""

    """Represents a execution endpoint"""

    def get_type(self) -> str:
        """
        Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, "executions".
        """
        return "executions"

    def cancel(self):
        """
        Cancel the execution.

        Sends a PUT request to the server to cancel the execution.
        """
        self.client.put(f"/api/executions/{self.id}/cancel")

    def logs(self):
        """
        Get the logs of the execution.

        Sends a GET request to the server to retrieve the logs.

        Returns:
            Response: The response from the server containing the logs.
        """
        return self.client.get(f"/api/executions/{self.id}/logs")

    def wait_for(
            self,
            status: str = "SUCCEEDED",
            fail_on_statuses=None,
            timeout: int = 300,
            follow_child_executions: bool = True,
    ) -> List["ExecutionEndpoint"]:
        """
        Wait for a specific status.

        Args:
            status (str, optional): The status to wait for. Defaults to 'SUCCEEDED'.
            fail_on_statuses (list, optional): The statuses that should cause the function to fail. Defaults to ['FAILED'].
            timeout (int, optional): The maximum time to wait in seconds. Defaults to 300.
            follow_child_executions (bool, optional): Whether to follow child executions. Defaults to True.

        Raises:
            Exception: If the execution fails with a status in fail_on_statuses.
            Exception: If the function times out.

        Returns:
            List[ExecutionEndpoint]: A list of executions that have reached the desired status.
        """
        if fail_on_statuses is None:
            fail_on_statuses = ["FAILED"]

        logger.info("Waiting for status %s", status)
        start = time.time()
        execution = self
        while time.time() - start < timeout:
            execution = execution.reload()
            if execution.status == status:
                if follow_child_executions:
                    all_executions = [execution]
                    for child_execution in [
                        ExecutionEndpoint.model_validate(
                            child_execution.dict()
                        ).set_client(self.client)
                        for child_execution in execution.child_executions
                    ]:
                        all_executions.extend(
                            child_execution.wait_for(
                                status,
                                fail_on_statuses,
                                timeout,
                                follow_child_executions,
                            )
                        )
                    return all_executions
                else:
                    return [execution]

            if execution.status in fail_on_statuses:
                raise Exception(
                    f"Execution {execution.id} failed with status {execution.status}"
                )

            time.sleep(5)

        raise Exception(f"Timed out waiting on execution {self.id}")


class UserEndpoint(User, EntityEndpoint):
    """Represents a user endpoint.

    This class is used to interact with the user endpoints of the API.
    It inherits from the User and EntityEndpoint classes.
    """

    """Represents a user endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "users".
        """
        return "users"

    def activate(self) -> "UserEndpoint":
        """Activate the user.

        This method sends a PUT request to the API to activate the user.

        Returns:
            UserEndpoint: The activated user endpoint.
        """
        url = f"/api/users/{self.id}/activate"
        response = self.client.put(url)
        return UserEndpoint.model_validate(response.json()).set_client(self.client)

    def deactivate(self) -> "UserEndpoint":
        """Deactivate the user.

        This method sends a PUT request to the API to deactivate the user.

        Returns:
            UserEndpoint: The deactivated user endpoint.
        """
        url = f"/api/users/{self.id}/activate"
        response = self.client.put(url)
        return UserEndpoint.model_validate(response.json()).set_client(self.client)

    def set_password(self, password: str, reset_token) -> "UserEndpoint":
        """Set the password of the user.

        This method sends a PUT request to the API to set the password of the user.

        Args:
            password (str): The new password.
            reset_token: The reset token.

        Returns:
            UserEndpoint: The user endpoint with the updated password.
        """
        url = f"/api/users/{self.id}/password"
        response = self.client.put(
            url, body={"password": password, "resetToken": reset_token}
        )
        return UserEndpoint.model_validate(response.json()).set_client(self.client)

    def get_memberships(self) -> List[MembershipEndpoint]:
        """Get the memberships of the user.

        This method sends a GET request to the API to retrieve the memberships of the user.

        Returns:
            List[MembershipEndpoint]: A list of the user's memberships.
        """
        url = f"/api/users/{self.id}/memberships"
        response = self.client.get(url)
        return [
            MembershipEndpoint.model_validate(membership)
            for membership in response.json()
        ]


class ExecutionsEndpoint(EntitiesEndpoint):
    """Represents a executions endpoint

    This class is used to represent an executions endpoint in the system.

    Attributes:
        None
    """

    """Represents a executions endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "executions"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            ExecutionEndpoint: The instance class of the endpoint.
        """
        return ExecutionEndpoint

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            PageExecutionEndpoint: The page class of the endpoint.
        """
        return PageExecutionEndpoint


class MembershipsEndpoint(EntitiesEndpoint):
    """Represents a memberships endpoint

    This class is used to represent a memberships endpoint in the system.

    Attributes:
        None
    """

    """Represents a memberships endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "memberships"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            MembershipEndpoint: The instance class of the endpoint.
        """
        return MembershipEndpoint

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            PageMembershipEndpoint: The page class of the endpoint.
        """
        return PageMembershipEndpoint


class UsersEndpoint(EntitiesEndpoint):
    """Represents a users endpoint

    This class is used to represent a users endpoint in the system.

    Attributes:
        None
    """

    """Represents a users endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "users"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            UserEndpoint: The instance class of the endpoint.
        """
        return UserEndpoint

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): The object dictionary. Defaults to None.

        Returns:
            PageUserEndpoint: The page class of the endpoint.
        """
        return PageUserEndpoint


class DataAttributeEndpoint(DataAttribute, ClientEndpoint):
    """
    Represents a data attribute endpoint.

    Attributes:
        data_object (DataObject): The data object of the data attribute.
    """

    """Represents a data attribute endpoint"""
    data_object: DataObject = None

    def set_data_object(self, data_object: DataObject):
        """
        Set the data object of the data attribute.

        Args:
            data_object (DataObject): The data object to be set.
        """
        self.data_object = data_object


class DataObjectEndpoint(DataObject, ClientEndpoint):
    """Represents a data object endpoint.

    This class is a combination of DataObject and ClientEndpoint. It provides
    methods to update, delete and retrieve attributes of a data object.

    Attributes:
        store_ref (str): Reference to the store.
        id (str): Unique identifier of the data object.
        client (Client): Client to interact with the API.
    """

    """Represents a data object endpoint"""

    def update(self):
        """Update the data object.

        This method updates the data object by making a PUT request to the API.

        Returns:
            None
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/dataObjects/{self.id}"
        self.client.put(url, body=self.model_dump(mode="json", by_alias=True))

    def delete(self):
        """Delete the data object.

        This method deletes the data object by making a DELETE request to the API.

        Returns:
            None
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/dataObjects/{self.id}"
        self.client.delete(url)

    @property
    def attributes(self) -> List[DataAttributeEndpoint]:
        """Get the attributes of the data object.

        This method retrieves the attributes of the data object by making a GET request to the API.

        Returns:
            List[DataAttributeEndpoint]: List of data attribute endpoints.
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/dataObjects/{self.id}/attributes"
        response = self.client.get(url)
        return [
            DataAttributeEndpoint.model_validate(attribute)
            for attribute in response.json()
        ]


class DocumentFamilyEndpoint(DocumentFamily, ClientEndpoint):
    """Represents a document family endpoint"""

    """Represents a document family endpoint"""

    def update(self):
        """
        Update the document family.
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}"
        response = self.client.put(url, body=self.model_dump(mode="json", by_alias=True))
        self.change_sequence = response.json()["changeSequence"]

    def set_active_assistant(self, assistant: Assistant):
        """
        Set the active assistant.
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/activeAssistant"
        response = self.client.put(url, body=assistant.model_dump(mode="json", by_alias=True))
        process_response(response)
        self.change_sequence = response.json()["changeSequence"]

    def clear_active_assistant(self):
        """
        Clear the active assistant.
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/activeAssistant"
        response = self.client.delete(url)
        process_response(response)
        self.change_sequence = response.json()["changeSequence"]

    def lock(self):
        """
        Lock the document family.
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/lock"
        response = self.client.put(url)
        process_response(response)
        self.change_sequence = response.json()["changeSequence"]

    def unlock(self):
        """
        Lock the document family.
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/unlock"
        response = self.client.put(url)
        process_response(response)
        self.change_sequence = response.json()["changeSequence"]

    def touch(self):
        """
        Update the document family.
        """
        url = f"/api/documentFamilies/{self.id}/touch"
        response = self.client.get(url)
        process_response(response)

    def get_external_data(self) -> dict:
        """
        Get the external data of the document family.

        Returns:
            DocumentExternalData: The external data of the document family.
        """
        url = f"/api/documentFamilies/{self.id}/externalData"
        response = self.client.get(url)
        return response.json()

    def set_external_data(self, external_data: dict) -> dict:
        """
        Set the external data of the document family.

        Args:
            external_data (dict): The external data to set for the document family.

        Returns:
            dict: The updated external data of the document family.
        """
        url = f"/api/documentFamilies/{self.id}/externalData"
        response = self.client.put(url, body=external_data)
        return response.json()

    def export(self) -> bytes:
        """
        Export the document family as bytes.

        Returns:
            bytes: The exported document family.
        """
        url = (
            f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/export"
        )
        get_response = self.client.get(url)
        process_response(get_response)
        return get_response.content

    def update_document(
            self, document: Document, content_object: Optional[ContentObject] = None
    ):
        """
        Update a document in the document family.

        Args:
            document (Document): The document to update.
            content_object (Optional[ContentObject]): The content object. Defaults to None.
        """
        if content_object is None:
            content_object = self.content_objects[-1]
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/objects/{content_object.id}/content"
        self.client.post(url, files={"document": document.to_kddb()})

    def wait_for(
            self,
            mixin: Optional[str] = None,
            label: Optional[str] = None,
            timeout: int = 60,
    ) -> "DocumentFamilyEndpoint":
        """
        Wait for the document family to be ready.

        Args:
            mixin (Optional[str]): The mixin. Defaults to None.
            label (Optional[str]): The label. Defaults to None.
            timeout (int): The timeout. Defaults to 60.

        Returns:
            DocumentFamilyEndpoint: The updated document family endpoint.
        """
        logger.info(
            "Waiting for mixin and/or label to be available on document family %s",
            self.id,
        )
        start = time.time()
        while time.time() - start < timeout:
            url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}"
            updated_document_family = DocumentFamilyEndpoint.model_validate(
                self.client.get(url).json()
            ).set_client(self.client)
            if mixin and mixin in updated_document_family.mixins:
                return updated_document_family
            if label and any(
                    doc_label.name == label for doc_label in updated_document_family.labels
            ):
                return updated_document_family

            time.sleep(5)

        raise Exception(f"Not available on document family {self.id}")

    def delete(self):
        """
        Delete the document family.
        """
        logger.info("Deleting document family %s", self.id)
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}"
        if self.client.exists(url):
            self.client.delete(url)
        else:
            raise Exception(f"Document family {self.id} does not exist")

    def get_native(self) -> bytes:
        """
        Get the native content object of the document family.

        Returns:
            bytes: The native content object.

        Raises:
            Exception: If no native content object is found.
        """
        hits = list(
            filter(
                lambda content_object: content_object.content_type == "NATIVE",
                self.content_objects,
            )
        )
        if len(hits) == 0:
            raise Exception(
                f"No native content object found on document family {self.id}"
            )

        get_response = self.client.get(
            f"api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/objects/{hits[0].id}/content"
        )

        return get_response.content

    def add_label(self, label: str):
        """
        Add a label to the document family.

        Args:
            label (str): The label to add.
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/addLabel"
        return self.client.put(url, params={"label": label})

    def remove_label(self, label: str):
        """
        Remove a label from the document family.

        Args:
            label (str): The label to remove.
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/removeLabel"
        return self.client.put(url, params={"label": label})

    def get_document(self, content_object: Optional[ContentObject] = None, inmemory=False) -> Document:
        """
        Get the document of the document family.

        Args:
            content_object (Optional[ContentObject]): The content object. Defaults to None.
            inmemory (bool): Whether to return the document in memory. Defaults to False.

        Returns:
            Document: The document of the document family.
        """
        if content_object is None:
            content_object = self.content_objects[-1]
        get_response = self.client.get(
            f"api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/objects/{content_object.id}/content"
        )
        return Document.from_kddb(get_response.content, inmemory=inmemory)

    def reprocess(self, assistant: Assistant):
        """
        Reprocess the document family.

        Args:
            assistant (Assistant): The assistant to use for reprocessing.
        """
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/reprocess"
        self.client.put(url, params={"assistantId": assistant.id})

    def set_document_status(self, document_status: DocumentStatus):
        """
        Set the document status of the document family.

        Args:
            document_status (DocumentStatus): The document status to set.
        """
        url = (
            f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/status"
        )
        self.client.put(url, body=document_status.model_dump(by_alias=True))

    def add_document(
            self, document: Document, content_object: Optional[ContentObject] = None
    ):
        """
        Add a document to the document family.

        Args:
            document (Document): The document to add.
            content_object (Optional[ContentObject]): The content object. Defaults to None.
        """
        url = (
            f'/api/stores/{self.store_ref.replace(":", "/")}/families/{self.id}/objects'
        )
        if content_object is None:
            content_object = self.content_objects[-1]
        self.client.post(
            url,
            params={
                "sourceContentObjectId": content_object.id,
                "transitionType": "DERIVED",
                "documentVersion": document.version,
            },
            files={"file": document.to_kddb()},
        )

    def export_as_zip(self) -> bytes:
        """
        Export the document family as bytes.

        Returns:
            bytes: The exported document family.
        """
        url = (
            f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/export"
        )
        get_response = self.client.get(url)
        return get_response.content

    def replace_tags(
            self,
            document: Document,
            content_object: Optional[ContentObject] = None,
            owner_uri: Optional[str] = None,
            replace_data: bool = False,
    ):
        """
        Replace the tags of the document family.

        Args:
            document (Document): The document.
            content_object (Optional[ContentObject]): The content object. Defaults to None.
            owner_uri (Optional[str]): The owner URI. Defaults to None.
            replace_data (bool): Whether to replace the data. Defaults to False.
        """
        if content_object is None:
            content_object = self.content_objects[-1]
        url = f"/api/stores/{self.store_ref.replace(':', '/')}/families/{self.id}/objects/{content_object.id}/_replaceTags"
        self.client.put(
            url, params={'replaceData': replace_data, 'ownerUri': owner_uri},
            body=document.get_feature_set(owner_uri).model_dump(by_alias=True),
        )


class StoreEndpoint(ComponentInstanceEndpoint, Store):
    """Represents a store endpoint.

    This class is used to manage the endpoints of a store. It includes methods to get and update metadata,
    upload contents, and post deployment actions.

    Attributes:
        metadata: The metadata of the store.
    """

    """Represents a store endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "stores".
        """
        return "stores"

    def get_metadata_class(self):
        """Get the metadata class.

        This method should be overridden in a subclass.

        Returns:
            None
        """
        return None

    def set_metadata(self, metadata):
        """Set the metadata.

        This method should be overridden in a subclass.

        Args:
            metadata: The metadata to set.
        """
        pass

    def upload_contents(self, metadata) -> List[str]:
        """Upload contents.

        This method should be overridden in a subclass.

        Args:
            metadata: The metadata of the contents to upload.

        Returns:
            list[str]: An empty list.
        """
        return []

    def update_metadata(self):
        """Update the metadata of the store.

        This method sends a PUT request to the store's metadata API endpoint with the store's metadata.
        """
        self.client.put(
            f"/api/stores/{self.ref.replace(':', '/')}/metadata",
            body=json.loads(self.metadata.json(by_alias=True)),
        )

    def get_metadata(self):
        """Get the metadata of the store.

        This method sends a GET request to the store's metadata API endpoint and validates the response.

        Returns:
            The validated metadata if the metadata class is defined, otherwise None.
        """
        metadata_response = self.client.get(
            f"/api/stores/{self.ref.replace(':', '/')}/metadata"
        )
        return (
            self.get_metadata_class().model_validate(metadata_response.json())
            if self.get_metadata_class()
            else None
        )

    def post_deploy(self) -> List[str]:
        """Post deploy the store.

        If the metadata is defined, this method updates the metadata and uploads the contents.

        Returns:
            list[str]: The result of uploading the contents if the metadata is defined, otherwise an empty list.
        """
        if self.metadata:
            # We need to determine in the subclass if we wil be uploading the
            # contents
            self.update_metadata()
            return self.upload_contents(self.metadata)
        return []


class DataExceptionEndpoint(DataException, EntityEndpoint):
    """Handles the endpoint for data exceptions.

    This class is a combination of DataException and EntityEndpoint. It is used
    to manage the endpoint for data exceptions.

    Methods:
        get_type: Returns the type of the endpoint.
    """

    def get_type(self) -> str:
        """Gets the type of the endpoint.

        This method returns the type of the endpoint which is "exceptions".

        Returns:
            str: The type of the endpoint.
        """
        return "exceptions"


class DataStoreExceptionsEndpoint(EntitiesEndpoint):
    """
    A class used to represent the DataStoreExceptionsEndpoint.

    ...

    Attributes
    ----------
    data_store : DataStoreEndpoint
        an instance of the DataStoreEndpoint class

    Methods
    -------
    get_instance_class(object_dict=None):
        Returns the DataExceptionEndpoint class.
    get_page_class(object_dict=None):
        Returns the PageDataExceptionEndpoint class.
    get_type() -> str:
        Returns the string "exceptions".
    __init__(data_store: "DataStoreEndpoint", client: "KodexaClient"):
        Initializes the DataStoreExceptionsEndpoint.
    list(query="*", page=1, page_size=10, sort=None, filters: List[str] = None):
        Lists the data exceptions.
    """

    def get_instance_class(self, object_dict=None):
        """
        Returns the DataExceptionEndpoint class.

        Parameters
        ----------
        object_dict : dict, optional
            a dictionary object (default is None)

        Returns
        -------
        class
            The DataExceptionEndpoint class.
        """
        return DataExceptionEndpoint

    def get_page_class(self, object_dict=None):
        """
        Returns the PageDataExceptionEndpoint class.

        Parameters
        ----------
        object_dict : dict, optional
            a dictionary object (default is None)

        Returns
        -------
        class
            The PageDataExceptionEndpoint class.
        """
        return PageDataExceptionEndpoint

    def get_type(self) -> str:
        """
        Returns the string "exceptions".

        Returns
        -------
        str
            The string "exceptions".
        """
        return "exceptions"

    def __init__(self, data_store: "DataStoreEndpoint", client: "KodexaClient"):
        self.data_store = data_store
        super().__init__(client)

    def list(
            self, query="*", page=1, page_size=10, sort=None, filters: List[str] = None
    ):
        """
        Lists the data exceptions.

        Parameters
        ----------
        query : str, optional
            a query string (default is "*")
        page : int, optional
            a page number (default is 1)
        page_size : int, optional
            a page size (default is 10)
        sort : str, optional
            a sort string (default is None)
        filters : list of str, optional
            a list of filter strings (default is None)

        Returns
        -------
        page
            a page of data exceptions
        """

        if filters is None:
            filters = []

        filters.append(f"dataObject.store.slug={self.data_store.slug}")

        page = super().list(query, page, page_size, sort, filters)
        page.content = [
            DataExceptionEndpoint(**data_exception).set_client(self.client)
            for data_exception in page.model_dump(by_alias=True)["content"]
        ]
        return page


class DataStoreEndpoint(StoreEndpoint):
    """Represents a data store endpoint"""

    """Represents a data store endpoint"""

    @property
    def exceptions(self) -> DataStoreExceptionsEndpoint:
        """Get the document stores endpoint of the project

        Returns:
            DataStoreExceptionsEndpoint: The document stores endpoint of the project
        """
        return DataStoreExceptionsEndpoint(self, self.client)

    def get_data_objects_export(
            self,
            document_family: Optional[DocumentFamily] = None,
            output_format: str = "json",
            path: Optional[str] = None,
            root_name: str = "",
            friendly_names=True,
    ) -> str:
        """Get the data objects export of the store

        Args:
            document_family (Optional[DocumentFamily]): The document family to limit results to
            output_format (str): The output format of the data objects export. Defaults to "json"
            path (Optional[str]): The path to the data object
            root_name (str): The root name of the data objects export
            friendly_names (bool): Whether to use friendly names. Defaults to True

        Returns:
            str: The data objects export of the store
        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        params = {
            "format": output_format,
            "friendlyNames": friendly_names,
            "rootName": root_name,
        }
        if document_family:
            params["documentFamilyId"] = document_family.id

        if path:
            params["path"] = path

        if output_format == "csv" and not path:
            raise ValueError("CSV output requires a path")

        response = self.client.get(url, params=params)
        return response.text

    def get_taxonomies(self) -> List[Taxonomy]:
        """Get the taxonomies of the store

        Returns:
            List[Taxonomy]: The taxonomies of the store
        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/taxonomies"
        taxonomy_response = self.client.get(url)
        return [
            TaxonomyEndpoint.model_validate(taxonomy_response)
            for taxonomy_response in taxonomy_response.json()
        ]

    def get_data_objects_df(
            self,
            path: str,
            query: str = "*",
            document_family: Optional[DocumentFamily] = None,
            include_id: bool = False,
            parent_id: Optional[str] = None,
    ):
        """
        Get the data objects as a pandas dataframe

        Args:
            path (str): The path to the data object
            query (str): A query to limit the results. Defaults to "*"
            document_family (Optional[DocumentFamily): The document family to limit results to
            include_id (bool): Whether to include the data object ID as a column. Defaults to False
            parent_id (Optional[str]): The parent ID to limit results to

        Returns:
            DataFrame: The data objects as a pandas dataframe
        """
        import pandas as pd

        data_objects = self.get_data_objects(path, query, document_family, parent_id)

        if len(data_objects) == 0:
            return pd.DataFrame()

        taxonomy: TaxonomyEndpoint = self.client.get_object_by_ref(
            "taxonomies", data_objects[0].taxonomy_ref
        )

        table_result = {"rows": [], "columns": [], "column_headers": []}

        for data_object in data_objects:
            if len(table_result["columns"]) == 0:
                if include_id:
                    table_result["column_headers"].append("Data Object ID")
                    table_result["columns"].append("data_object_id")
                    table_result["column_headers"].append("Parent Data Object ID")
                    table_result["columns"].append("parent_id")

                for taxon in taxonomy.get_taxon_by_path(data_object.path).children:
                    if not taxon.group:
                        table_result["column_headers"].append(taxon.label)
                        table_result["columns"].append(taxon.name)

            new_row = []
            for column in table_result["columns"]:
                column_value = None
                if include_id:
                    if column == "data_object_id":
                        column_value = data_object.id
                    if column == "parent_id":
                        column_value = data_object.parent_id
                for attribute in data_object.attributes:
                    if attribute.tag == column:
                        column_value = attribute.string_value
                new_row.append(column_value)

            table_result["rows"].append(new_row)

        return pd.DataFrame(
            table_result["rows"], columns=table_result["column_headers"]
        )

    def get_data_objects(
            self,
            path: str,
            query: str = "*",
            document_family: Optional[DocumentFamily] = None,
            parent_id: Optional[str] = None,
    ) -> List[DataObjectEndpoint]:
        """
        Get the data objects of the store

        Args:
            path (str): The path to the data object
            query (str): A query to limit the results. Defaults to "*"
            document_family (Optional[DocumentFamily): The document family to limit results to
            parent_id (Optional[str]): The parent ID to limit results to

        Returns:
            List[DataObjectEndpoint]: The data objects of the store
        """

        # We need to get the first set of rows,
        rows: List = []
        row_response = self.get_data_objects_page_request(
            path, 1, document_family=document_family, parent_id=parent_id
        )

        # lets work out the last page
        rows = rows + row_response.content
        total_pages = row_response.total_pages

        for page in range(2, total_pages + 1):
            row_response = self.get_data_objects_page_request(
                path,
                page,
                query=query,
                document_family=document_family,
                parent_id=parent_id,
            )
            rows = rows + row_response.content

        return rows

    def get_data_object(self, data_object_id: str):
        """Get a data object by id

        Args:
            data_object_id (str): The ID of the data object

        Returns:
            DataObjectEndpoint: The data object with the given ID
        """

        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects/{data_object_id}"
        logger.info(f"Downloading a specific data object from {url}")

        data_object_response = self.client.get(url)
        return DataObjectEndpoint.model_validate(data_object_response.json())

    def get_data_objects_page_request(
            self,
            path: str,
            page_number: int = 1,
            page_size=20,
            query="*",
            document_family: Optional[DocumentFamily] = None,
            parent_id: Optional[str] = None,
    ) -> PageDataObject:
        """
        Get a page of data objects

        Args:
            path (str): The parent taxon ("/" is root)
            page_number (int): The page number to get. Defaults to 1
            page_size (int): The size of the page. Defaults to 20
            query (str): The query to limit results. Defaults to "*"
            document_family (Optional[DocumentFamily): The document family to limit results to
            parent_id (Optional[str]): The parent ID to limit results to

        Returns:
            PageDataObject: A page of data objects
        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects"

        if parent_id:
            url += f"/{parent_id}/children"
        logger.debug(f"Downloading a specific table from {url}")

        # We need to go through and pull all the pages
        params = {
            "path": path,
            "page": page_number,
            "pageSize": page_size,
            "query": query,
        }

        if document_family:
            params["documentFamilyId"] = document_family.id
            params["storeRef"] = document_family.store_ref

        data_objects_response = self.client.get(url, params=params)
        data_object_page = PageDataObject.model_validate(data_objects_response.json())
        data_object_page.content = [
            DataObjectEndpoint(**data_object).set_client(self.client)
            for data_object in data_object_page.model_dump(by_alias=True)["content"]
        ]
        return data_object_page

    def stream_data_objects(
            self,
            path: str,
            query="*",
            document_family: Optional[DocumentFamily] = None,
            parent_id: Optional[str] = None,
    ):
        """
        Stream page request

        Args:
            path (str): The parent taxon ("/" is root)
            query (str): The query to limit results. Defaults to "*"
            document_family (Optional[DocumentFamily): The document family to limit results to
            parent_id (Optional[str]): The parent ID to limit results to
        """
        page_size = 20
        page = 1

        while True:
            data_object_response = self.get_data_objects_page_request(
                path, page, page_size, query, document_family, parent_id
            )
            if not data_object_response.content:
                break
            for data_object in data_object_response.content:
                yield data_object

            page += 1

    def create_data_objects(
            self, data_objects: List[DataObject]
    ) -> List[DataObjectEndpoint]:
        """
        Create data objects in the store

        Args:
            data_objects (List[DataObject]): A list of data objects that you want to create

        Returns:
            List[DataObjectEndpoint]: The created data objects
        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/dataObjects"
        logger.debug(f"Creating data objects in store {url}")

        create_response = requests.post(
            url, json=[data_object.dict(by_alias=True) for data_object in data_objects]
        )
        return [
            DataObjectEndpoint.model_validate(data_object)
            for data_object in create_response.json()
        ]


class DocumentStoreEndpoint(StoreEndpoint):
    """Represents a document store that can be used to store files and then their related document representations"""

    def query_by_embedding(self, embedding: list[float], threshold: float, limit: int):
        """
        Query the document store by an embedding.

        Args:
            embedding (list[float]): The embedding to query by.
            threshold (int): The threshold to use for the query.
            limit (int): The limit of the query.

        Returns:
            list[DocumentEmbedding]: a list of document embeddings
        """
        url = "/api/embeddings/query"
        embedding_query = {"embedding": embedding, "threshold": threshold, "limit": limit, "storeRef": self.ref}
        response = self.client.post(url, body=embedding_query)
        process_response(response)

        # We get a list of the document embeddings
        return [DocumentEmbedding.model_validate(embedding) for embedding in response.json()]

    def delete_by_path(self, object_path: str):
        """
        Delete the content stored in the store at the given path.

        Args:
            object_path (str): The path to the document family (ie. Invoice.pdf).
        """
        self.client.delete(
            f"/api/stores/{self.ref.replace(':', '/')}/fs", params={"path": object_path}
        )

    def import_family(self, file_path: str):
        """
        Import a document family from a file.

        Args:
            file_path (str): The path to the file.
        """
        if Path(file_path).is_file():
            logger.info(f"Uploading {file_path}")
            with open(file_path, "rb") as dfm_content:
                files = {"familyZip": dfm_content}
                content_object_response = self.client.post(
                    f"/api/stores/{self.ref.replace(':', '/')}/families",
                    params={"import": "true"},
                    files=files,
                )
                logger.info(f"Uploaded ({content_object_response.status_code})")
                return DocumentFamilyEndpoint.model_validate(
                    content_object_response.json()
                ).set_client(self.client)
        else:
            raise Exception(f"{file_path} is not a file")

    def upload_file(
            self,
            file_path: str,
            object_path: Optional[str] = None,
            replace=False,
            additional_metadata: Optional[dict] = None,
            external_data: Optional[dict] = None,
            document: Optional[Document] = None,
    ):
        """
        Upload a file to the store.

        Args:
            file_path (str): The path to the file.
            object_path (Optional[str]): The path to the object (Default is the same the file path).
            replace (bool): Replace the file if it already exists (Default False).
            additional_metadata (Optional[dict]): Additional metadata to add to the file (Default None).
            external_data (Optional[dict]): External data to add to the file (Default None).
            document (Optional[Document]): The document to add to the file (Default None).
        """
        if Path(file_path).is_file():
            logger.info(f"Uploading {file_path}")
            with open(file_path, "rb") as path_content:
                return self.upload_bytes(
                    path=object_path if object_path is not None else file_path,
                    content=path_content,
                    replace=replace,
                    additional_metadata=additional_metadata,
                    external_data=external_data,
                    document=document,
                )
        else:
            raise Exception(f"{file_path} is not a file")

    def upload_bytes(
            self,
            path: str,
            content,
            replace=False,
            additional_metadata: Optional[dict] = None,
            external_data: Optional[dict] = None,
            document: Optional[Document] = None,
    ) -> DocumentFamilyEndpoint:
        """
        Put the content into the store at the given path.

        Args:
            path (str): The path you wish to put the content at.
            content: The content for that object.
            replace (bool): Replace the content if it exists.
            additional_metadata (Optional[dict]): Additional metadata to store with the document (not it can't include 'path').
            external_data (Optional[dict]): External data to store with the document.
            document (Optional[Document]): The document to store with the content.

        Returns:
            DocumentFamilyEndpoint: The document family that was created.
        """
        files = {"file": content, "document": document.to_kddb()} if document else {"file": content}

        if additional_metadata is None:
            additional_metadata = {}

        if external_data is not None:
            additional_metadata["externalData"] = json.dumps(external_data)

        if replace and self.client.exists(
                f"/api/stores/{self.ref.replace(':', '/')}/fs", params={"path": path}
        ):
            try:
                self.client.delete(
                    f"/api/stores/{self.ref.replace(':', '/')}/fs",
                    params={"path": path},
                )
                logger.info(f"Deleting {path}")
            except Exception as e:
                logger.info(f"No file to replace. Continuing upload. Error: {e}")

        content_object_response = self.client.post(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": path},
            data=additional_metadata,
            files=files,
        )
        logger.info(f"Uploaded {path} ({content_object_response.status_code})")
        return DocumentFamilyEndpoint.model_validate(
            content_object_response.json()
        ).set_client(self.client)

    def get_bytes(self, object_path: str):
        """
        Get the bytes for the object at the given path, will return None if there is no object there.

        Args:
            object_path (str): The object path.

        Returns:
            bytes: The bytes or None is nothing is at the path.
        """
        return self.client.get(
            f"/api/stores/{self.ref.replace(':', '/')}/fs", params={"path": object_path}
        ).content

    def list_contents(self) -> List[str]:
        """
        List the contents of the store.

        Returns:
            List[str]: A list of the contents of the store.
        """

        # TODO We need to remove this
        params = {"page": 1, "pageSize": 90, "query": "*"}
        get_response = self.client.get(
            f"api/stores/{self.ref.replace(':', '/')}/families", params=params
        )
        paths = []
        for fam_dict in get_response.json()["content"]:
            paths.append(fam_dict["path"])
        return paths

    def download_document_families(self, output_dir: str):
        """
        Download all the document families in the store to the given directory.

        Args:
            output_dir (str): The directory to download the document families to.
        """

        for document_family in self.stream_query():
            export_bytes = document_family.export()
            with open(os.path.join(output_dir, document_family.id + ".dfm"), "wb") as f:
                f.write(export_bytes)

    def reprocess_document_families(
            self, document_family_ids: List[str], assistant: AssistantEndpoint
    ):
        """
        Reprocess the document families with the given ids through the assistant in a bulk fashion.

        Args:
            document_family_ids (List[str]): The ids of the document families to reprocess.
            assistant (AssistantEndpoint): The assistant to use for reprocessing.
        """
        request = ReprocessRequest()
        request.assistant_ids = [assistant.id]

        # Dont process locked doc_familys. Iterate through the list in reverse to avoid index issues when removing items
        for i in range(len(document_family_ids) - 1, -1, -1):
            if self.get_family(document_family_ids[i]).locked:
                del document_family_ids[i]

        request.family_ids = document_family_ids

        self.client.put(
            f"api/stores/{self.ref.replace(':', '/')}/reprocess",
            body=request.model_dump(mode="json", by_alias=True),
        )

    def get_metadata_class(self):
        """
        Get the metadata class for the store.

        Returns:
            type: The metadata class for the store.
        """
        return DocumentContentMetadata

    def get_family(self, document_family_id: str) -> DocumentFamilyEndpoint:
        """
        Get the document family with the given id.

        Args:
            document_family_id (str): The id of the document family to get.

        Returns:
            DocumentFamilyEndpoint: The document family with the given id.
        """
        logger.info(f"Getting document family id {document_family_id}")
        document_family_response = self.client.get(
            f"/api/stores/{self.ref.replace(':', '/')}/families/{document_family_id}"
        )
        return DocumentFamilyEndpoint.model_validate(
            document_family_response.json()
        ).set_client(self.client)

    def stream_query(self, query: str = "*", sort=None, limit=None):
        """
        Stream the query for the document family.

        Args:
            query (str, optional): The query to run. Defaults to "*".
            sort (str, optional): Sorting order of the query. Defaults to None.
            limit (int, optional): The maximum number of items to return. Defaults to None.

        Returns:
            generator: A generator of the document families.
        """
        page_size = 5
        page = 1
        number_of_items = 0

        if not sort:
            sort = "id"

        while True:
            page_response = self.query(
                query=query, page=page, page_size=page_size, sort=sort
            )
            if not page_response.content:
                break
            for document_family in page_response.content:
                number_of_items += 1
                if limit and number_of_items > limit:
                    break

                yield document_family

            page += 1

    def query(
            self, query: str = "*", page: int = 1, page_size: int = 100, sort=None
    ) -> PageDocumentFamilyEndpoint:
        """
        Query the document family.

        Args:
            query (str, optional): The query to run. Defaults to "*".
            page (int, optional): The page number to get. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 100.
            sort (str, optional): Sorting order of the query. Defaults to None.

        Returns:
            PageDocumentFamilyEndpoint: The page of document families.
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "query": requests.utils.quote(query),
        }

        if sort is not None:
            params["sort"] = sort

        get_response = self.client.get(
            f"api/stores/{self.ref.replace(':', '/')}/families", params=params
        )

        return PageDocumentFamilyEndpoint.model_validate(
            get_response.json()
        ).set_client(self.client)

    def stream_filter(self, filter_string: str = "", sort=None, limit=None):
        """
        Stream the filter for the document family.

        Args:
            filter_string (str, optional): The filter string to use. Defaults to "".
            sort (str, optional): Sorting order of the query. Defaults to None.
            limit (int, optional): The maximum number of items to return. Defaults to None.

        Returns:
            generator: A generator of the document families.
        """
        page_size = 5
        page = 1
        count = 0
        if not sort:
            sort = "id"

        while True:
            page_response = self.filter(
                filter_string=filter_string, page=page, page_size=page_size, sort=sort
            )
            if not page_response.content:
                break
            for document_family in page_response.content:
                yield document_family
                count += 1
                if limit and count >= limit:
                    break
            if limit and count >= limit:
                break
            page += 1

    def filter(
            self, filter_string: str = "", page: int = 1, page_size: int = 100, sort=None
    ) -> PageDocumentFamilyEndpoint:
        """
        Filter the document family.

        Args:
            filter_string (str, optional): The filter string to use. Defaults to "".
            page (int, optional): The page number to get. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 100.
            sort (str, optional): Sorting order of the query. Defaults to None.

        Returns:
            PageDocumentFamilyEndpoint: The page of document families.
        """
        params = {"page": page, "pageSize": page_size, "filter": filter_string}

        if sort is not None:
            params["sort"] = sort

        get_response = self.client.get(
            f"api/stores/{self.ref.replace(':', '/')}/families", params=params
        )

        return PageDocumentFamilyEndpoint.model_validate(
            get_response.json()
        ).set_client(self.client)

    def upload_document(
            self, path: str, document: "Document"
    ) -> DocumentFamilyEndpoint:
        """
        Upload a document to the store at the given path.

        Args:
            path (str): The path to upload the document to.
            document (Document): The document to upload.

        Returns:
            DocumentFamilyEndpoint: The document family that was created.
        """
        logger.info(f"Putting document to path {path}")

        files = {"file": document.to_kddb()}
        data = {"path": path, "documentVersion": document.version, "document": True}
        document_family_response = self.client.post(
            f"/api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": path},
            files=files,
            data=data,
        )

        return DocumentFamilyEndpoint.model_validate(
            document_family_response.json()
        ).set_client(self.client)

    def exists_by_path(self, path: str) -> bool:
        """
        Check if the store has a document family at the given path.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if a document family exists at the given path, False otherwise.
        """
        return self.client.exists(
            f"/api/stores/{self.ref.replace(':', '/')}/fs", params={"path": path}
        )

    def get_by_path(self, path: str) -> DocumentFamilyEndpoint:
        """
        Get the document family at the given path.

        Args:
            path (str): The path to get the document family from.

        Returns:
            DocumentFamilyEndpoint: The document family at the given path.
        """
        get_response = self.client.get(
            f"api/stores/{self.ref.replace(':', '/')}/fs",
            params={"path": path, "meta": True},
        )
        process_response(get_response)
        return DocumentFamilyEndpoint.model_validate(get_response.json()).set_client(
            self.client
        )

    def delete_families(self):
        """
        Delete all the families in the store.
        """
        delete_response = self.client.delete(
            f"api/stores/{self.ref.replace(':', '/')}/families"
        )
        process_response(delete_response)


class ModelStoreEndpoint(DocumentStoreEndpoint):
    """Represents a model store

    Attributes:
        IMPLEMENTATION_PREFIX (ClassVar[str]): Prefix for the model implementation.
        TRAINED_MODELS_PREFIX (ClassVar[str]): Prefix for the trained models.
    """

    """Represents a model store"""
    IMPLEMENTATION_PREFIX: ClassVar[str] = "model_implementation/"
    TRAINED_MODELS_PREFIX: ClassVar[str] = "trained_models/"

    def get_metadata_class(self):
        """Get the metadata class for the store

        Returns:
            ModelContentMetadata: The metadata class for the store.
        """
        return ModelContentMetadata

    def upload_trained_model(
            self, training_run_id: str, base_path: Optional[str] = None
    ):
        """Upload a trained model to the store

        Args:
            training_run_id (str): The ID of the training run.
            base_path (str, optional): The base path of the model. Defaults to None.

        Returns:
            list: A list of results from the upload.
        """
        results = []
        final_wildcard = "**/*" if base_path is None else f"{base_path}/**/*"
        num_hits = 0
        import zipfile

        with zipfile.ZipFile("training.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
            for path_hit in glob.glob(final_wildcard, recursive=True):
                relative_path = (
                    path_hit.replace(base_path + "/", "") if base_path else path_hit
                )

                if Path(path_hit).is_file():
                    zipf.write(path_hit, relative_path)
                    num_hits += 1

        if num_hits > 0:
            logger.info(f"Uploading {num_hits} files to store (training.zip)")
            self.client.post(
                f"/api/stores/{self.ref.replace(':', '/')}/trainings/{training_run_id}/content",
                files={"training": open("training.zip", "rb")},
            )
            results.append(f"{num_hits} files uploaded for {final_wildcard}")

        logger.info(
            f"Uploading training run {training_run_id} to store, deleting local"
        )
        Path("training.zip").unlink()
        return results

    def download_trained_model(
            self, training_id: str, download_path: Optional[str] = ""
    ):
        """Download the content for the given training id

        Args:
            training_id (str): The ID of the training.
            download_path (str, optional): The path to download the content to. Defaults to "".
        """
        if download_path is None:
            download_path = ""
        if download_path != "":
            os.makedirs(download_path, exist_ok=True)
        response = self.client.get(
            f"/api/stores/{self.ref.replace(':', '/')}/trainings/{training_id}/content"
        )
        process_response(response)
        from zipfile import ZipFile
        from io import BytesIO

        zipped_contents = ZipFile(BytesIO(response.content))
        zipped_contents.extractall(download_path)

    def download_implementation(self, download_path: Optional[str] = ""):
        """Download the implementation from the store

        Args:
            download_path (str, optional): The path to download the implementation to. Defaults to "".
        """
        if download_path is None:
            download_path = ""
        if download_path != "":
            os.makedirs(download_path, exist_ok=True)
        response = self.client.get(
            f"/api/stores/{self.ref.replace(':', '/')}/implementation"
        )
        process_response(response)
        from zipfile import ZipFile
        from io import BytesIO

        logger.info(
            f"Downloading implementation package to {download_path}, and extracting"
        )
        zipped_contents = ZipFile(BytesIO(response.content))
        zipped_contents.extractall(download_path)

    def upload_implementation(self, metadata):
        """Upload the implementation to the store

        Args:
            metadata (ModelContentMetadata): The metadata of the implementation.

        Returns:
            list: A list of results from the upload.
        """
        return self.upload_contents(metadata)

    def create_training(
            self,
            name: Optional[str] = None,
            training_parameters: Optional[Dict[str, Any]] = None,
            user_test=False,
    ) -> ModelTraining:
        """Create a new model training

        Args:
            name (str, optional): The name of the training. Defaults to None.
            training_parameters (Dict[str, Any], optional): The parameters for the training. Defaults to None.
            user_test (bool, optional): Whether the training is a user test. Defaults to False.

        Returns:
            ModelTraining: The created model training.
        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/trainings"
        new_training = ModelTraining(name=name, user_test=user_test)

        if training_parameters is not None:
            new_training.training_parameters = training_parameters

        response = self.client.post(
            url, body=json.loads(new_training.json(by_alias=True))
        )
        return ModelTraining.model_validate(response.json())

    def update_training(self, training: ModelTraining) -> ModelTraining:
        """Update a model training

        Args:
            training (ModelTraining): The training to update.

        Returns:
            ModelTraining: The updated model training.
        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/trainings/{training.id}"
        response = self.client.put(
            url, body=json.loads(training.model_dump_json(by_alias=True))
        )
        return ModelTraining.model_validate(response.json())

    def delete_training(self, training_id: str):
        """Delete a model training

        Args:
            training_id (str): The ID of the training to delete.
        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/trainings/{training_id}"
        self.client.delete(url)

    def get_training(self, training_id: str) -> ModelTraining:
        """Get a model training

        Args:
            training_id (str): The ID of the training to get.

        Returns:
            ModelTraining: The requested model training.
        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/trainings/{training_id}"
        response = self.client.get(url)
        return ModelTraining.model_validate(response.json())

    def stream_list_trainings(self, query="*", sort=None, filters: List[str] = None):
        """
            Stream the list of model trainings

        Args:
            query (str): the query to run
            sort (str): sorting order of the list
            filters (List[str]): in a format of list, for example: ["name=training1", "status=completed"]
        """
        page_size = 5
        page = 1

        if not sort:
            sort = "id"

        while True:
            page_response = self.list_trainings(query=query, page=page, page_size=page_size, sort=sort, filters=filters)
            if not page_response.content:
                break
            for training in page_response.content:
                yield training
            page += 1

    def list_trainings(
            self, query="*", page=1, page_size=10, sort=None, filters: List[str] = None
    ) -> PageModelTraining:
        """List all model trainings

        Args:
            query (str, optional): The query to filter the trainings. Defaults to "*".
            page (int, optional): The page number. Defaults to 1.
            page_size (int, optional): The size of the page. Defaults to 10.
            sort (str, optional): The sort order. Defaults to None.
            filters (List[str], optional): The filters to apply. Defaults to None.

        Returns:
            PageModelTraining: The page of model trainings.
        """
        url = f"/api/stores/{self.ref.replace(':', '/')}/trainings"
        params = {
            "query": requests.utils.quote(query),
            "page": page,
            "pageSize": page_size,
        }

        if sort is not None:
            params["sort"] = sort

        if filters is not None:
            params["filter"] = filters

        response = self.client.get(url, params=params)
        return PageModelTraining.model_validate(response.json())

    @staticmethod
    def build_implementation_zip(metadata: ModelContentMetadata):
        """Build a zip file for the implementation

        Args:
            metadata (ModelContentMetadata): The metadata of the implementation.

        Returns:
            int: The number of files in the zip.
        """
        import zipfile

        num_hits = 0

        with zipfile.ZipFile("implementation.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
            ignore_files = []
            if metadata.ignored_contents:
                for ignore_path in metadata.ignored_contents:
                    final_wildcard = (
                        os.path.join(metadata.base_dir, ignore_path)
                        if metadata.base_dir
                        else ignore_path
                    )
                    for path_hit in glob.glob(final_wildcard, recursive=True):
                        ignore_files.append(path_hit)

            for content_path in metadata.contents:
                final_wildcard = (
                    os.path.join(metadata.base_dir, content_path)
                    if metadata.base_dir
                    else content_path
                )

                for path_hit in glob.glob(final_wildcard, recursive=True):
                    if path_hit in ignore_files:
                        continue
                    relative_path = (
                        path_hit.replace(metadata.base_dir + "/", "")
                        if metadata.base_dir
                        else path_hit
                    )

                    # We will put the implementation in one place
                    if Path(path_hit).is_file():
                        zipf.write(path_hit, relative_path)
                        num_hits += 1

        if num_hits == 0:
            print(
                f"No files found for implementation in {metadata.base_dir} with {metadata.contents}"
            )

        return num_hits

    def upload_contents(self, metadata: ModelContentMetadata, dry_run=False):
        """Upload the contents of the metadata to the store

        Args:
            metadata (ModelContentMetadata): The metadata of the contents.
            dry_run (bool, optional): Whether to perform a dry run. Defaults to False.

        Returns:
            list: A list of results from the upload.
        """
        results = []
        if metadata.contents:
            num_hits = self.build_implementation_zip(metadata)
            if num_hits > 0 and not dry_run:
                with open("implementation.zip", "rb") as zip_content:
                    response = self.client.post(
                        f"/api/stores/{self.ref.replace(':', '/')}/implementation",
                        files={"implementation": zip_content},
                    )
                    process_response(response)
                results.append(f"{num_hits} files packaged and deployed to {self.ref}")
        if not metadata.keep_zip:
            Path("implementation.zip").unlink()
        return results


class TaxonomiesEndpoint(ComponentEndpoint, ClientEndpoint, OrganizationOwned):
    """Represents a taxonomies endpoint

    This class is used to represent a taxonomies endpoint. It inherits from
    ComponentEndpoint, ClientEndpoint, and OrganizationOwned classes.

    Attributes:
        None
    """

    """Represents a taxonomies endpoint"""

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint, in this case "taxonomies".
        """
        return "taxonomies"

    def get_page_class(self, object_dict=None):
        """Get the page class for the endpoint

        This method is used to get the page class for the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            PageTaxonomyEndpoint: The page class for the endpoint.
        """
        return PageTaxonomyEndpoint

    def get_instance_class(self, object_dict=None):
        """Get the instance class for the endpoint

        This method is used to get the instance class for the endpoint.

        Args:
            object_dict (dict, optional): An optional dictionary object. Defaults to None.

        Returns:
            TaxonomyEndpoint: The instance class for the endpoint.
        """
        return TaxonomyEndpoint


def process_response(response) -> requests.Response:
    """
    This function processes the server response. It checks the status code of the response and raises an exception with
    a specific message depending on the status code. If the status code is 401, it raises an "Unauthorized" exception.
    If the status code is 404, it raises a "Not found" exception.
    If the status code is 405, it raises a "Method not allowed" exception.
    If the status code is 500, it raises an "Internal server error" exception.
    If the status code is 400, it checks if the response has a JSON body with an "errors" field.
    If so, it raises an exception with a message containing all the errors.
    If not, it raises a "Bad request" exception.
    If the status code is anything other than 200, it raises an "Unexpected response" exception.
    If the status code is 200, it returns the response as is.

    Args:
        response (requests.Response): The server response to process.

    Returns:
        requests.Response: The original server response if the status code is 200.

    Raises:
        Exception: If the status code is not 200, an exception is raised with a message specific to the status code.
    """
    if response.status_code == 401:
        raise Exception(f"Unauthorized ({response.text})")
    if response.status_code == 404:
        raise Exception(f"Not found ({response.text})")
    if response.status_code in [301, 302]:
        raise Exception(f"Redirected ({response.text})")
    if response.status_code == 405:
        raise Exception("Method not allowed")
    if response.status_code == 500:
        raise Exception("Internal server error: \n" + response.text)
    if response.status_code == 400:
        if response.json() and response.json().get("errors"):
            messages = []
            for key, value in response.json()["errors"].items():
                messages.append(f"{key}: {value}")
            raise Exception(", ".join(messages))

        raise Exception("Bad request " + response.text)

    return response


OBJECT_TYPES = {
    "extensionPacks": {
        "name": "extensionPack",
        "plural": "extensionPacks",
        "type": ExtensionPackEndpoint,
        "endpoint": ExtensionPacksEndpoint,
    },
    "dashboards": {
        "name": "dashboard",
        "plural": "dashboards",
        "type": DashboardEndpoint,
        "endpoint": DashboardsEndpoint,
    },
    "dataForms": {
        "name": "dataForm",
        "plural": "dataForms",
        "type": DataFormEndpoint,
        "endpoint": DataFormsEndpoint,
    },
    "pipelines": {
        "name": "pipeline",
        "plural": "pipelines",
        "type": PipelineEndpoint,
        "endpoint": PipelinesEndpoint,
    },
    "assistants": {
        "name": "assistant",
        "plural": "assistants",
        "type": AssistantEndpoint,
        "endpoint": AssistantsEndpoint,
        "global": True,
    },
    "assistantDefinitions": {
        "name": "assistantDefinition",
        "plural": "assistantDefinitions",
        "type": AssistantDefinitionEndpoint,
        "endpoint": AssistantDefinitionsEndpoint,
    },
    "actions": {
        "name": "action",
        "plural": "actions",
        "type": ActionEndpoint,
        "endpoint": ActionsEndpoint,
    },
    "prompts": {
        "name": "prompt",
        "plural": "prompts",
        "type": PromptEndpoint,
        "endpoint": PromptsEndpoint,
    },
    "guidance": {
        "name": "guidance",
        "plural": "guidance",
        "type": GuidanceSetEndpoint,
        "endpoint": GuidanceSetsEndpoint,
    },
    "modelRuntimes": {
        "name": "modelRuntime",
        "plural": "modelRuntimes",
        "type": ModelRuntimeEndpoint,
        "endpoint": ModelRuntimesEndpoint,
    },
    "credentialDefinitions": {
        "name": "credentialDefinition",
        "plural": "credentialDefinitions",
        "type": CredentialDefinitionEndpoint,
        "endpoint": CredentialDefinitionsEndpoint,
    },
    "taxonomies": {
        "name": "taxonomy",
        "plural": "taxonomies",
        "type": TaxonomyEndpoint,
        "endpoint": TaxonomiesEndpoint,
    },
    "stores": {"name": "store", "plural": "stores", "endpoint": StoresEndpoint},
    "projects": {
        "name": "project",
        "plural": "projects",
        "type": ProjectEndpoint,
        "endpoint": ProjectsEndpoint,
        "global": True,
    },
    "workspaces": {
        "name": "workspace",
        "plural": "workspaces",
        "type": WorkspaceEndpoint,
        "endpoint": WorkspacesEndpoint,
        "global": True,
    },
    "organizations": {
        "name": "organization",
        "plural": "organizations",
        "type": OrganizationEndpoint,
        "endpoint": OrganizationsEndpoint,
        "global": True,
    },
    "channels": {
        "name": "channel",
        "plural": "channels",
        "type": ChannelEndpoint,
        "endpoint": ChannelsEndpoint,
        "global": True,
    },
    "projectTemplates": {
        "name": "projectTemplate",
        "plural": "projectTemplates",
        "type": ProjectTemplateEndpoint,
        "endpoint": ProjectTemplatesEndpoint,
    },
    "executions": {
        "name": "execution",
        "plural": "executions",
        "type": Execution,
        "global": True,
        "sort": "startDate:desc",
        "endpoint": ExecutionsEndpoint,
    },
    "memberships": {
        "name": "membership",
        "plural": "memberships",
        "type": MembershipEndpoint,
        "global": True,
        "endpoint": MembershipsEndpoint,
    },
}


def resolve_object_type(obj_type):
    """
    This function takes a part of an object type (e.g., 'pipeline') and resolves it to the full object type (e.g., 'pipelines').

    Args:
        obj_type (str): A string representing part of the object type.

    Returns:
        tuple: A tuple containing the key and the object type dictionary, if found. If only one match is found,
        the key and the object type dictionary are returned. If no matches are found, an exception is raised.
        If multiple potential matches are found, an exception is raised.

    Raises:
        Exception: If no matches are found for the object type, or if multiple potential matches are found.
    """
    hits = []
    keys = []

    if not isinstance(obj_type, str):
        obj_type = str(obj_type).lower()
    else:
        obj_type = obj_type.lower()

    for target_type in OBJECT_TYPES.keys():
        if obj_type in target_type.lower():
            hits.append(OBJECT_TYPES[target_type])
            keys.append(target_type)

    if len(hits) == 1:
        return keys[0], hits[0]

    if len(hits) == 0:
        raise Exception(f"Unable to find object type {obj_type}")

    raise Exception(f"Too many potential matches for object type ({','.join(keys)}")


class ExtractionEngineEndpoint:
    """
    Provides endpoint access to the extraction engine.

    Attributes:
        client (KodexaClient): The client to interact with the extraction engine.
    """

    """
    Provides endpoint access to the extraction engine
    """

    def __init__(self, client: "KodexaClient"):
        self.client = client

    def extract_data_objects(
            self, taxonomy: Taxonomy, document: Document
    ) -> List[DataObject]:
        """
        Extracts data objects from the given document using the given taxonomy.

        Args:
            taxonomy (Taxonomy): The taxonomy to use for extraction.
            document (Document): The document to extract data from.

        Returns:
            List[DataObject]: The extracted data objects.
        """
        response = self.client.post(
            "/api/extractionEngine/extract",
            data={"taxonomyJson": taxonomy.model_dump_json(by_alias=True)},
            files={"document": document.to_kddb()},
        )
        print(response.json())
        return [
            DataObject.model_validate(data_object) for data_object in response.json()
        ]

    def extract_data_objects_with_exceptions(
            self, taxonomy: Taxonomy, document: Document
    ) -> Dict:
        """
        Extracts data objects from the given document using the given taxonomy and returns any exceptions.

        Args:
            taxonomy (Taxonomy): The taxonomy to use for extraction.
            document (Document): The document to extract data from.

        Returns:
            Dict: A dictionary containing the extracted data objects and any exceptions.
        """
        response = self.client.post(
            "/api/extractionEngine/extract",
            params="full",
            data={"taxonomyJson": taxonomy.model_dump_json(by_alias=True)},
            files={"document": document.to_kddb()},
        )
        return {
            "dataObjects": [
                DataObject.model_validate(data_object)
                for data_object in response.json()["dataObjects"]
            ],
            "exceptions": [
                ContentException.model_validate(exception)
                for exception in response.json()["contentExceptions"]
            ],
        }

    def extract_to_format(
            self, taxonomy: Taxonomy, document: Document, format: str
    ) -> str:
        """
        Extracts data from the given document using the given taxonomy and returns it in the given format.

        Args:
            taxonomy (Taxonomy): The taxonomy to use for extraction.
            document (Document): The document to extract data from.
            format (str): The format to return the extracted data in.

        Returns:
            str: The extracted data in the given format.
        """
        response = self.client.post(
            "/api/extractionEngine/extract",
            params={"format": format},
            data={"taxonomyJson": taxonomy.model_dump_json(by_alias=True)},
            files={"document": document.to_kddb()},
        )
        return response.text


class KodexaClient:
    """
    A class to represent a Kodexa client.

    Attributes:
        base_url (str): The base URL for the Kodexa platform.
        access_token (str): The access token for the Kodexa platform.
        organizations (OrganizationsEndpoint): An endpoint for organizations.
        projects (ProjectsEndpoint): An endpoint for projects.
        workspaces (WorkspacesEndpoint): An endpoint for workspaces.
        users (UsersEndpoint): An endpoint for users.
        memberships (MembershipsEndpoint): An endpoint for memberships.
        executions (ExecutionsEndpoint): An endpoint for executions.
        channels (ChannelsEndpoint): An endpoint for channels.
        messages (MessagesEndpoint): An endpoint for messages.
        assistants (AssistantsEndpoint): An endpoint for assistants.
        products (ProductsEndpoint): An endpoint for products.
        tasks (TasksEndpoint): An endpoint for tasks.
        retained_guidances (RetainedGuidancesEndpoint): An endpoint for retained guidances.
    """

    def __init__(self, url=None, access_token=None, profile=None):
        from kodexa import KodexaPlatform

        self.base_url = url if url is not None else KodexaPlatform.get_url(profile)
        self.access_token = (
            access_token
            if access_token is not None
            else KodexaPlatform.get_access_token(profile)
        )
        self.organizations = OrganizationsEndpoint(self)
        self.projects = ProjectsEndpoint(self)
        self.workspaces = WorkspacesEndpoint(self)
        self.users = UsersEndpoint(self)
        self.memberships = MembershipsEndpoint(self)
        self.executions = ExecutionsEndpoint(self)
        self.channels = ChannelsEndpoint(self)
        self.assistants = AssistantsEndpoint(self)
        self.messages = MessagesEndpoint(self)
        from kodexa.model.entities.product import ProductsEndpoint
        self.products = ProductsEndpoint(self)
        self.tasks = TasksEndpoint(self)
        self.retained_guidances = RetainedGuidancesEndpoint(self)

    @staticmethod
    def login(url, token):
        """
        A static method to login to the Kodexa platform.

        Args:
            url (str): The URL for the Kodexa platform.
            token (str): The email for the user.

        Returns:
            KodexaClient: A KodexaClient instance.

        Raises:
            Exception: If the status code is not 200.
        """

        obj_response = requests.get(
            f"{url}/api/account/me",
            headers={"content-type": "application/json",
                     "x-access-token": token,
                     "cf-access-token": os.environ.get("CF_TOKEN", "")}
        )
        if obj_response.status_code == 200:
            return KodexaClient(url, obj_response.text)

        raise Exception(f"Check your URL and password [{obj_response.status_code}]")

    @property
    def me(self):
        """
        A property that returns the UserEndpoint instance for the current user.

        Returns:
            UserEndpoint: The UserEndpoint instance for the current user.
        """
        return UserEndpoint.model_validate(
            self.get("/api/account/me").json()
        ).set_client(self)

    @property
    def extraction_engine(self):
        """
        A property that returns the ExtractionEngineEndpoint instance.

        Returns:
            ExtractionEngineEndpoint: The ExtractionEngineEndpoint instance.
        """
        return ExtractionEngineEndpoint(self)

    @property
    def platform(self) -> PlatformOverview:
        """
        A property that returns the PlatformOverview instance.

        Returns:
            PlatformOverview: The PlatformOverview instance.
        """
        return PlatformOverview.model_validate(self.get("/api").json())

    def change_password(self, old_password: str, new_password: str):
        """
        A method to change the password for the current user.

        Args:
            old_password (str): The old password.
            new_password (str): The new password.

        Returns:
            requests.Response: The response from the server.
        """
        return self.post(
            "/api/account/passwordChange",
            body={"oldPassword": old_password, "newPassword": new_password},
        )

    def __build_object(self, ref, object_type_metadata):
        """
        A private method to build an object from the given reference and object type metadata.

        Args:
            ref (str): The reference for the object.
            object_type_metadata (dict): The metadata for the object type.

        Returns:
            BaseModel: The built object.
        """
        url = f"/api/{object_type_metadata['plural']}/{ref.replace(':', '/')}"
        response = process_response(self.get(url))

        # We need to merge the use of the object type metadata
        # and the deserialize method better

        if "type" not in object_type_metadata:
            return self.deserialize(response.json())
        instance = object_type_metadata["type"](**response.json())
        if isinstance(instance, ClientEndpoint):
            instance.set_client(self)

        return instance

    def get_object_by_ref(self, object_type: str, ref: str) -> BaseModel:
        """
        A method to get an object by its reference.

        Args:
            object_type (str): The type of the object.
            ref (str): The reference for the object.

        Returns:
            BaseModel: The object.
        """
        return self.__build_object(ref, resolve_object_type(object_type)[1])

    def get_object_endpoint(self, object_type: str) -> BaseModel:
        """
        A method to get an object endpoint.

        Args:
            object_type (str): The type of the object.

        Returns:
            BaseModel: The object endpoint.
        """
        pass

    def get_platform(self):
        """
        A method to get the PlatformOverview instance.

        Returns:
            PlatformOverview: The PlatformOverview instance.
        """
        return PlatformOverview.model_validate(self.get(f"{self.base_url}/api").json())

        # The followings methods are helpers for working with requests

    def exists(self, url, params=None) -> bool:
        """
        A method to check if a URL exists.

        Args:
            url (str): The URL to check.
            params (dict, optional): The parameters for the request. Defaults to None.

        Returns:
            bool: True if the URL exists, False otherwise.
        """
        response = requests.get(
            self.get_url(url),
            params=params,
            headers={
                "x-access-token": self.access_token,
                "cf-access-token": os.environ.get("CF_TOKEN", ""),
                "content-type": "application/json",
            },
        )
        if response.status_code == 200:
            return True
        if response.status_code == 404:
            return False

        process_response(response)

    def get(self, url, params=None) -> requests.Response:
        """
        A method to send a GET request.

        Args:
            url (str): The URL for the request.
            params (dict, optional): The parameters for the request. Defaults to None.

        Returns:
            requests.Response: The response from the server.
        """
        response = requests.get(
            self.get_url(url),
            params=params,
            headers={
                "x-access-token": self.access_token,
                "cf-access-token": os.environ.get("CF_TOKEN", ""),
                "content-type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            }
        )

        return process_response(response)

    def post(
            self, url, body=None, data=None, files=None, params=None
    ) -> requests.Response:
        """
        A method to send a POST request.

        Args:
            url (str): The URL for the request.
            body (dict, optional): The body for the request. Defaults to None.
            data (dict, optional): The data for the request. Defaults to None.
            files (dict, optional): The files for the request. Defaults to None.
            params (dict, optional): The parameters for the request. Defaults to None.

        Returns:
            requests.Response: The response from the server.
        """
        headers = {
            "x-access-token": self.access_token,
            "X-Requested-With": "XMLHttpRequest",
            "cf-access-token": os.environ.get("CF_TOKEN", "")}
        if files is None:
            headers["content-type"] = "application/json"

        response = requests.post(
            self.get_url(url),
            json=body,
            data=data,
            files=files,
            params=params,
            headers=headers,
        )
        return process_response(response)

    def put(
            self, url, body=None, data=None, files=None, params=None
    ) -> requests.Response:
        """
        A method to send a PUT request.

        Args:
            url (str): The URL for the request.
            body (dict, optional): The body for the request. Defaults to None.
            data (dict, optional): The data for the request. Defaults to None.
            files (dict, optional): The files for the request. Defaults to None.
            params (dict, optional): The parameters for the request. Defaults to None.

        Returns:
            requests.Response: The response from the server.
        """
        headers = {"x-access-token": self.access_token,
                   "cf-access-token": os.environ.get("CF_TOKEN", ""),
                   "X-Requested-With": "XMLHttpRequest"}
        if files is None:
            headers["content-type"] = "application/json"

        response = requests.put(
            self.get_url(url),
            json=body,
            data=data,
            files=files,
            params=params,
            headers=headers,
        )
        return process_response(response)

    def delete(self, url, params=None) -> requests.Response:
        """
        A method to send a DELETE request.

        Args:
            url (str): The URL for the request.
            params (dict, optional): The parameters for the request. Defaults to None.

        Returns:
            requests.Response: The response from the server.
        """
        response = requests.delete(
            self.get_url(url),
            params=params,
            headers={"x-access-token": self.access_token,
                     "cf-access-token": os.environ.get("CF_TOKEN", ""),
                     "X-Requested-With": "XMLHttpRequest"}
        )
        return process_response(response)

    def get_url(self, url):
        """
        A method to get the full URL.

        Args:
            url (str): The URL to append to the base URL.

        Returns:
            str: The full URL.
        """
        if url.startswith("/"):
            return self.base_url + url
        else:
            return self.base_url + "/" + url

    def export_project(self, project: ProjectEndpoint, export_path: str):
        """
        A method to export a project.

        Args:
            project (ProjectEndpoint): The project to export.
            export_path (str): The path to export the project to.
        """

        # We will create a directory for the project in the export path and then export the project
        # components and metadata to that directory

        # First export the project metadata

        project_export_dir = os.path.join(export_path, project.name)
        Path(project_export_dir).mkdir(parents=True, exist_ok=False)

        project_metadata_file = os.path.join(
            project_export_dir, "project_metadata.json"
        )
        with open(project_metadata_file, "w") as f:
            f.write(
                json.dumps(project.model_dump(mode="json", by_alias=True), indent=4)
            )

        for assistant in project.assistants.list():
            assistant_file = os.path.join(
                project_export_dir, f"assistant-{assistant.id}.json"
            )
            with open(assistant_file, "w") as f:
                f.write(
                    json.dumps(
                        assistant.model_dump(mode="json", by_alias=True), indent=4
                    )
                )

        for data_store in project.data_stores.list():
            data_store_file = os.path.join(
                project_export_dir,
                f"data-store-{data_store.slug}-{data_store.version}.json",
            )
            with open(data_store_file, "w") as f:
                f.write(
                    json.dumps(
                        data_store.model_dump(mode="json", by_alias=True), indent=4
                    )
                )

        for document_store in project.document_stores.list():
            document_store_file = os.path.join(
                project_export_dir,
                f"document-store-{document_store.slug}-{document_store.version}.json",
            )
            with open(document_store_file, "w") as f:
                f.write(
                    json.dumps(
                        document_store.model_dump(mode="json", by_alias=True), indent=4
                    )
                )

            store_folder = os.path.join(
                project_export_dir,
                f"document-store-{document_store.slug}-{document_store.version}",
            )
            Path(store_folder).mkdir(parents=True, exist_ok=False)
            document_store.download_document_families(store_folder)

        for model_store in project.model_stores.list():
            model_store_file = os.path.join(
                project_export_dir,
                f"model-store-{model_store.slug}-{model_store.version}.json",
            )
            with open(model_store_file, "w") as f:
                f.write(
                    json.dumps(
                        model_store.model_dump(mode="json", by_alias=True), indent=4
                    )
                )

            store_folder = os.path.join(
                project_export_dir,
                f"document-store-{model_store.slug}-{model_store.version}",
            )
            Path(store_folder).mkdir(parents=True, exist_ok=False)
            model_store.download_document_families(store_folder)

        for taxonomy in project.taxonomies.list():
            taxonomy_file = os.path.join(
                project_export_dir, f"taxonomy-{taxonomy.slug}-{taxonomy.version}.json"
            )
            with open(taxonomy_file, "w") as f:
                f.write(
                    json.dumps(
                        taxonomy.model_dump(mode="json", by_alias=True), indent=4
                    )
                )

        for guidance in project.guidance.list():
            guidance_file = os.path.join(
                project_export_dir, f"guidance-{guidance.slug}-{guidance.version}.json"
            )
            with open(guidance_file, "w") as f:
                f.write(
                    json.dumps(
                        guidance.model_dump(mode="json", by_alias=True), indent=4
                    )
                )

    def import_project(self, organization: OrganizationEndpoint, import_path: str):
        """
        A method to import a project.

        Args:
            organization (OrganizationEndpoint): The organization to import the project to.
            import_path (str): The path to import the project from.
        """
        # The import path is the directory containing the export (or a zip file containing the export)

        project_metadata_file = os.path.join(import_path, "project_metadata.json")
        with open(project_metadata_file, "r") as f:
            project = Project.model_validate(json.load(f))
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
                assistant: AssistantEndpoint = AssistantEndpoint.model_validate(
                    json.load(f)
                )

                assistant.assistant_definition_ref = assistant.definition.ref.split(
                    ":"
                )[0]
                new_project.assistants.create(assistant)

        for document_store_file in glob.glob(
                os.path.join(import_path, "document-store-*.json")
        ):
            with open(document_store_file, "r") as f:
                document_store = DocumentStoreEndpoint.model_validate(
                    json.load(f)
                ).set_client(self)
                document_store.org_slug = None
                document_store.ref = None
                document_store = organization.stores.create(document_store)
                stores.append(document_store)

                for doc_fam in glob.glob(
                        os.path.join(
                            import_path, document_store_file.replace(".json", "/*.dfm")
                        )
                ):
                    document_store.import_family(doc_fam)

        for data_store_file in glob.glob(
                os.path.join(import_path, "data-store-*.json")
        ):
            with open(data_store_file, "r") as f:
                data_store = DataStoreEndpoint.model_validate(json.load(f)).set_client(
                    self
                )
                data_store.org_slug = None
                data_store.ref = None
                data_store = organization.stores.create(data_store)
                stores.append(data_store)

        for model_store_file in glob.glob(
                os.path.join(import_path, "model-store-*.json")
        ):
            with open(model_store_file, "r") as f:
                model_store = ModelStoreEndpoint.model_validate(
                    json.load(f)
                ).set_client(self)
                model_store.org_slug = None
                model_store.ref = None
                model_store = organization.stores.create(model_store)
                stores.append(model_store)

                for doc_fam in glob.glob(
                        os.path.join(
                            import_path, model_store_file.replace(".json", "/*.dfm")
                        )
                ):
                    model_store.import_family(doc_fam)

        for taxonomy_file in glob.glob(os.path.join(import_path, "taxonomy-*.json")):
            with open(taxonomy_file, "r") as f:
                taxonomy = TaxonomyEndpoint.model_validate(json.load(f))
                taxonomy.org_slug = None
                taxonomy.ref = None
                taxonomies.append(organization.taxonomies.create(taxonomy))

        for guidance_file in glob.glob(os.path.join(import_path, "guidance-*.json")):
            with open(guidance_file, "r") as f:
                guidance = GuidanceSetEndpoint.model_validate(json.load(f))
                guidance.org_slug = None
                guidance.ref = None
                organization.guidance.create(guidance)

        import time

        time.sleep(4)

        new_project.update_resources(stores=stores, taxonomies=taxonomies)

    def deserialize(
            self, component_dict: dict, component_type: Optional[str] = None
    ) -> ComponentInstanceEndpoint:
        """
        A method to deserialize a component.

        Args:
            component_dict (dict): The dictionary to deserialize.
            component_type (str, optional): The type of the component. Defaults to None.

        Returns:
            ComponentInstanceEndpoint: The deserialized component.

        Raises:
            Exception: If the type is not found in the dictionary.
        """
        if "type" in component_dict or component_type is not None:
            component_type = (
                component_type if component_type is not None else component_dict["type"]
            )
            if component_type == "store":
                if "storeType" in component_dict:
                    store_type = component_dict["storeType"]
                    if store_type.lower() == "document":
                        document_store = DocumentStoreEndpoint.model_validate(
                            component_dict
                        )
                        document_store.set_client(self)

                        # We need special handling of the metadata
                        if (
                                "metadata" in component_dict
                                and component_dict["metadata"] is not None
                        ):
                            document_store.metadata = (
                                DocumentContentMetadata.model_validate(
                                    component_dict["metadata"]
                                )
                            )

                        return document_store
                    elif store_type.lower() == "model":
                        model_store = ModelStoreEndpoint.model_validate(component_dict)
                        model_store.set_client(self)

                        # We need special handling of the metadata
                        if (
                                "metadata" in component_dict
                                and component_dict["metadata"] is not None
                        ):
                            model_store.metadata = ModelContentMetadata.model_validate(
                                component_dict["metadata"]
                            )

                        return model_store
                    if store_type.lower() == "data" or store_type.lower() == "table":
                        return DataStoreEndpoint.model_validate(
                            component_dict
                        ).set_client(self)

                    raise Exception("Unknown store type: " + store_type)

                raise Exception("A store must have a storeType")

            from kodexa.model.entities.product import ProductEndpoint
            from kodexa.model.entities.product_subscription import ProductSubscriptionEndpoint
            from kodexa.model.entities.check_response import CheckResponseEndpoint
            known_components = {
                "taxonomy": TaxonomyEndpoint,
                "pipeline": PipelineEndpoint,
                "action": ActionEndpoint,
                "credential": CredentialDefinitionEndpoint,
                "projectTemplate": ProjectTemplateEndpoint,
                "modelRuntime": ModelRuntimeEndpoint,
                "extensionPack": ExtensionPackEndpoint,
                "user": UserEndpoint,
                "project": ProjectEndpoint,
                "membership": MembershipEndpoint,
                "documentFamily": DocumentFamilyEndpoint,
                "organization": OrganizationEndpoint,
                "dataForm": DataFormEndpoint,
                "dashboard": DashboardEndpoint,
                "execution": ExecutionEndpoint,
                "assistant": AssistantDefinitionEndpoint,
                "exception": DataExceptionEndpoint,
                "workspace": WorkspaceEndpoint,
                "message": MessageEndpoint,
                "prompt": PromptEndpoint,
                "guidance": GuidanceSetEndpoint,
                "retainedGuidance": RetainedGuidanceEndpoint,
                "channel": ChannelEndpoint,
                "product": ProductEndpoint,
                "task": TaskEndpoint,
                "productSubscription": ProductSubscriptionEndpoint,
                "checkResponse": CheckResponseEndpoint
            }

            if component_type in known_components:
                return (
                    known_components[component_type]
                    .model_validate(component_dict)
                    .set_client(self)
                )
            raise Exception("Unknown component type: " + component_type)

        raise Exception(
            f"Type not found in the dictionary, unable to deserialize ({component_type})"
        )

    def get_project(self, project_id) -> ProjectEndpoint:
        """
        A method to get a project by its ID.

        Args:
            project_id (str): The ID of the project.

        Returns:
            ProjectEndpoint: The project.
        """
        project = self.get(f"/api/projects/{project_id}")
        return ProjectEndpoint.model_validate(project.json()).set_client(self)

    def get_object_type(
            self, object_type, organization: Optional[OrganizationEndpoint] = None
    ) -> ClientEndpoint:
        """
        A method to get an object type.

        Args:
            object_type (str): The type of the object.
            organization (OrganizationEndpoint, optional): The organization. Defaults to None.

        Returns:
            ClientEndpoint: The object type.

        Raises:
            Exception: If the object type is unknown.
        """
        obj_type, obj_metadata = resolve_object_type(object_type)

        if "endpoint" in obj_metadata:
            if "global" in obj_metadata and obj_metadata["global"]:
                obj_inst = obj_metadata["endpoint"](self, organization)
            else:
                obj_inst = (
                    obj_metadata["endpoint"]()
                    .set_client(self)
                    .set_organization(organization)
                )

            return obj_inst

        raise Exception(f"Unknown object type: {object_type}")


MessageContext.model_rebuild()
MessageEndpoint.model_rebuild()
ClientEndpoint.model_rebuild()
DocumentStoreEndpoint.model_rebuild()
ModelStoreEndpoint.model_rebuild()
DataStoreEndpoint.model_rebuild()
TaxonomyEndpoint.model_rebuild()
PipelineEndpoint.model_rebuild()
ActionEndpoint.model_rebuild()
CredentialDefinitionEndpoint.model_rebuild()
ProjectTemplateEndpoint.model_rebuild()
ModelRuntimeEndpoint.model_rebuild()
ExtensionPackEndpoint.model_rebuild()
UserEndpoint.model_rebuild()
ProjectEndpoint.model_rebuild()
MembershipEndpoint.model_rebuild()
OrganizationEndpoint.model_rebuild()
DataFormEndpoint.model_rebuild()
DashboardEndpoint.model_rebuild()
ExecutionEndpoint.model_rebuild()
AssistantDefinitionEndpoint.model_rebuild()
DataExceptionEndpoint.model_rebuild()
WorkspaceEndpoint.model_rebuild()
DocumentFamilyStatistics.model_rebuild()
DocumentFamilyEndpoint.model_rebuild()
ClientEndpoint.model_rebuild()
