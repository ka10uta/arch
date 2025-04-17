from abc import ABC, abstractmethod

from app.application.usecase.user import CreateUserOutputData


class UserOutputPort(ABC):
    """ユーザー関連のプレゼンターインターフェース"""

    @abstractmethod
    def present_user(self, output_data: CreateUserOutputData) -> None:
        """ユーザー情報を表示する

        Args:
            output_data: 出力データ
        """
        raise NotImplementedError


class UserPresenter(UserOutputPort):
    """ユーザー関連のプレゼンター実装"""

    def present_user(self, output_data: CreateUserOutputData) -> None:
        """ユーザー情報を表示する

        Args:
            output_data: 出力データ
        """
        # ここでは特に何もしない（gRPCレスポンスは別途構築される）
        pass 