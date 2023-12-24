import json
from datetime import datetime
from typing import Optional, Annotated

from pydantic import BaseModel, Field, WithJsonSchema, PlainSerializer, ConfigDict


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


StandardDateTime = Annotated[
    datetime,
    PlainSerializer(
        lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z" if not isinstance(v,str) else v, return_type=str
    ),
    WithJsonSchema({"type": "datetime"}, mode="serialization"),
]