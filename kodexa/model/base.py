from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class KodexaBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        json_encoders = {
            # custom output conversion for datetime (yyyy-MM-dd'T'HH:mm:ss.SSS'Z')
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        }


class BaseEntity(KodexaBaseModel):
    id: Optional[str] = Field(None, description='The ID of the object')
