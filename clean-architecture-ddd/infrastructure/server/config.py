from functools import lru_cache
from pydantic import StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='server_')

    version: StrictStr = "v0.0.1"

@lru_cache
def get() -> Config:
    return Config()