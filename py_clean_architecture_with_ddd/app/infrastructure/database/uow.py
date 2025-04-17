from types import TracebackType

from tortoise import transactions

from app.application.unit_of_work.user import UserUnitOfWork
from app.domain.entity.user import User
from app.domain.repository.base import WriteRepository
from app.infrastructure.repository.user import UserRepository


class TortoiseUserUnitOfWork(UserUnitOfWork):
    """Tortoise-ORMを使用したユーザー用UnitOfWork実装"""

    def __init__(self) -> None:
        self._context: transactions.TransactionContext | None = None
        self._users: WriteRepository[User] | None = None

    @property
    def users(self) -> WriteRepository[User]:
        if self._users is None:
            msg = "UnitOfWorkのコンテキスト外でリポジトリにアクセスしようとしました"
            raise RuntimeError(msg)
        return self._users

    async def __aenter__(self) -> "UserUnitOfWork":
        self._context = transactions.in_transaction()
        await self._context.__aenter__()
        self._users = UserRepository(self._context)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not self._context:
            return

        try:
            if exc_type is not None:
                await self._context.__aexit__(Exception("トランザクションはロールバックされました"), None, None)
            else:
                await self._context.__aexit__(None, None, None)
        finally:
            self._users = None
