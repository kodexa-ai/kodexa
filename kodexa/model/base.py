from datetime import datetime

from pydantic import BaseModel


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class KodexaBaseModel(BaseModel):
    class Config:
        use_enum_values = True
        json_encoders = {
            # custom output conversion for datetime (yyyy-MM-dd'T'HH:mm:ss.SSS'Z')
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'
        }
