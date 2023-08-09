import asyncio
import subprocess
from .utils import log
from .log import process_log_queue


async def read_stdout(stdout: any, queue: asyncio.Queue):
    print('read_stdout')
    while True:
        # buf = await stdout.read(4096)
        buf = await stdout.readline()
        if not buf:
            break
        line = buf.decode('utf-8').rstrip()
        print(f"stdout: {line}")
        queue.put_nowait(log(line, "stdout"))
    print('read_stdout end')


async def read_stderr(stderr: any, queue: asyncio.Queue):
    print('read_stderr')
    while True:
        buf = await stderr.readline()
        if not buf:
            break
        line = buf.decode('utf-8').rstrip()
        print(f"stderr: {line}")
        queue.put_nowait(log(line, "stderr"))
    print('read_stderr end')


async def consumer_adb_handler(pubsub: any, proc: any, CHANNEL_NAME: str, queue: asyncio.Queue):
    print(f"subscribe {CHANNEL_NAME}")
    await pubsub.subscribe(CHANNEL_NAME)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                print(message)
                data = message.pop('data')
                proc.stdin.write(f"{data}\n".encode('utf-8'))
                print(f"stderr: {data}")
                queue.put_nowait(log(data, "stdin"))
                await proc.stdin.drain()
                await asyncio.sleep(0.5)
    except Exception as exc:
        print(exc)
    print("consumer_handler end")


async def adb_connect(pubsub: any, ADB_HOST: str, ADB_PORT: int, CHANNEL_NAME: str):
    queue = asyncio.Queue()

    print("adb_devices")
    # 1. 연결된 디바이스가 하나임
    adb_devices = await asyncio.create_subprocess_shell("adb devices", shell=True)
    await adb_devices.wait()
    print(f"adb_connect {ADB_HOST}:{ADB_PORT}")
    adb_connect = await asyncio.create_subprocess_shell(f"adb connect {ADB_HOST}:{ADB_PORT}", shell=True)
    await adb_connect.wait()

    print("adb_shell")
    proc = await asyncio.create_subprocess_shell('adb shell', shell=True,
                                                 stdin=subprocess.PIPE,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE)

    print("create task")
    read_stderr_task = asyncio.create_task(read_stderr(proc.stderr, queue))
    read_stdout_task = asyncio.create_task(read_stdout(proc.stdout, queue))
    process_log_task = asyncio.create_task(process_log_queue(queue))
    consumer_task = asyncio.create_task(consumer_adb_handler(pubsub=pubsub, 
                                                             proc=proc, CHANNEL_NAME=CHANNEL_NAME, queue=queue))
    print("start task")
    done, pending = await asyncio.wait(
        [read_stderr_task, read_stdout_task, consumer_task, process_log_task], return_when=asyncio.FIRST_COMPLETED,
    )
    print(f"Done task: {done}")
    for task in pending:
        print(f"Canceling task: {task}")
        task.cancel()
