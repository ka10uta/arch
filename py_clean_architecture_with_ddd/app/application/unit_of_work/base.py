from abc import ABC, abstractmethod
from types import TracebackType
from typing import TypeVar

T = TypeVar("T", bound="UnitOfWork")


class UnitOfWork(ABC):
    """作業単位を表現する抽象基底クラス。

    一連の操作をアトミックに実行することを保証します。
    全ての操作が成功した場合のみ変更が確定され、
    例外が発生した場合は全ての変更が取り消されます。
    """

    @abstractmethod
    async def __aenter__(self: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        raise NotImplementedError
