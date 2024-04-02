from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    MQTT_SERVER_IP: str = "192.168.1.21"
    MQTT_SERVER_PORT: str = "1883"
    MONGO_URL: str = "mongodb://localhost:27017/?directConnection=true&serverSelectionTimeoutMS=2000&replicaSet=dbrs"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_config() -> Config:
    return Config()
