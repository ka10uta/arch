from pydantic import ConfigDict

from app.domain.value_object.user.email import Email
from app.domain.value_object.user.name import UserName

from .base import Entity


class User(Entity):
    model_config = ConfigDict(frozen=True)

    name: UserName
    email: Email

    @property
    def display_name(self) -> str:
        return self.name.display_name

    @property
    def email_address(self) -> str:
        return self.email.value
