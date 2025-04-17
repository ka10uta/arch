from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Any

from tortoise import transactions

from app.application.unit_of_work.user import UserUnitOfWork
from app.domain.entity.user import User
from app.domain.repository.base import WriteRepository


class UserUnitOfWorkImpl(UserUnitOfWork):
    def __init__(self, users: WriteRepository[User]) -> None:
        self._users = users
        self._transaction_ctx: AbstractAsyncContextManager[Any] | None = None

    @property
    def users(self) -> WriteRepository[User]:
        return self._users

    async def __aenter__(self) -> "UserUnitOfWorkImpl":
        self._transaction_ctx = transactions.in_transaction()
        await self._transaction_ctx.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._transaction_ctx:
            await self._transaction_ctx.__aexit__(exc_type, exc_val, exc_tb)
