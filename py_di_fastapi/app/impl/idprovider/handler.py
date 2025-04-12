import os
from logging import getLogger

from app.abc.idprovider.handler import IdPHandler
from app.impl.idprovider.auth0_handler import Auth0IdPHandler
from app.impl.idprovider.azure_handler import AzureIdPHandler

logger = getLogger(__name__)

class IdPHandlerSingleton:
    _instance: IdPHandler | None = None

    @classmethod
    async def get_instance(cls) -> IdPHandler:
        if cls._instance is None:
            idp_type = os.getenv("ID_PROVIDER_TYPE")
            logger.info("Now selecting IdP")

            if idp_type == "azure":
                cls._instance = AzureIdPHandler()
            elif idp_type == "auth0":
                cls._instance = Auth0IdPHandler()
            else:
                message = f"Invalid IDP type: {idp_type}"
                raise ValueError(message)

        return cls._instance

async def get() -> IdPHandler:
    return await IdPHandlerSingleton.get_instance()
