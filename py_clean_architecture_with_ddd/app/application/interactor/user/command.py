import asyncio
from datetime import datetime
from logging import getLogger
from uuid import uuid4
from zoneinfo import ZoneInfo

from app.application.identity_map.user import UserIdentityMap
from app.application.unit_of_work.user import UserUnitOfWork
from app.application.usecase.user import (
    CreateUserInputData,
    CreateUserOutputData,
    UserCommandInputPort,
    UserCommandOutputPort,
)
from app.domain.entity.user import User
from app.domain.repository.user import ReadUserRepository
from app.domain.value_object.user.email import Email
from app.domain.value_object.user.name import UserName

logger = getLogger(__name__)


class UserCommandInteractor(UserCommandInputPort):
    """ユーザー関連のコマンド操作を実装するインタラクター

    CQRSパターンにおけるCommand責務を担当します。
    状態を変更する操作のみを提供します。
    """

    def __init__(
        self,
        presenter: UserCommandOutputPort,
        uow: UserUnitOfWork,
        identity_map: UserIdentityMap,
        read_user_repository: ReadUserRepository,
    ) -> None:
        """コンストラクタ

        Args:
            presenter: コマンド操作の出力ポート
            uow: ユーザーUnitOfWork
            identity_map: ユーザーIdentityMap
        """
        self.presenter = presenter
        self._uow = uow
        self._identity_map = identity_map
        self._read_user_repository = read_user_repository
    async def create_user(self, input_data: CreateUserInputData) -> None:
        """ユーザーを新規作成するユースケース

        Args:
            input_data: ユーザー作成に必要な入力データ

        Raises:
            ValueError: 入力データに問題がある場合
        """
        if await self._read_user_repository.exists_by_email(input_data.email):
            msg = f"Email {input_data.email} is already created"
            raise ValueError(msg)

        # 重複チェック EmailによるIdentityMapからの検索
        # この段階では新規ユーザーなのでIdentityMapには存在しないはず
        if self._identity_map.get_by_email(input_data.email):
            msg = f"Email {input_data.email} is already in IdentityMap"
            raise ValueError(msg)

        # ドメインロジックの実行 Entityの作成 トランザクション外
        now = datetime.now(tz=ZoneInfo("Asia/Tokyo"))
        user = User(
            id=uuid4(),
            name=UserName(value=input_data.name),
            email=Email(value=input_data.email),
            created_at=now,
            updated_at=now,
        )

        # デモのための処理遅延 重い処理の例
        await asyncio.sleep(1)

        # UnitOfWork内でトランザクション処理
        async with self._uow as uow:
            # リポジトリに保存対象として登録
            # この段階でIdentityMapにも登録される
            saved_user = await uow.users.save(user)

        # トランザクション完了後の処理
        output_data = CreateUserOutputData.from_entity(saved_user)
        self.presenter.present_user_created(output_data)
