from redis import Redis
from app.core.config import settings


RedisClient = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                    charset="utf-8", db=settings.REDIS_DB, decode_responses=True)
