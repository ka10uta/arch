import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.abc.idprovider.handler import IdPHandler
from app.impl.idprovider import handler as idp_handler

logging.basicConfig(
    level=logging.INFO,
    format=(
        '{'
        '"time": "%(asctime)s", '
        '"level": "%(levelname)s", '
        '"message": "%(message)s"'
        '}'
    ),
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)

logger = logging.getLogger(__name__)

app = FastAPI()

# HTTPBearerスキーマを使用
security = HTTPBearer()

# トークン検証のための依存関係
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    handler: Annotated[IdPHandler, Depends(idp_handler.get)],
) -> dict:
    token = credentials.credentials
    is_valid = await handler.validate_token(token)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="トークンが無効です",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await handler.get_user_info(token)

@app.get("/user-info")
async def get_user_info(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    return current_user
