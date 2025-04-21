import grpc

from app.infrastructure.proto.v1.health import service_pb2, service_pb2_grpc


class HealthServicer(service_pb2_grpc.HealthServiceServicer):
    def health_check(
        self,
        _request: service_pb2.HealthCheckRequest,
        _context: grpc.ServicerContext,
    ) -> service_pb2.HealthCheckResponse:
        """ヘルスチェックエンドポイントの実装"""
        return service_pb2.HealthCheckResponse(
            status="OK",
        )
