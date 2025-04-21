from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.entity.user import User

# -- Command関連のデータクラスとインターフェース --

class CreateUserInputData(BaseModel):
    """ユーザー作成の入力データ"""
    model_config = ConfigDict(frozen=True)

    name: str
    email: str


class CreateUserOutputData(BaseModel):
    """ユーザー作成の出力データ"""
    model_config = ConfigDict(frozen=True)

    id: UUID
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "CreateUserOutputData":
        return cls(
            id=user.id,
            name=user.name.value,
            email=user.email.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UserCommandInputPort(ABC):
    """ユーザー関連のコマンド操作入力ポート

    CQRSパターンにおけるCommand責務を担当します。
    状態を変更する操作のみを提供します。
    """

    @abstractmethod
    async def create_user(self, input_data: CreateUserInputData) -> None:
        """ユーザーを新規作成する

        Args:
            input_data: ユーザー作成に必要な入力データ

        Raises:
            ValueError: ユーザー作成に失敗した場合
        """


class UserCommandOutputPort(ABC):
    """ユーザー関連のコマンド操作出力ポート"""

    @abstractmethod
    def present_user_created(self, output_data: CreateUserOutputData) -> None:
        """ユーザー作成結果を表示する

        Args:
            output_data: 作成されたユーザーの出力データ
        """


# -- Query関連のデータクラスとインターフェース --

class GetUserOutputData(BaseModel):
    """ユーザー取得の出力データ"""
    model_config = ConfigDict(frozen=True)

    id: UUID
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "GetUserOutputData":
        """ユーザーエンティティから出力データを生成

        Args:
            user: ユーザーエンティティ

        Returns:
            GetUserOutputData: 取得したユーザーの出力データ
        """
        return cls(
            id=user.id,
            name=user.name.value,
            email=user.email.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UserQueryInputPort(ABC):
    """ユーザー関連のクエリ操作入力ポート

    CQRSパターンにおけるQuery責務を担当します。
    状態を参照する操作のみを提供します。
    """

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> None:
        """IDによりユーザーを取得する

        Args:
            user_id: ユーザーID

        Raises:
            EntityNotFoundError: ユーザーが見つからない場合
        """

    @abstractmethod
    async def get_user_by_email(self, email: str) -> None:
        """メールアドレスによりユーザーを取得する

        Args:
            email: メールアドレス

        Raises:
            EntityNotFoundError: ユーザーが見つからない場合
        """


class UserQueryOutputPort(ABC):
    """ユーザー関連のクエリ操作出力ポート"""

    @abstractmethod
    def present_user_get(self, output_data: GetUserOutputData) -> None:
        """ユーザー取得結果を表示する

        Args:
            output_data: 取得したユーザーの出力データ
        """
