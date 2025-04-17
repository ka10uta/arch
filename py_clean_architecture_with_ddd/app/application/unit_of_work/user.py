from abc import abstractmethod

from app.domain.entity.user import User
from app.domain.repository.base import WriteRepository

from .base import UnitOfWork


class UserUnitOfWork(UnitOfWork):
    """ユーザー関連の操作を管理するUnitOfWork"""

    @property
    @abstractmethod
    def users(self) -> WriteRepository[User]:
        """ユーザーリポジトリを取得します。"""
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> "UserUnitOfWork":
        """ユーザーリポジトリを取得します。"""
        raise NotImplementedError
