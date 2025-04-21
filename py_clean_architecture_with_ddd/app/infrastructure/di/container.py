# mypy: disable-error-code="type-abstract"

from injector import Binder, Module, inject, singleton

from app.application.identity_map.user import UserIdentityMap
from app.application.interactor.user.command import UserCommandInteractor
from app.application.interactor.user.query import Repositories, UserQueryInteractor
from app.application.presenter.user import UserPresenterInterface
from app.application.unit_of_work.user import UserUnitOfWork
from app.application.usecase.user import (
    UserCommandOutputPort,
    UserQueryOutputPort,
)
from app.domain.repository.user import ReadUserRepository, WriteUserRepository
from app.iadapter.presenter.user import UserPresenter
from app.infrastructure.repository.user import ReadUserRepositoryImpl, WriteUserRepositoryImpl
from app.infrastructure.unit_of_work.user import UserUnitOfWorkImpl


class DIContainer(Module):
    def configure(self, binder: Binder) -> None:
        # Repositories
        binder.bind(ReadUserRepositoryImpl, to=ReadUserRepositoryImpl, scope=singleton)
        binder.bind(WriteUserRepositoryImpl, to=WriteUserRepositoryImpl, scope=singleton)
        binder.bind(WriteUserRepository, to=WriteUserRepositoryImpl, scope=singleton)
        binder.bind(ReadUserRepository, to=ReadUserRepositoryImpl, scope=singleton)

        # UnitOfWork
        binder.bind(
            UserUnitOfWork,
            to=self.configure_unit_of_work,
            scope=singleton,
        )

        # IdentityMap
        binder.bind(
            UserIdentityMap,
            to=UserIdentityMap,
            scope=singleton,
        )

        # Repositories group
        binder.bind(
            Repositories,
            to=self.configure_repositories,
            scope=singleton,
        )

        # Presenter - リクエストごとに新しいインスタンスを作成
        binder.bind(UserPresenter, to=UserPresenter)
        binder.bind(UserPresenterInterface, to=UserPresenter)
        binder.bind(UserCommandOutputPort, to=UserPresenter)
        binder.bind(UserQueryOutputPort, to=UserPresenter)

        # Command Interactor
        binder.bind(
            UserCommandInteractor,
            to=self.configure_user_command_interactor,
            scope=singleton,
        )
        # Query Interactor
        binder.bind(
            UserQueryInteractor,
            to=self.configure_user_query_interactor,
            scope=singleton,
        )

    @inject
    def configure_unit_of_work(
        self,
        users: WriteUserRepositoryImpl,
    ) -> UserUnitOfWork:
        return UserUnitOfWorkImpl(users=users)

    @inject
    def configure_repositories(
        self,
        user_repository: ReadUserRepository,
    ) -> Repositories:
        return Repositories(user=user_repository)

    @inject
    def configure_user_command_interactor(
        self,
        presenter: UserCommandOutputPort,
        uow: UserUnitOfWork,
        identity_map: UserIdentityMap,
        read_user_repository: ReadUserRepository,
    ) -> UserCommandInteractor:
        return UserCommandInteractor(
            presenter=presenter,
            uow=uow,
            identity_map=identity_map,
            read_user_repository=read_user_repository,
        )

    @inject
    def configure_user_query_interactor(
        self,
        repositories: Repositories,
        presenter: UserQueryOutputPort,
        identity_map: UserIdentityMap,
    ) -> UserQueryInteractor:
        return UserQueryInteractor(
            repositories=repositories,
            presenter=presenter,
            identity_map=identity_map,
        )
