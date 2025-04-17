from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.value_object.user.email import Email
from app.domain.value_object.user.name import UserName


class User(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    name: UserName
    email: Email
    created_at: datetime
    updated_at: datetime

    @property
    def display_name(self) -> str:
        return self.name.display_name

    @property
    def email_address(self) -> str:
        return self.email.value
