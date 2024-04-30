from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field
from kodexa.model.base import StandardDateTime
from kodexa.platform.client import EntityEndpoint, PageEndpoint, EntitiesEndpoint


class Product(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A product
    """


    id: Optional[str] = None
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    name: str
    description: Optional[str] = None
    overview_markdown: Optional[str] = Field(None, alias="overviewMarkdown")


class ProductEndpoint(Product, EntityEndpoint):
    """Handles the endpoint for a product

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
        return "products"


class PageProduct(BaseModel):
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
    content: Optional[List[Product]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageProductEndpoint(PageProduct, PageEndpoint):
    def get_type(self) -> Optional[str]:
        return "product"


class ProductsEndpoint(EntitiesEndpoint):
    """Represents the products endpoint

    This class is used to represent the products endpoint in the system.

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
        return "products"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            AssistantEndpoint: The instance class of the endpoint.
        """
        return ProductEndpoint

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            PageAssistantEndpoint: The page class of the endpoint.
        """
        return PageProductEndpoint
