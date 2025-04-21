from abc import ABC
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Entity(BaseModel, ABC):
    """エンティティの基底クラス"""
    model_config = ConfigDict(frozen=True)

    id: UUID
    created_at: datetime
    updated_at: datetime

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
