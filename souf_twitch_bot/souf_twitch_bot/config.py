from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    access_token: str

    refresh_token: str

    client_id: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
