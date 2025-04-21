from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from app.domain.entity.base import Entity

T = TypeVar("T", bound=Entity)

class ReadRepository(Generic[T], ABC):
    """読み取り専用リポジトリの基底クラス

    読み取り操作のみを提供するインターフェースです。
    CQRSパターンにおけるQueryの役割を担います。
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> T | None:
        """IDによるエンティティの取得

        Args:
            id: エンティティID

        Returns:
            エンティティまたはNone
        """
        raise NotImplementedError


class WriteRepository(Generic[T], ABC):
    """書き込み可能リポジトリの基底クラス

    書き込み操作のみを提供するインターフェースです。
    CQRSパターンにおけるCommandの役割を担います。
    """

    @abstractmethod
    async def save(self, entity: T) -> T:
        """エンティティの保存

        Args:
            entity: 保存するエンティティ

        Returns:
            保存されたエンティティ
        """
        raise NotImplementedError


class Repository(ReadRepository[T], WriteRepository[T], ABC):
    """リポジトリの基底クラス

    読み取りと書き込みの両方の操作を提供するインターフェースです。
    CQRSを厳密に適用しない場合に使用します。
    """
