import re

from pydantic import field_validator

from app.domain.value_object.base import ValueObject
from app.domain.value_object.user.exceptions import InvalidEmailError


class Email(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not cls._is_valid_email(v):
            raise InvalidEmailError(v)
        return v

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
