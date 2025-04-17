from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from pydantic import BaseModel

from app.application.unit_of_work.user import UserUnitOfWork
from app.application.usecase.user import (
    CreateUserInputData,
    CreateUserOutputData,
    UserInputPort,
    UserOutputPort,
)
from app.domain.entity.user import User
from app.domain.repository.base import ReadRepository
from app.domain.repository.user import UserRepository
from app.domain.value_object.user.email import Email
from app.domain.value_object.user.name import UserName


class ReadRepositories(BaseModel):
    """ユーザー関連のリポジトリ群"""
    user: ReadRepository[User]
    # 必要に応じて他のリポジトリを追加
    # example: user_preferences: ReadRepository[UserPreference]

    class Config:
        arbitrary_types_allowed = True  # リポジトリインスタンスを許可

class UserInteractor(UserInputPort):
    def __init__(self, repositories: ReadRepositories, presenter: UserOutputPort, uow: UserUnitOfWork) -> None:
        self.repositories = repositories
        self.presenter = presenter
        self._uow = uow

    async def create_user(self, input_data: CreateUserInputData) -> CreateUserOutputData:
        now = datetime.now(tz=ZoneInfo("Asia/Tokyo"))
        user = User(
            id=uuid4(),
            name=UserName(value=input_data.name),
            email=Email(value=input_data.email),
            created_at=now,
            updated_at=now,
        )

        uow: UserUnitOfWork
        async with self._uow as uow:
            saved_user = await uow.users.save(user)
        output_data = CreateUserOutputData.from_entity(saved_user)
        self.presenter.present_user(output_data)
        return output_data
