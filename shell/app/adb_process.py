import os
import logging
import asyncio
import subprocess
import redis.asyncio as redis


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", '')
CHANNEL_NAME = os.getenv("CHANNEL_NAME", 'shell')

logger = logging.getLogger(__name__)


async def get_redis_pool():
    return await redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)


async def read_stdout(stdout):
    print('read_stdout')
    while True:
        buf = await stdout.read(4096)
        if not buf:
            break
        print(f"stdout: { buf.decode('utf-8') }")
    print('read_stdout end')


async def read_stderr(stderr):
    print('read_stderr')
    while True:
        buf = await stderr.read(4096)
        if not buf:
            break
        print(f"stderr: { buf.decode('utf-8')  }")
    print('read_stderr end')


async def consumer_handler(pubsub: any, proc: any):
    print(f"subscribe {CHANNEL_NAME}")
    await pubsub.subscribe(CHANNEL_NAME)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                print(message)
                data = message.pop('data')
                proc.stdin.write(f"{data}\n".encode('utf-8'))
                await proc.stdin.drain()
                await asyncio.sleep(0.5)
    except Exception as exc:
        logger.error(exc)
    print("consumer_handler end")


async def main():
    conn = await get_redis_pool()
    pubsub = conn.pubsub()

    proc = await asyncio.create_subprocess_shell('adb shell', shell=True,
                                                 stdin=subprocess.PIPE,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE)

    read_stderr_task = asyncio.create_task(read_stderr(proc.stderr))
    read_stdout_task = asyncio.create_task(read_stdout(proc.stdout))
    consumer_task = asyncio.create_task(consumer_handler(pubsub=pubsub, proc=proc))

    done, pending = await asyncio.wait(
        [read_stderr_task, read_stdout_task, consumer_task], return_when=asyncio.FIRST_COMPLETED,
    )

    logger.debug(f"Done task: {done}")
    for task in pending:
        logger.debug(f"Canceling task: {task}")
        task.cancel()

asyncio.run(main())
