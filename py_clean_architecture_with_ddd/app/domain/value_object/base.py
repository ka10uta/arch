from abc import ABC
from typing import Self

from pydantic import BaseModel, ConfigDict


class ValueObject(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    def equals(self, other: Self) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.model_dump() == other.model_dump()
