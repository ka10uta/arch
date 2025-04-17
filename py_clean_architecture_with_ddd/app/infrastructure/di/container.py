# mypy: disable-error-code="type-abstract"
from typing import TYPE_CHECKING, Any, cast

from injector import Binder, Module, inject, singleton

from app.application.interactor.user import ReadRepositories, UserInteractor
from app.application.presenter.user import UserPresenter
from app.application.unit_of_work.user import UserUnitOfWork
from app.application.usecase.user import UserOutputPort
from app.domain.entity.user import User
from app.domain.repository.base import ReadRepository, WriteRepository
from app.infrastructure.repository.user import UserRepository
from app.infrastructure.unit_of_work.user import UserUnitOfWorkImpl

if TYPE_CHECKING:
    from contextlib import AbstractAsyncContextManager


class DIContainer(Module):
    def configure(self, binder: Binder) -> None:
        # Repositories
        binder.bind(UserRepository, to=UserRepository, scope=singleton)
        binder.bind(WriteRepository[User], to=UserRepository, scope=singleton)
        binder.bind(ReadRepository[User], to=UserRepository, scope=singleton)

        # UnitOfWork
        binder.bind(
            UserUnitOfWork,
            to=self.configure_unit_of_work,
            scope=singleton,
        )

        # Repositories group
        binder.bind(
            ReadRepositories,
            to=self.configure_repositories,
            scope=singleton,
        )

        # Presenter
        binder.bind(
            UserOutputPort,
            to=cast("type[UserOutputPort]", UserPresenter),
            scope=singleton,
        )

        # Interactors
        binder.bind(
            UserInteractor,
            to=self.configure_user_interactor,
            scope=singleton,
        )

    @inject
    def configure_unit_of_work(
        self,
        users: WriteRepository[User],
    ) -> UserUnitOfWork:
        return UserUnitOfWorkImpl(users=users)

    @inject
    def configure_repositories(
        self,
        user_repository: ReadRepository[User],
    ) -> ReadRepositories:
        return ReadRepositories(user=user_repository)

    @inject
    def configure_user_interactor(
        self,
        repositories: ReadRepositories,
        presenter: UserOutputPort,
        uow: UserUnitOfWork,
    ) -> UserInteractor:
        return UserInteractor(
            repositories=repositories,
            presenter=presenter,
            uow=uow,
        )
