import os
import redis.asyncio as redis


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", '')
CHANNEL_NAME = os.getenv("CHANNEL_NAME", 'shell')

ADB_HOST = os.getenv("ADB_HOST", "192.168.1.208")
ADB_PORT = os.getenv("ADB_PORT", 5555)

SSH_HOST = os.getenv("SSH_HOST", "192.168.1.23")
SSH_USERNAME = os.getenv("SSH_USERNAME", "nextlab")
SSH_PASSWORD = os.getenv("SSH_PASSWORD", ".nextlab1@")
SSH_PORT = os.getenv("SSH_PORT", 22)

SHELL_TYPE = os.getenv("SHELL_TYPE", "adb")  # adb, ssh


async def get_redis_pool():
    return await redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)