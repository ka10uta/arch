import asyncio
import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, TypeVar

import grpc

from app.iadapter.presenter.user import UserPresenter

logger = logging.getLogger(__name__)

Request = TypeVar("Request")  # リクエスト型
Response = TypeVar("Response")  # レスポンス型


def async_grpc_method(error_message: str) -> Callable[
    [Callable[[Any, Any, grpc.ServicerContext], Awaitable[Any]]],
    Callable[[Any, Any, grpc.ServicerContext], Any],
]:
    """gRPCメソッドを非同期実行するデコレータ

    Args:
        error_message: エラー時のログメッセージ

    Returns:
        デコレータ関数
    """
    def decorator(
        func: Callable[[Any, Any, grpc.ServicerContext], Awaitable[Any]],
    ) -> Callable[[Any, Any, grpc.ServicerContext], Any]:
        """非同期gRPCメソッドをラップするデコレータ

        Args:
            func: 非同期gRPCメソッド

        Returns:
            同期的なgRPCハンドラー
        """
        @wraps(func)
        def wrapper(self: Any, request: Any, context: grpc.ServicerContext) -> Any:  # noqa: ANN401
            """非同期関数を同期的に実行するラッパー

            Args:
                self: サービサーインスタンス
                request: gRPCリクエスト
                context: gRPCコンテキスト

            Returns:
                gRPCレスポンス
            """
            # 新しいイベントループを作成して使用
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                if hasattr(self, "injector") and self.injector:
                    presenter = self.injector.get(UserPresenter)
                    self.controller.set_presenter(presenter)

                # 非同期関数を実行
                return loop.run_until_complete(func(self, request, context))
            except Exception as e:
                logger.exception(error_message)
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                # エラー時に適切な型の空のレスポンスを返す
                return_type = func.__annotations__.get("return")
                if return_type:
                    return return_type()
                return None
            finally:
                loop.close()
        return wrapper
    return decorator
