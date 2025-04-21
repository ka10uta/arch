from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entity.user import User
from app.domain.repository.base import ReadRepository, WriteRepository


class ReadUserRepository(ReadRepository[User], ABC):
    """読み取り専用のユーザーリポジトリインターフェース

    CQRSパターンにおけるQuery責務を担当します。
    読み取り操作のみを提供し、状態の変更は行いません。
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> User:
        """IDによるユーザーの取得

        Args:
            id: ユーザーID

        Returns:
            User: 取得したユーザーエンティティ

        Raises:
            EntityNotFoundError: ユーザーが見つからない場合
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(self, email: str) -> User:
        """メールアドレスによるユーザーの取得

        Args:
            email: メールアドレス

        Returns:
            User: 取得したユーザーエンティティ

        Raises:
            EntityNotFoundError: ユーザーが見つからない場合
        """
        raise NotImplementedError

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """メールアドレスによるユーザーの存在確認

        Args:
            email: メールアドレス
        """
        raise NotImplementedError

class WriteUserRepository(WriteRepository[User], ABC):
    """書き込み可能なユーザーリポジトリインターフェース

    CQRSパターンにおけるCommand責務を担当します。
    状態を変更する操作のみを提供し、読み取り操作は行いません。
    """

    @abstractmethod
    async def save(self, user: User) -> User:
        """ユーザーの保存

        Args:
            user: 保存するユーザーエンティティ

        Returns:
            User: 保存されたユーザーエンティティ
        """
        raise NotImplementedError
