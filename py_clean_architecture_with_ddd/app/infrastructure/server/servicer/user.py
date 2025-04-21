import logging

import grpc
from injector import Injector

from app.iadapter.controller.user import UserController
from app.infrastructure.proto.v1.user.create_pb2 import CreateUserRequest, CreateUserResponse
from app.infrastructure.proto.v1.user.get_pb2 import GetUserRequest, GetUserResponse
from app.infrastructure.proto.v1.user.service_pb2_grpc import UserServiceServicer

from .extend import async_grpc_method

logger = logging.getLogger(__name__)



class UserServicer(UserServiceServicer):
    """ユーザー関連のgRPCサービサー実装"""

    def __init__(self, controller: UserController, injector: Injector | None = None) -> None:
        """コンストラクタ

        Args:
            controller: ユーザーコントローラー
            injector: DIコンテナ
        """
        self.controller = controller
        self.injector = injector

    @async_grpc_method("Error processing CreateUser request")
    async def CreateUser(
        self,
        request: CreateUserRequest,
        _context: grpc.ServicerContext,
    ) -> CreateUserResponse:
        """ユーザー作成エンドポイント(非同期)"""
        return await self.controller.create_user(request)

    @async_grpc_method("Error processing GetUser request")
    async def GetUser(
        self,
        request: GetUserRequest,
        _context: grpc.ServicerContext,
    ) -> GetUserResponse:
        """ユーザー取得エンドポイント(非同期)"""
        return await self.controller.get_user_by_id(request)

