from enum import StrEnum
from pydantic.types import SecretStr, PositiveInt
from pydantic import BeforeValidator, field_validator, ValidationInfo
from pydantic_settings import BaseSettings
from typing import Any
from typing_extensions import Annotated

class Role(StrEnum):
    READER = "reader"
    MODERATOR = "moderator"
    ADMIN = "admin"

def strip_raw(v: Any):
    if isinstance(v,str):
        print("Yes, it's a string!")
        v = v.strip()
    else:
        print("Nope, it's a {}!".format(type(v)))
    return v

strippedString = Annotated[str, BeforeValidator(strip_raw)]

class Settings(BaseSettings):
    username: strippedString
    password: SecretStr
    age: PositiveInt
    role: Role = Role.READER

    @field_validator("password","username", mode="after")
    @classmethod
    def validate_field_length(cls, v: str, info: ValidationInfo):
        if len(v) < 8:
            raise ValueError(f"The field {info.field_name} must have a length at least of 8 characters")
        return v

S = Settings()