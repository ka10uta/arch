from app.application.usecase.user import (
    CreateUserOutputData,
    UserOutputPort,
)
from app.iadapter.controller.user import CreateUserResponse


class UserPresenter(UserOutputPort):
    def __init__(self) -> None:
        self.view_model: CreateUserResponse | None = None

    def present_user(self, output_data: CreateUserOutputData) -> None:
        self.view_model = CreateUserResponse(
            id=output_data.id,
            name=output_data.name,
            email=output_data.email,
            created_at=output_data.created_at,
            updated_at=output_data.updated_at,
        )
