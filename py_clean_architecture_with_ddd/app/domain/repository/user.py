from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entity.user import User
from app.domain.value_object.user.email import Email


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: Email) -> User | None:
        raise NotImplementedError
