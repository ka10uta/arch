from abc import ABC, abstractmethod


class IdPHandler(ABC):
    @abstractmethod
    async def validate_token(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_user_info(self, user_id: str) -> dict:
        raise NotImplementedError
