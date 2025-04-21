from uuid import UUID

from app.application.identity_map.user import UserIdentityMap
from app.domain.entity.user import User
from app.domain.repository.user import ReadUserRepository, WriteUserRepository
from app.infrastructure.data_mapper.user import UserDataMapper
from app.infrastructure.database.model.user import UserModel
from app.infrastructure.exceptions import EntityNotFoundError


class ReadUserRepositoryImpl(ReadUserRepository):
    """Tortoise-ORMを使用した読み取り専用UserRepositoryの実装"""

    def __init__(self) -> None:
        self._identity_map = UserIdentityMap()
        self._data_mapper = UserDataMapper()

    @property
    def identity_map(self) -> UserIdentityMap:
        """IdentityMapへのアクセサ

        Returns:
            UserIdentityMap: ユーザーエンティティのIdentityMap
        """
        return self._identity_map

    @property
    def data_mapper(self) -> UserDataMapper:
        """DataMapperへのアクセサ

        Returns:
            UserDataMapper: ユーザーエンティティのDataMapper
        """
        return self._data_mapper

    async def find_by_id(self, id: UUID) -> User:
        """IDによるユーザーの取得

        Args:
            id: ユーザーID

        Returns:
            User: 取得したユーザーエンティティ

        Raises:
            EntityNotFoundError: ユーザーが見つからない場合
        """
        # IdentityMapから検索
        entity = self._identity_map.get(id)
        if entity:
            return entity

        # DBから検索
        model = await UserModel.get_or_none(id=id)
        if model is None:
            msg = f"User with id {id} not found"
            raise EntityNotFoundError(msg)

        # エンティティに変換してIdentityMapに登録
        entity = await self._data_mapper.to_entity(model)
        self._identity_map.add(entity)
        return entity

    async def find_by_email(self, email: str) -> User:
        """メールアドレスによるユーザーの取得

        Args:
            email: メールアドレス

        Returns:
            User: 取得したユーザーエンティティ

        Raises:
            EntityNotFoundError: ユーザーが見つからない場合
        """
        # IdentityMapから検索
        entity = self._identity_map.get_by_email(email)
        if entity:
            return entity

        # DBから検索
        model = await UserModel.get_or_none(email=email)
        if model is None:
            msg = f"User with email {email} not found"
            raise EntityNotFoundError(msg)

        # エンティティに変換してIdentityMapに登録
        entity = await self._data_mapper.to_entity(model)
        self._identity_map.add(entity)

        return entity

    async def exists_by_email(self, email: str) -> bool:
        """メールアドレスによるユーザーの存在確認

        Args:
            email: メールアドレス
        """
        # IdentityMapから検索
        entity = self._identity_map.get_by_email(email)
        if entity:
            return True

        return await UserModel.exists(email=email)


class WriteUserRepositoryImpl(WriteUserRepository):
    """Tortoise-ORMを使用した書き込み可能UserRepositoryの実装

    DataMapperパターンを活用し、トランザクション外で変更を蓄積し、
    UnitOfWorkによるトランザクション内で一括更新します。
    CQRSパターンに従い、読み取り操作は提供せず、書き込み操作のみを実装します。
    """

    def __init__(self, read_repository: ReadUserRepositoryImpl | None = None) -> None:
        self._read_repository = read_repository or ReadUserRepositoryImpl()
        self._identity_map = self._read_repository.identity_map
        self._data_mapper = self._read_repository.data_mapper
        # 変更対象のエンティティを追跡するコレクション
        self._pending_entities: dict[UUID, User] = {}

    async def save(self, user: User) -> User:
        """ユーザーの保存

        エンティティを保存対象として登録し、コミット時に一括で保存します。
        UnitOfWorkのトランザクション内でコミットメソッドが呼ばれることを前提としています。

        Args:
            user: 保存するユーザーエンティティ

        Returns:
            User: 保存対象のユーザーエンティティ
        """
        # 変更を追跡
        self._pending_entities[user.id] = user
        # IdentityMapにも追加/更新
        self._identity_map.add(user)
        return user

    async def commit(self) -> None:
        """保留中の変更をすべてデータベースに反映します。

        UnitOfWorkによるトランザクション内で呼び出されることを想定しています。
        """
        # 保留中のエンティティがなければ何もしない
        if not self._pending_entities:
            return

        # 各エンティティを処理し、低レベルSQLを使用してDBに反映
        # これによりsaveメソッドの内部コミットを回避
        for entity in self._pending_entities.values():
            # エンティティをDBモデルに変換
            model = await self._data_mapper.to_model(entity)

            # 既存レコードか新規レコードかを確認
            exists = await UserModel.exists(id=model.id)

            if exists:
                # 既存レコードの場合はUPDATE文を使用
                # Tortoise-ORMのbulk_updateを使用して明示的な更新
                await UserModel.filter(id=model.id).update(
                    name=model.name,
                    email=model.email,
                    updated_at=model.updated_at,
                )
            else:
                # 新規レコードの場合はINSERT文を使用
                # Tortoise-ORMのcreateを使用して明示的な作成
                await UserModel.create(
                    id=model.id,
                    name=model.name,
                    email=model.email,
                    created_at=model.created_at,
                    updated_at=model.updated_at,
                )

        # 後処理
        self._pending_entities.clear()

    def clear(self) -> None:
        """保留中の変更とIdentityMapをクリアします"""
        self._pending_entities.clear()
        self._identity_map.clear()

