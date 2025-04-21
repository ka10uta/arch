from collections.abc import Callable

import grpc

from app.infrastructure.server import config as server_config


class VersionInterceptor(grpc.ServerInterceptor):
    def __init__(self) -> None:
        self.config = server_config.get()

    def intercept_service(
        self,
        continuation: Callable,
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        handler = continuation(handler_call_details)

        if handler and handler.unary_unary:
            return grpc.unary_unary_rpc_method_handler(
                self._wrap_unary_response_with_version(handler.unary_unary),
                handler.request_deserializer,
                handler.response_serializer,
            )
        return handler

    def _wrap_unary_response_with_version(self, handler_fn: Callable) -> Callable:
        def new_handler(request: object, servicer_context: grpc.ServicerContext) -> object:
            response = handler_fn(request, servicer_context)
            # メタデータにバージョン情報を追加
            servicer_context.set_trailing_metadata((
                ("version", self.config.version),
            ))
            return response
        return new_handler
