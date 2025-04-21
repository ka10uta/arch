
from app.application.presenter.user import UserPresenterInterface
from app.application.usecase.user import (
    CreateUserOutputData,
    GetUserOutputData,
)
from app.infrastructure.proto.v1.user.create_pb2 import CreateUserResponse
from app.infrastructure.proto.v1.user.get_pb2 import GetUserResponse
from app.infrastructure.proto.v1.user.model_pb2 import User as ProtoUser


class UserPresenter(UserPresenterInterface):
    """ユーザー関連のプレゼンター実装

    CQRSパターンに従い、コマンド操作とクエリ操作の両方の出力ポートを実装します。
    アプリケーション層のインターフェースを実装し、具体的なレスポンスへの変換を担当します。
    """

    def __init__(self) -> None:
        """プレゼンターの初期化"""
        self._create_user_response: CreateUserResponse | None = None
        self._get_user_response: GetUserResponse | None = None

    def reset_responses(self) -> None:
        """レスポンスをリセットする"""
        self.reset_create_user_response()
        self.reset_get_user_response()

    def reset_create_user_response(self) -> None:
        """ユーザー作成レスポンスをリセットする"""
        self._create_user_response = None

    def reset_get_user_response(self) -> None:
        """ユーザー取得レスポンスをリセットする"""
        self._get_user_response = None

    @property
    def create_user_response(self) -> CreateUserResponse | None:
        """ユーザー作成レスポンスを取得する

        Returns:
            Optional[CreateUserResponse]: ユーザー作成レスポンス
        """
        return self._create_user_response

    @property
    def get_user_response(self) -> GetUserResponse | None:
        """ユーザー取得レスポンスを取得する

        Returns:
            Optional[GetUserResponse]: ユーザー取得レスポンス
        """
        return self._get_user_response

    def present_user_created(self, output_data: CreateUserOutputData) -> None:
        """ユーザー作成結果を表示する

        Args:
            output_data: 作成されたユーザーの出力データ
        """
        # アプリケーション層の出力データからgRPCレスポンスを構築
        self._create_user_response = CreateUserResponse(
            user=ProtoUser(
                id=str(output_data.id),
                name=output_data.name,
                email=output_data.email,
            ),
        )

    def present_user_get(self, output_data: GetUserOutputData) -> None:
        """ユーザー取得結果を表示する

        Args:
            output_data: 取得したユーザーの出力データ
        """
        # アプリケーション層の出力データからgRPCレスポンスを構築
        self._get_user_response = GetUserResponse(
            user=ProtoUser(
                id=str(output_data.id),
                name=output_data.name,
                email=output_data.email,
            ),
        )
