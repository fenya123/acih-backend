"""Configuration module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.shared.environment import get_env_file


if TYPE_CHECKING:
    from typing import Self


class Config(BaseSettings):
    """Application's configuration class."""

    MINIO_ACCESS_KEY: str = Field(..., min_length=1)
    MINIO_HOST: str = Field(..., min_length=1)
    MINIO_PORT: str = Field(..., min_length=1)
    MINIO_SECRET_KEY: str = Field(..., min_length=1)

    POSTGRES_DB: str = Field(..., min_length=1)
    POSTGRES_HOST: str = Field(..., min_length=1)
    POSTGRES_PASSWORD: str = Field(..., min_length=1)
    POSTGRES_PORT: str = Field(..., min_length=1)
    POSTGRES_USER: str = Field(..., min_length=1)

    SECRET_KEY: str = Field(..., min_length=1)

    @property
    def POSTGRES_CONNECTION_URI(self: Self) -> str:  # noqa: D102,N802
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=get_env_file(), extra="allow", frozen=True)


config = Config()
