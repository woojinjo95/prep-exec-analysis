import os
import time
import asyncio
import logging
import redis.asyncio as redis

REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=''

logger = logging.getLogger(__name__)

async def get_redis_pool():
    return await redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)


async def producer_handler(pubsub: redis):
    await pubsub.subscribe("control")
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                print(message.get('data'))
    except Exception as exc:
        logger.error(exc)


async def main():
    conn = await get_redis_pool()
    pubsub = conn.pubsub()
    consumer_task = producer_handler(pubsub=pubsub)
    done, pending = await asyncio.wait(
        [consumer_task], return_when=asyncio.FIRST_COMPLETED,
    )
    logger.debug(f"Done task: {done}")
    for task in pending:
        logger.debug(f"Canceling task: {task}")
        task.cancel()

if __name__ == "__main__":
    asyncio.run(main())