from pydantic import BaseModel


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class KodexaBaseModel(BaseModel):
    class Config:
        use_enum_values = True
