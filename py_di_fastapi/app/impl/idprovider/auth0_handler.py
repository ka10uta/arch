from logging import Logger, getLogger

from app.abc.idprovider.handler import IdPHandler

default_logger = getLogger(__name__)


class Auth0IdPHandler(IdPHandler):
    def __init__(self, logger: Logger = default_logger) -> None:
        self.logger = logger

    async def validate_token(self, _token: str) -> bool:
        self.logger.info("Auth0IdPの検証")
        return True

    async def get_user_info(self, _token: str) -> dict:
        self.logger.info("Auth0IdPのユーザー情報の取得")
        # 本来はIdPからトークンの中身を解析してユーザー情報を取得する
        # IdPのUserInfoエンドポイントを叩いてユーザー情報を取得することも可能
        return {"user_id": "dummy_user_id", "name": "Auth0IdPUserName"}
