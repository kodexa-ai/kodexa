import json
from datetime import datetime
from typing import Optional, Annotated

from pydantic import BaseModel, Field, WithJsonSchema, PlainSerializer


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


StandardDateTime = Annotated[
    datetime,
    PlainSerializer(lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z', return_type=str),
    WithJsonSchema({'type': 'datetime'}, mode='serialization'),
]


class KodexaBaseModel(BaseModel):

    class Config:
        populate_by_name = True
        use_enum_values = True
        arbitrary_types_allowed = True
        protected_namespaces = ('model_config',)

    def to_dict(self, **kwargs):
        return json.loads(self.model_dump_json(by_alias=True, exclude={'client'}, **kwargs))


class BaseEntity(KodexaBaseModel):
    id: Optional[str] = Field(None, description='The ID of the object')
