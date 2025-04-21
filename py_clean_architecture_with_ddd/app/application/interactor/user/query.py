from logging import getLogger
from uuid import UUID

from pydantic import BaseModel

from app.application.identity_map.user import UserIdentityMap
from app.application.usecase.user import (
    GetUserOutputData,
    UserQueryInputPort,
    UserQueryOutputPort,
)
from app.domain.repository.user import ReadUserRepository

logger = getLogger(__name__)


class Repositories(BaseModel):
    """ユーザー関連のリポジトリ群"""
    user: ReadUserRepository
    # 必要に応じて他のリポジトリを追加
    # example: user_preferences: ReadUserRepository[UserPreference]

    class Config:
        arbitrary_types_allowed = True  # リポジトリインスタンスを許可


class UserQueryInteractor(UserQueryInputPort):
    """ユーザー関連のクエリ操作を実装するインタラクター

    CQRSパターンにおけるQuery責務を担当します。
    状態を参照する操作のみを提供します。
    """

    def __init__(
        self,
        repositories: Repositories,
        presenter: UserQueryOutputPort,
        identity_map: UserIdentityMap,
    ) -> None:
        """コンストラクタ

        Args:
            repositories: 読み取り用リポジトリ群
            presenter: クエリ操作の出力ポート
            identity_map: ユーザーIdentityMap
        """
        self.repositories = repositories
        self.presenter = presenter
        self._identity_map = identity_map

    async def get_user_by_id(self, user_id: UUID) -> None:
        """IDによるユーザー取得

        Args:
            user_id: ユーザーID

        Raises:
            EntityNotFoundError: ユーザーが見つからない場合
        """
        # まずIdentityMapから検索
        user = self._identity_map.get(user_id)
        if user:
            output_data = GetUserOutputData.from_entity(user)
            self.presenter.present_user_get(output_data)
            return

        # IdentityMapに存在しない場合はリポジトリから取得
        # ReadRepositoryを使用するのでトランザクション不要
        user = await self.repositories.user.find_by_id(user_id)

        # 出力データを作成し、プレゼンターに渡す
        output_data = GetUserOutputData.from_entity(user)
        self.presenter.present_user_get(output_data)


    async def get_user_by_email(self, email: str) -> None:
        """メールアドレスによるユーザー取得

        Args:
            email: メールアドレス

        Raises:
            EntityNotFoundError: ユーザーが見つからない場合
        """
        # まずIdentityMapから検索
        user = self._identity_map.get_by_email(email)
        if user:
            output_data = GetUserOutputData.from_entity(user)
            self.presenter.present_user_get(output_data)
            return

        # IdentityMapに存在しない場合はリポジトリから取得
        # ReadRepositoryを使用するのでトランザクション不要
        user = await self.repositories.user.find_by_email(email)

        # 出力データを作成し、プレゼンターに渡す
        output_data = GetUserOutputData.from_entity(user)
        self.presenter.present_user_get(output_data)

