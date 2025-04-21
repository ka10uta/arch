from abc import ABC

from app.application.usecase.user import (
    UserCommandOutputPort,
    UserQueryOutputPort,
)


class UserPresenterInterface(UserCommandOutputPort, UserQueryOutputPort, ABC):
    """ユーザー関連のプレゼンターインターフェース

    CQRSパターンに従い、コマンド操作とクエリ操作の両方の出力ポートを実装します。
    抽象クラスとして定義し、実際の実装はiadapterレイヤーで行います。
    """
    # 抽象メソッドは親クラスのUserCommandOutputPortとUserQueryOutputPortで定義済み
