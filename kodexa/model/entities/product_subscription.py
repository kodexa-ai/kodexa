from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from kodexa.model.base import StandardDateTime
from kodexa.model.entities.product import Product
from kodexa.model.objects import Organization
from kodexa.platform.client import EntityEndpoint, PageEndpoint, EntitiesEndpoint


class ProductSubscription(BaseModel):
    """
    A product subscription
    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )

    id: Optional[str] = Field(None)
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    product: Optional[Product] = None
    organization: Optional[Organization] = None


class ProductSubscriptionEndpoint(ProductSubscription, EntityEndpoint):
    """Handles the endpoint for a product subscription

    This class is a combination of ProductSubscription and EntityEndpoint. It is used
    to manage the endpoint for product subscriptions.

    Methods:
        get_type: Returns the type of the endpoint.
    """

    def get_type(self) -> str:
        """Gets the type of the endpoint.

        This method returns the type of the endpoint which is "product_subscriptions".

        Returns:
            str: The type of the endpoint.
        """
        return "productSubscription"


class PageProductSubscription(BaseModel):
    """
    A page of product subscriptions
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
    content: Optional[List[ProductSubscription]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageProductSubscriptionEndpoint(PageProductSubscription, PageEndpoint):
    def get_type(self) -> Optional[str]:
        return "productSubscription"


class ProductSubscriptionsEndpoint(EntitiesEndpoint):
    """Represents the product subscriptions endpoint

    This class is used to represent the product subscriptions endpoint in the system.

    Attributes:
        object_dict: A dictionary containing the object data.
    """

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint.

        Returns:
            str: The type of the endpoint.
        """
        return "productSubscriptions"

    def get_instance_class(self, object_dict=None):
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            ProductSubscriptionEndpoint: The instance class of the endpoint.
        """
        return ProductSubscriptionEndpoint

    def get_page_class(self, object_dict=None):
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            PageProductSubscriptionEndpoint: The page class of the endpoint.
        """
        return PageProductSubscriptionEndpoint
