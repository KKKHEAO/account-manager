from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')
    # PG
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: str
    postgres_driver: str
    postgres_host: str
    # JWT
    jwt_exp: int
    jwt_secret: str


@lru_cache
def get_settings():
    return Settings()
