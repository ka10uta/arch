# mypy: disable-error-code="attr-defined,assignment"
from types import TracebackType
from typing import TYPE_CHECKING, Any, Self

from tortoise.transactions import in_transaction

from app.application.unit_of_work.user import UserUnitOfWork
from app.infrastructure.repository.user import WriteUserRepositoryImpl

if TYPE_CHECKING:
    from contextlib import AbstractAsyncContextManager


class UserUnitOfWorkImpl(UserUnitOfWork):
    """ユーザー関連の操作を扱うUnitOfWorkの実装

    トランザクション管理を担当し、データの整合性を保証します。
    DataMapperパターンと連携し、リポジトリで蓄積された変更を
    トランザクション内で一括コミットします。
    IdentityMapパターンと連携してエンティティの一意性を保証します。
    """

    def __init__(self, users: WriteUserRepositoryImpl) -> None:
        """コンストラクタ

        Args:
            users: ユーザーリポジトリの実装
        """
        self._users = users
        self._transaction_ctx: AbstractAsyncContextManager[Any] | None = None

    @property
    def users(self) -> WriteUserRepositoryImpl:
        """ユーザーリポジトリを取得します

        Returns:
            WriteUserRepositoryImpl: 書き込み可能なユーザーリポジトリ
        """
        return self._users

    async def __aenter__(self) -> Self:
        """トランザクションを開始します

        UnitOfWorkパターンの重要な部分として、この時点でデータベーストランザクションを
        開始します。これにより、複数の操作をアトミックに実行できます。

        Returns:
            Self: このUnitOfWorkインスタンス
        """
        # トランザクションコンテキストを作成して開始
        self._transaction_ctx = in_transaction()
        await self._transaction_ctx.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """トランザクションを終了します

        リポジトリで蓄積された変更をトランザクション内でコミットし、
        例外が発生した場合はロールバック、そうでなければコミットします。
        トランザクション終了後、IdentityMapをクリアして次の操作の準備をします。

        Args:
            exc_type: 例外の型
            exc_val: 例外のインスタンス
            exc_tb: トレースバック情報
        """
        try:
            # 例外が発生していない場合に限り、リポジトリの変更をコミット
            if exc_type is None:
                try:
                    # トランザクション終了前に明示的にリポジトリのコミットを呼び出す
                    await self._users.commit()
                except Exception as e:
                    # コミット時に例外が発生した場合も確実にトランザクションを終了
                    # ロールバックを明示的に行うため例外を再度投げる
                    if self._transaction_ctx:
                        await self._transaction_ctx.__aexit__(type(e), e, e.__traceback__)
                    # 後続の処理のために例外を再度発生させる
                    raise

            # トランザクションを終了
            if self._transaction_ctx:
                await self._transaction_ctx.__aexit__(exc_type, exc_val, exc_tb)
        finally:
            # 常にリポジトリのクリアを呼び出し、IdentityMapもクリアする
            self._users.clear()

            # トランザクションコンテキストをクリア
            self._transaction_ctx = None
