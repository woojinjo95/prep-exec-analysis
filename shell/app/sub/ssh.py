import sys
import asyncio
from typing import Optional
import asyncssh
from .utils import log
from .log import process_log_queue


class QAASClientSession(asyncssh.SSHClientSession):
    def set_queue(self, queue: asyncio.Queue):
        self._queue = queue

    def data_received(self, data: str, datatype: asyncssh.DataType) -> None:
        print(data, end='')
        self._queue.put_nowait(log(data, "stdout"))

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            print('SSH session error: ' + str(exc), file=sys.stderr)


class QAASSSHClient(asyncssh.SSHClient):
    def connection_made(self, conn: asyncssh.SSHClientConnection) -> None:
        print('Connection made to %s.' % conn.get_extra_info('peername')[0])

    def auth_completed(self) -> None:
        print('Authentication successful.')


async def consumer_ssh_handler(pubsub: any, channel: any, CHANNEL_NAME: str, queue: asyncio.Queue):
    print(f"subscribe {CHANNEL_NAME}")
    await pubsub.subscribe(CHANNEL_NAME)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                print(message)
                data = message.pop('data')
                channel.writelines([data])
                queue.put_nowait(log(data, "stdin"))
                await asyncio.sleep(0.5)
    except Exception as exc:
        print(exc)
    print("consumer_handler end")


async def ssh_connect(pubsub: any, SSH_HOST: str, SSH_PORT: int, SSH_USERNAME: str, SSH_PASSWORD: str, CHANNEL_NAME: str):
    queue = asyncio.Queue()

    connection, client = await asyncssh.create_connection(QAASSSHClient, host=SSH_HOST, port=SSH_PORT,
                                                          username=SSH_USERNAME, password=SSH_PASSWORD,
                                                          known_hosts=None)
    async with connection:
        channel, session = await connection.create_session(QAASClientSession)
        session.set_queue(queue)

        consumer_task = asyncio.create_task(consumer_ssh_handler(pubsub=pubsub,
                                                                 channel=channel,
                                                                 CHANNEL_NAME=CHANNEL_NAME, queue=queue))
        process_log_task = asyncio.create_task(process_log_queue(queue))
        # await channel.wait_closed()
        done, pending = await asyncio.wait(
            [consumer_task, process_log_task], return_when=asyncio.FIRST_COMPLETED,
        )
        print(f"Done task: {done}")
        for task in pending:
            print(f"Canceling task: {task}")
            task.cancel()
