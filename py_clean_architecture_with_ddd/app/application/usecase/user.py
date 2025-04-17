from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.entity.user import User


class CreateUserInputData(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    email: str


class CreateUserOutputData(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "CreateUserOutputData":
        return cls(
            id=user.id,
            name=user.name.value,
            email=user.email.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UserInputPort(ABC):
    @abstractmethod
    async def create_user(self, input_data: CreateUserInputData) -> CreateUserOutputData:
        pass


class UserOutputPort(ABC):
    @abstractmethod
    def present_user(self, output_data: CreateUserOutputData) -> None:
        pass
