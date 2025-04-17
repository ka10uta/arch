from app.application.interactor.user import UserInteractor
from app.application.usecase.user import CreateUserInputData, CreateUserOutputData
from app.infrastructure.proto.v1.user.create_pb2 import CreateUserRequest, CreateUserResponse
from app.infrastructure.proto.v1.user.model_pb2 import User as ProtoUser


class UserController:
    def __init__(self, interactor: UserInteractor) -> None:
        self._interactor = interactor

    async def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        """ユーザーを作成する

        Args:
            request (CreateUserRequest): gRPCリクエスト

        Returns:
            CreateUserResponse: gRPCレスポンス
        """
        # 入力データを作成
        input_data = CreateUserInputData(
            name=request.user.name,
            email=request.user.email,
        )

        # ユースケースを実行
        output_data = await self._interactor.create_user(input_data)

        # レスポンスを作成して返す
        return CreateUserResponse(
            user=ProtoUser(
                id=str(output_data.id),
                name=output_data.name,
                email=output_data.email,
            ),
        )
