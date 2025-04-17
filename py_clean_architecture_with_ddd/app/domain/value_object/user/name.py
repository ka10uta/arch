from pydantic import field_validator

from app.domain.value_object.base import ValueObject
from app.domain.value_object.user.exceptions import InvalidUserNameError

MIN_LENGTH = 2
MAX_LENGTH = 50


class UserName(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not cls._is_valid_username(v):
            raise InvalidUserNameError(v)
        return v

    @staticmethod
    def _is_valid_username(name: str) -> bool:
        if not name:
            return False
        return not (len(name) < MIN_LENGTH or len(name) > MAX_LENGTH)

    @property
    def display_name(self) -> str:
        """表示用の名前を返します"""
        return self.value.title()
