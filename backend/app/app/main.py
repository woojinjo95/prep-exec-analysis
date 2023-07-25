import logging
import logging.config

import sentry_sdk
from app.api.api_v1.api import api_router
from app.core.config import settings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

logging.config.fileConfig('./app/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
sentry_sdk.init(dsn=settings.SENTRY_DSN)
sentry_sdk.set_tag("service", f"{settings.SERVICE_NAME}-backend")


def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.SERVICE_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    return app


app = get_application()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
