import asyncio
import subprocess


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


async def adb_connect(pubsub: any, ADB_HOST: str, ADB_PORT: int, CHANNEL_NAME: str):
    print(f"adb_connect {ADB_HOST}:{ADB_PORT}")
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
    read_stderr_task = asyncio.create_task(read_stderr(proc.stderr))
    read_stdout_task = asyncio.create_task(read_stdout(proc.stdout))
    consumer_task = asyncio.create_task(consumer_adb_handler(pubsub=pubsub, proc=proc, CHANNEL_NAME=CHANNEL_NAME))
    print("start task")
    done, pending = await asyncio.wait(
        [read_stderr_task, read_stdout_task, consumer_task], return_when=asyncio.FIRST_COMPLETED,
    )
    print(f"Done task: {done}")
    for task in pending:
        print(f"Canceling task: {task}")
        task.cancel()


async def consumer_adb_handler(pubsub: any, proc: any, CHANNEL_NAME: str):
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
        print(exc)
    print("consumer_handler end")
