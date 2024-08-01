from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field
from kodexa.model.base import StandardDateTime
from kodexa.model.objects import User
from kodexa.platform.client import EntityEndpoint, PageEndpoint, EntitiesEndpoint

from enum import Enum


class CheckStatus(Enum):
    """ Check Status ENUM: OPEN, CLOSED, IN_PROGRESS """
    open = "OPEN"
    closed = "CLOSED"
    in_progress = "IN_PROGRESS"


class CheckResponse(BaseModel):
    """
    Entity of check response
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
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CheckStatus] = None
    confidence: Optional[float] = None
    approver: Optional[User] = None


class PageCheckResponse(BaseModel):
    """
        A page pydantic for check response
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
    content: Optional[List[CheckResponse]] = None
    number: Optional[int] = None
    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageCheckResponseEndpoint(PageCheckResponse, PageEndpoint):
    """
        Represents a page check response endpoint

        This class is used to represent the endpoints of a page check response. It inherits from
        the PageCheckResponse and PageEndpoint classes.

        Methods:
            get_type: Returns the type of the endpoint.
    """

    def get_type(self) -> str:
        """Get the type of the endpoint

        This method is used to get the type of the endpoint. In this case, it will always
        return "workspace".

        Returns:
            str: The type of the endpoint, "workspace".
        """
        return "checkResponse"


class CheckResponseEndpoint(CheckResponse, EntityEndpoint):
    """Represents a Check Response endpoint"""

    def get_type(self) -> str:
        """
        Get the type of endpoint

        :return: The type of endpoint
        """
        return "checkResponses"


class CheckResponsesEndpoint(EntitiesEndpoint):
    """ Represents check responses endpoint """

    def get_type(self) -> str:
        """
            Get the type of endpoint
        :return: The type of endpoint
        """
        return "checkResponses"

    def get_instance_class(self, object_dict=None) -> CheckResponseEndpoint:
        """Get the instance class of the endpoint

        This method is used to get the instance class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            CheckResponseEndpoint: The instance class of the endpoint.
        """
        return CheckResponseEndpoint

    def get_page_class(self, object_dict=None) -> PageCheckResponseEndpoint:
        """Get the page class of the endpoint

        This method is used to get the page class of the endpoint.

        Args:
            object_dict (dict, optional): A dictionary containing the object data.

        Returns:
            PageCheckResponseEndpoint: The page class of the endpoint.
        """
        return PageCheckResponseEndpoint
