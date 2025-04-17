class DomainError(Exception):
    """ドメイン層の基底例外クラス"""


class InvalidValueObjectError(DomainError):
    """ValueObjectが無効な値を持つ場合の例外"""
