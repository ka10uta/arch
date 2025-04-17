from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Any, cast
from uuid import UUID

from tortoise import transactions

from app.domain.entity.user import User
from app.domain.repository.base import WriteRepository
from app.domain.value_object.user.email import Email
from app.domain.value_object.user.name import UserName
from app.infrastructure.database.model.user import UserModel


class UserRepository(WriteRepository[User]):
    """Tortoise-ORMを使用したUserRepositoryの実装"""

    def __init__(self, transaction_ctx: AbstractAsyncContextManager[Any] | None = None) -> None:
        self._transaction_ctx = transaction_ctx

    async def find_by_id(self, id: str) -> User:
        """IDによるユーザーの取得

        Args:
            id: ユーザーID

        Returns:
            User: 取得したユーザーエンティティ

        Raises:
            EntityNotFoundError: ユーザーが見つからない場合
        """
        user_model = await UserModel.get(id=UUID(id))
        return self._to_entity(user_model)

    async def save(self, user: User) -> User:
        """ユーザーの保存

        Args:
            user: 保存するユーザーエンティティ

        Returns:
            User: 保存されたユーザーエンティティ
        """
        if self._transaction_ctx is not None:
            # トランザクションコンテキストが存在する場合は、それを使用
            async with self._transaction_ctx:
                user_model = await UserModel.create(
                    id=user.id,
                    name=user.name.value,
                    email=user.email.value,
                )
        else:
            # トランザクションコンテキストが存在しない場合は、新しいトランザクションを作成
            async with transactions.in_transaction():
                user_model = await UserModel.create(
                    id=user.id,
                    name=user.name.value,
                    email=user.email.value,
                )

        return self._to_entity(user_model)

    def _to_entity(self, model: UserModel) -> User:
        """UserModelをUserエンティティに変換

        Args:
            model: 変換元のUserModel

        Returns:
            User: 変換後のUserエンティティ
        """
        return User(
            id=cast("UUID", model.id),
            name=UserName(value=model.name),
            email=Email(value=model.email),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
