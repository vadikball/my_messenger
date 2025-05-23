"""Application settings."""

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # base kwargs
    DEBUG: bool = False
    APP_HOST: str

    # database
    POSTGRES_DSN: str
    SQL_DEBUG: bool = False

    ALLOWED_ORIGINS: List[str] = Field(default=["*"], validation_alias="ALLOWED_ORIGINS")
    SECRET_KEY: str


settings = AppSettings()  # type: ignore
