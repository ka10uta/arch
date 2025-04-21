import logging
from uuid import UUID

from app.application.interactor.user.command import UserCommandInteractor
from app.application.interactor.user.query import UserQueryInteractor
from app.application.usecase.user import CreateUserInputData
from app.iadapter.exceptions import PresenterResponseIsNoneError
from app.iadapter.presenter.user import UserPresenter
from app.infrastructure.proto.v1.user.create_pb2 import CreateUserRequest, CreateUserResponse
from app.infrastructure.proto.v1.user.get_pb2 import GetUserRequest, GetUserResponse

logger = logging.getLogger(__name__)


class UserController:
    """ユーザー関連のコントローラー

    CQRSパターンに従い、コマンド操作とクエリ操作のインタラクターを
    それぞれ保持し、適切な操作に対応します。
    プレゼンターを使用してビューへの変換を行います。
    """

    def __init__(
        self,
        command_interactor: UserCommandInteractor,
        query_interactor: UserQueryInteractor,
        presenter: UserPresenter,
    ) -> None:
        """コンストラクタ

        Args:
            command_interactor: コマンド操作のインタラクター
            query_interactor: クエリ操作のインタラクター
            presenter: プレゼンター
        """
        self._command_interactor = command_interactor
        self._query_interactor = query_interactor
        self._presenter = presenter

        # インタラクターのプレゼンターを設定
        self._command_interactor.presenter = self._presenter
        self._query_interactor.presenter = self._presenter

    def set_presenter(self, presenter: UserPresenter) -> None:
        """プレゼンターを設定する

        Args:
            presenter: 新しいプレゼンター
        """
        self._presenter = presenter
        self._command_interactor.presenter = presenter
        self._query_interactor.presenter = presenter

    async def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        """ユーザーを作成する

        Args:
            request (CreateUserRequest): gRPCリクエスト

        Returns:
            CreateUserResponse: gRPCレスポンス

        Raises:
            PresenterResponseIsNoneError: プレゼンターがレスポンスを作成しなかった場合
            Exception: その他の例外
        """
        # リクエスト前にプレゼンターの状態をリセット
        self._presenter.reset_create_user_response()

        # 入力データを作成
        input_data = CreateUserInputData(
            name=request.user.name,
            email=request.user.email,
        )

        # コマンドインタラクターでユースケースを実行
        # インタラクターは内部でプレゼンターにデータを渡す
        await self._command_interactor.create_user(input_data)

        # プレゼンターからレスポンスを取得して返す
        if self._presenter.create_user_response is None:
            msg = "Presenter did not create a response"
            raise PresenterResponseIsNoneError(msg)

        return self._presenter.create_user_response

    async def get_user_by_id(self, request: GetUserRequest) -> GetUserResponse:
        """IDによりユーザーを取得する

        Args:
            request (GetUserRequest): gRPCリクエスト

        Returns:
            GetUserResponse: gRPCレスポンス

        Raises:
            PresenterResponseIsNoneError: プレゼンターがレスポンスを作成しなかった場合
            Exception: その他の例外
        """
        # リクエスト前にプレゼンターの状態をリセット
        self._presenter.reset_get_user_response()

        # ユーザーIDを取得
        user_id = UUID(request.id)

        # クエリインタラクターでユースケースを実行
        # インタラクターは内部でプレゼンターにデータを渡す
        await self._query_interactor.get_user_by_id(user_id)

        # プレゼンターからレスポンスを取得して返す
        if self._presenter.get_user_response is None:
            msg = "Presenter did not create a response"
            raise PresenterResponseIsNoneError(msg)

        return self._presenter.get_user_response
