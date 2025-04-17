import asyncio

import grpc
from infrastructure.proto.v1.user import create_pb2, service_pb2_grpc

from app.iadapter.controller.user import UserController


class UserServicer(service_pb2_grpc.UserServiceServicer):
    def __init__(self, controller: UserController) -> None:
        self.controller = controller

    def CreateUser(
        self,
        request: create_pb2.CreateUserRequest,
        _context: grpc.ServicerContext,
    ) -> create_pb2.CreateUserResponse:
        """ユーザー作成エンドポイントの実装"""
        # 新しいイベントループを作成して使用
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.controller.create_user(request))
        finally:
            loop.close()

