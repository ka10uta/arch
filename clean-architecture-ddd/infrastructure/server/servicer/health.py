from infrastructure.proto.v1.health import service_pb2, service_pb2_grpc

class HealthServicer(service_pb2_grpc.HealthServicer):
    def HealthCheck(self, request, context):
        """ヘルスチェックエンドポイントの実装"""
        return service_pb2.HealthCheckResponse(
            status="OK"
        )