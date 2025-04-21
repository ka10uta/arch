class InfrastructureError(Exception):
    """インフラストラクチャ層の基底例外クラス"""


class EntityNotFoundError(InfrastructureError):
    """エンティティが見つからない場合の例外"""
