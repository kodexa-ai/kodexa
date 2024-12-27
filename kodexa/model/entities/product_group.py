from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field
from kodexa.model.base import StandardDateTime
from kodexa.platform.client import EntityEndpoint, PageEndpoint, EntitiesEndpoint


class ProductGroup(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A product group
    """


    id: Optional[str] = None
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    name: str
    description: Optional[str] = None
    overview_markdown: Optional[str] = Field(None, alias="overviewMarkdown")


class ProductGroupEndpoint(ProductGroup, EntityEndpoint):
    """Handles the endpoint for a product group

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
        return "product-groups"


class PageProductGroup(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[ProductGroup]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageProductGroupEndpoint(PageProductGroup, PageEndpoint):
    def get_type(self) -> Optional[str]:
        return "product-group"


class ProductGroupsEndpoint(EntitiesEndpoint):
    """Represents the product groups endpoint

    This class is used to represent the product groups endpoint in the system.

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
        return "product-groups"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            AssistantEndpoint: The instance class of the endpoint.
        """
        return ProductGroupEndpoint

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            PageAssistantEndpoint: The page class of the endpoint.
        """
        return PageProductGroupEndpoint