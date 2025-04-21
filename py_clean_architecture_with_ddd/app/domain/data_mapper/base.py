from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from tortoise import Model

from app.domain.entity.base import Entity

T = TypeVar("T", bound=Entity)
M = TypeVar("M", bound=Model)

class DataMapper(Generic[T, M], ABC):
    """DataMapperパターンの基底インターフェース

    ドメインエンティティとデータベースモデル間の変換を担当します。
    この抽象クラスを実装することで、永続化の詳細からドメインモデルを
    分離し、単一責任の原則を保ちます。

    型パラメータ:
        T: ドメインエンティティの型
        M: データベースモデルの型
    """

    @abstractmethod
    async def to_entity(self, model: M) -> T:
        """データベースモデルからドメインエンティティへの変換

        Args:
            model: 変換元のデータベースモデル

        Returns:
            変換されたドメインエンティティ
        """
        raise NotImplementedError

    @abstractmethod
    async def to_model(self, entity: T) -> M:
        """ドメインエンティティからデータベースモデルへの変換

        トランザクション内で呼び出されることを想定しています。

        Args:
            entity: 変換元のドメインエンティティ

        Returns:
            変換されたデータベースモデル(保存はまだされていない)
        """
        raise NotImplementedError
