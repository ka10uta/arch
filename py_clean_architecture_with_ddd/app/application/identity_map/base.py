from abc import ABC
from typing import Generic, TypeVar
from uuid import UUID

from app.domain.entity.base import Entity

T = TypeVar("T", bound=Entity)


class IdentityMap(Generic[T], ABC):
    """IdentityMapパターンの基底クラス

    同一エンティティの複数インスタンス生成を防ぎ、整合性を保持します。
    UUIDをキーとしてエンティティを管理し、同一IDのエンティティの
    重複生成を防止します。

    型パラメータ:
        T: 管理対象のエンティティの型
    """

    def __init__(self) -> None:
        """新しいIdentityMapを初期化します。"""
        self._entities: dict[UUID, T] = {}

    def add(self, entity: T) -> None:
        """エンティティをマップに追加します。

        Args:
            entity: 追加するエンティティ
        """
        self._entities[entity.id] = entity

    def get(self, id: UUID) -> T | None:
        """IDによりエンティティを取得します。

        Args:
            id: 取得対象エンティティのID

        Returns:
            Optional[T]: 見つかった場合はエンティティ、見つからない場合はNone
        """
        return self._entities.get(id)

    def remove(self, id: UUID) -> None:
        """IDによりエンティティをマップから削除します。

        Args:
            id: 削除対象エンティティのID
        """
        if id in self._entities:
            del self._entities[id]

    def clear(self) -> None:
        """全てのエンティティをマップから削除します。"""
        self._entities.clear()

    def contains(self, id: UUID) -> bool:
        """指定されたIDのエンティティが存在するか確認します。

        Args:
            id: 確認対象エンティティのID

        Returns:
            bool: エンティティが存在する場合はTrue、そうでない場合はFalse
        """
        return id in self._entities

    def get_all(self) -> list[T]:
        """マップ内の全エンティティを取得します。

        Returns:
            list[T]: マップ内の全エンティティのリスト
        """
        return list(self._entities.values())
