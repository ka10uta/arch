from uuid import UUID

from app.domain.entity.user import User

from .base import IdentityMap


class UserIdentityMap(IdentityMap[User]):
    """ユーザーエンティティのIdentityMap

    ユーザーエンティティの一意性を保証し、メモリ内キャッシュとして機能します。
    UUIDだけでなく、メールアドレスによる検索もサポートします。
    """

    def __init__(self) -> None:
        """新しいUserIdentityMapを初期化します。"""
        super().__init__()
        self._email_index: dict[str, User] = {}

    def add(self, user: User) -> None:
        """ユーザーエンティティをマップに追加します。

        Args:
            user: 追加するユーザーエンティティ
        """
        super().add(user)
        # メールアドレスによるインデックスも更新
        self._email_index[user.email.value] = user

    def get_by_email(self, email: str) -> User | None:
        """メールアドレスによりユーザーエンティティを取得します。

        Args:
            email: ユーザーのメールアドレス

        Returns:
            Optional[User]: 見つかった場合はユーザーエンティティ、見つからない場合はNone
        """
        return self._email_index.get(email)

    def remove(self, id: UUID) -> None:
        """IDによりユーザーエンティティをマップから削除します。
        Args:
            id: 削除対象ユーザーエンティティのID
        """
        user = self.get(id)
        if user and user.email.value in self._email_index:
            # メールアドレスインデックスからも削除
            del self._email_index[user.email.value]
        super().remove(id)

    def clear(self) -> None:
        """全てのユーザーエンティティをマップから削除します。"""
        self._email_index.clear()
        super().clear()
