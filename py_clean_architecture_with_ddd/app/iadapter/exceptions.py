class InterfaceAdapterError(Exception):
    """インターフェースアダプターの基底例外クラス"""


class PresenterResponseIsNoneError(InterfaceAdapterError):
    """プレゼンターのレスポンスがNoneの場合の例外"""
