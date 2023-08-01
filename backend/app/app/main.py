import logging
import logging.config
import traceback

import sentry_sdk
from app import schemas
from app.api.api_v1.api import api_router
from app.core.config import settings
from fastapi import APIRouter, FastAPI, HTTPException
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


@api_router.get("/healthcheck", response_model=schemas.Msg)
def healthcheck() -> schemas.Msg:
    try:
        from app.db.session import db_session
        from app.db.redis_session import RedisClient
        RedisClient.hget(name='item', key='id')
        db_session
    except Exception as er:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"msg": "OK"}


app.include_router(api_router, prefix=settings.API_V1_STR)
