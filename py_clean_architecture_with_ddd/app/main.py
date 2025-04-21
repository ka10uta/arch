import logging
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection
from injector import Injector
from tortoise import Tortoise

from app.application.interactor.user.command import UserCommandInteractor
from app.application.interactor.user.query import UserQueryInteractor
from app.iadapter.controller.user import UserController
from app.iadapter.presenter.user import UserPresenter
from app.infrastructure.database import tortoise_config
from app.infrastructure.di.container import DIContainer
from app.infrastructure.proto.v1.health import service_pb2 as health_service_pb2
from app.infrastructure.proto.v1.health import service_pb2_grpc as health_service_pb2_grpc
from app.infrastructure.proto.v1.user import service_pb2 as user_service_pb2
from app.infrastructure.proto.v1.user import service_pb2_grpc as user_service_pb2_grpc
from app.infrastructure.server import interceptor, servicer


async def init_db() -> None:
    """データベースの初期化を行う関数"""
    await Tortoise.init(config=tortoise_config)
    # スキーマの生成
    await Tortoise.generate_schemas()

async def close_db() -> None:
    """データベース接続を閉じる関数"""
    await Tortoise.close_connections()

def serve() -> None:
    """gRPCサーバーを起動する関数"""
    # データベースの初期化
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_db())

    # DIコンテナの初期化
    injector = Injector([DIContainer()])

    # インタラクターを取得
    command_interactor = injector.get(UserCommandInteractor)
    query_interactor = injector.get(UserQueryInteractor)

    # Injectが常に新しいプレゼンターを作成する
    # 初期のコントローラー作成時は一時的にプレゼンターを作成
    user_controller = UserController(
        command_interactor=command_interactor,
        query_interactor=query_interactor,
        presenter=injector.get(UserPresenter),
    )

    # インターセプターを作成
    interceptors = [
        interceptor.VersionInterceptor(),
    ]

    # インターセプターを含めたサーバーの作成
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=interceptors,
    )
    health_service_pb2_grpc.add_HealthServiceServicer_to_server(
        servicer.HealthServicer(), server,
    )

    # UserServicerにはinjectをラップするサービサーを使用
    user_servicer = servicer.UserServicer(
        controller=user_controller,
        injector=injector,  # 各リクエスト処理ごとに新しいプレゼンターを取得するためinjectを渡す
    )
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        user_servicer, server,
    )

    # リフレクションサービスの追加
    service_names = (
        health_service_pb2.DESCRIPTOR.services_by_name["HealthService"].full_name,
        user_service_pb2.DESCRIPTOR.services_by_name["UserService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    logger.info("Server started successfully. Listening on port: 50051")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        # データベース接続を閉じる
        loop.run_until_complete(close_db())
        logger.warning("Server has been gracefully terminated.")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    serve()
