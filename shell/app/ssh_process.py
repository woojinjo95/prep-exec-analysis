import os
import logging
import asyncio
import asyncssh
import sys
from typing import Optional
import redis.asyncio as redis


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", '')
CHANNEL_NAME = os.getenv("CHANNEL_NAME", 'shell')


SSH_HOST = os.getenv("SSH_HOST", "192.168.1.23")
SSH_USERNAME = os.getenv("SSH_USERNAME", "nextlab")
SSH_PASSWORD = os.getenv("SSH_PASSWORD", ".nextlab1@")
SSH_PORT = os.getenv("SSH_PORT", 22)

SHELL_TYPE = os.getenv("SHELL_TYPE", "adb")  # adb, ssh

logger = logging.getLogger(__name__)


class QAASClientSession(asyncssh.SSHClientSession):
    def data_received(self, data: str, datatype: asyncssh.DataType) -> None:
        print(data, end='')

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            print('SSH session error: ' + str(exc), file=sys.stderr)


class QAASSSHClient(asyncssh.SSHClient):
    def connection_made(self, conn: asyncssh.SSHClientConnection) -> None:
        print('Connection made to %s.' % conn.get_extra_info('peername')[0])

    def auth_completed(self) -> None:
        print('Authentication successful.')


async def get_redis_pool():
    return await redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)


async def consumer_handler(pubsub: any, channel: any):
    print(f"subscribe {CHANNEL_NAME}")
    await pubsub.subscribe(CHANNEL_NAME)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                print(message)
                data = message.pop('data')
                channel.writelines([data])
                await asyncio.sleep(0.5)
    except Exception as exc:
        logger.error(exc)
    print("consumer_handler end")


async def main():
    conn = await get_redis_pool()
    pubsub = conn.pubsub()

    connection, client = await asyncssh.create_connection(QAASSSHClient, host=SSH_HOST, port=SSH_PORT,
                                                          username=SSH_USERNAME, password=SSH_PASSWORD,
                                                          known_hosts=None)
    async with connection:
        channel, session = await connection.create_session(QAASClientSession)
        consumer_task = asyncio.create_task(consumer_handler(pubsub=pubsub, channel=channel))
        # await channel.wait_closed()

        done, pending = await asyncio.wait(
            [consumer_task], return_when=asyncio.FIRST_COMPLETED,
        )
        logger.debug(f"Done task: {done}")
        for task in pending:
            logger.debug(f"Canceling task: {task}")
            task.cancel()

asyncio.run(main())
