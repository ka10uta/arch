from abc import abstractmethod

from app.domain.repository.user import WriteUserRepository

from .base import UnitOfWork


class UserUnitOfWork(UnitOfWork):
    """ユーザー関連の操作を管理するUnitOfWork"""

    @property
    @abstractmethod
    def users(self) -> WriteUserRepository:
        """ユーザーリポジトリを取得します。"""
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> "UserUnitOfWork":
        """ユーザーリポジトリを取得します。"""
        raise NotImplementedError
