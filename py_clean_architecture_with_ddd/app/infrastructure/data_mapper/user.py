from uuid import UUID

from app.domain.data_mapper.base import DataMapper
from app.domain.entity.user import User
from app.domain.value_object.user.email import Email
from app.domain.value_object.user.name import UserName
from app.infrastructure.database.model.user import UserModel


class UserDataMapper(DataMapper[User, UserModel]):
    """ユーザーエンティティとデータベースモデル間の変換を担当するデータマッパー

    DataMapperパターンの実装として、エンティティとデータベースモデルの
    変換ロジックをカプセル化します。
    """

    async def to_entity(self, model: UserModel) -> User:
        """データベースモデルからドメインエンティティへの変換

        Args:
            model: 変換元のデータベースモデル

        Returns:
            変換されたドメインエンティティ
        """
        return User(
            id=UUID(str(model.id)),
            name=UserName(value=model.name),
            email=Email(value=model.email),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def to_model(self, entity: User) -> UserModel:
        """ドメインエンティティからデータベースモデルへの変換

        トランザクション内で呼び出されることを想定しています。
        既存モデルの検索と更新、または新規モデルの作成を行いますが、
        実際の保存(save)操作は呼び出し元で実行します。

        Args:
            entity: 変換元のドメインエンティティ

        Returns:
            変換されたデータベースモデル(保存はまだされていない)
        """
        # 既存のモデルを検索
        model = await UserModel.get_or_none(id=entity.id)

        if model is None:
            # 新規作成の場合
            model = UserModel(
                id=entity.id,
                name=entity.name.value,
                email=entity.email.value,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )
        else:
            # 更新の場合
            model.name = entity.name.value
            model.email = entity.email.value
            model.updated_at = entity.updated_at

        return model
