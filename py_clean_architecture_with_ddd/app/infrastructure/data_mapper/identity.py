from typing import Generic, TypeVar
from uuid import UUID

from app.domain.entity.base import Entity

T = TypeVar("T", bound=Entity)


class TortoiseIdentityMap(Generic[T]):
    """エンティティのIdentityMapを管理するクラス"""

    def __init__(self) -> None:
        self._entities: dict[UUID, T] = {}
        self._originals: dict[UUID, T] = {}

    def add(self, entity: T) -> None:
        """エンティティをIdentityMapに追加する"""
        self._entities[entity.id] = entity
        self._originals[entity.id] = entity.model_copy(deep=True)

    def get(self, entity_id: UUID) -> T | None:
        """エンティティIDからエンティティを取得する"""
        return self._entities.get(entity_id)

    def has_changes(self, entity: T) -> bool:
        """エンティティに変更があるかを確認する"""
        original = self._originals.get(entity.id)
        if original is None:
            # オリジナルがない場合は新規エンティティとみなす
            return True
        return original != entity

    def clear(self) -> None:
        """全てのエンティティをクリアする"""
        self._entities.clear()
        self._originals.clear()
