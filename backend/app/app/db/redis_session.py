from redis import Redis
from app.core.config import settings


if settings.REDIS_PASSWORD:
    RedisClient = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                    charset="utf-8", db=settings.REDIS_DB, password=settings.REDIS_PASSWORD, decode_responses=True)
else:
    RedisClient = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                    charset="utf-8", db=settings.REDIS_DB, decode_responses=True)
