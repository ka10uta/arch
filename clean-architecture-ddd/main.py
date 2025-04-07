import grpc
from concurrent import futures
import logging
from infrastructure.proto.v1.health import service_pb2
from infrastructure.proto.v1.health import service_pb2_grpc
from grpc_reflection.v1alpha import reflection

from infrastructure.server import interceptor
from infrastructure.server import servicer


def serve():
    """gRPCサーバーを起動する関数"""
    # インターセプターを作成
    interceptors = [
        interceptor.VersionInterceptor(),
    ]
    
    # インターセプターを含めたサーバーの作成
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=interceptors
    )
    service_pb2_grpc.add_HealthServicer_to_server(
        servicer.HealthServicer(), server
    )
    
    # リフレクションサービスの追加
    SERVICE_NAMES = (
        service_pb2.DESCRIPTOR.services_by_name['Health'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Server started successfully. Listening on port: 50051")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        logger.warning("Server has been gracefully terminated.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    serve()