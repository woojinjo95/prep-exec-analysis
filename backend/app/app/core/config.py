import os
from typing import Optional

from pydantic import BaseSettings, HttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", '')
    SENTRY_DSN: Optional[HttpUrl] = None
    SERVICE_NAME: str
    FILES_PATH: str = os.getenv("FILES_PATH", '/app/app/files')

    MONGODB_SERVER: str
    MONGODB_NAME: str
    MONGODB_PORT: str
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_AUTHENTICATION_SOURCE: str

    REDIS_HOST: str = os.getenv("REDIS_HOST", "")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_DB: int = os.getenv("REDIS_DB")

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    class Config:
        case_sensitive = True


settings = Settings()
