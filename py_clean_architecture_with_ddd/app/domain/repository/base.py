from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class ReadRepository(Generic[T], ABC):
    """読み取り専用リポジトリの基底クラス"""

    @abstractmethod
    async def find_by_id(self, id: str) -> T:
        """IDによるエンティティの取得"""
        raise NotImplementedError


class WriteRepository(ReadRepository[T], ABC):
    """書き込み可能なリポジトリの基底クラス"""

    @abstractmethod
    async def save(self, entity: T) -> T:
        """エンティティの保存"""
        raise NotImplementedError
