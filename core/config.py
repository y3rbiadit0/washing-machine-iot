from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Washing Machines - API"
    version: str = "v1"


@lru_cache
def settings() -> Settings:
    return Settings()
