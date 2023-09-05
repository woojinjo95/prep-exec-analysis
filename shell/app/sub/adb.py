import json
import asyncio
import subprocess
from datetime import datetime
from .log import process_log_queue
from .message import check_skip_message


async def read_stdout(stdout: any, queue: asyncio.Queue):
    print('read_stdout')
    while True:
        # buf = await stdout.read(4096)
        buf = await stdout.readline()
        if not buf:
            break
        line = buf.decode('utf-8').rstrip()
        print(f"stdout: {line}")
        queue.put_nowait({'timestamp': datetime.utcnow().timestamp(), 'module':  "stdout", 'message': line})
    print('read_stdout end')


async def read_stderr(stderr: any, queue: asyncio.Queue):
    print('read_stderr')
    while True:
        buf = await stderr.readline()
        if not buf:
            break
        line = buf.decode('utf-8').rstrip()
        print(f"stderr: {line}")
        queue.put_nowait({'timestamp': datetime.utcnow().timestamp(), 'module':  "stderr", 'message': line})
    print('read_stderr end')


async def consumer_adb_handler(conn: any, shell_id: int, proc: any, CHANNEL_NAME: str, queue: asyncio.Queue):
    print(f"subscribe {CHANNEL_NAME}")
    pubsub = conn.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)
    try:
        while True:
            try:  # 루프 깨지지 않도록 예외처리
                raw = await pubsub.get_message(ignore_subscribe_messages=True)
                await asyncio.sleep(0.01)
                # 필요없는 메시지는 여기서 걸러줌
                if raw is None:
                    continue
                if isinstance(raw, dict):
                    message = json.loads(raw['data'])

                    print(f"consumer_adb_handler: {message}")
                    if not check_skip_message(message, shell_id):
                        continue

                    # config 변경 메시지 수신
                    # 두가지 변경 메시지가 있음
                    # 연결 정보가 변경되는 메시지 
                    # 테스트런과 프로젝트가 변경되는 메시지
                    if message['msg'] == 'config' or message['msg'] == 'workspace':
                        # 현재 작업을 종료함.
                        # 컨피그가 변경되었거나 워크스페이스가 변경되었기 때문에
                        return

                    command = message['data']['command']
                    proc.stdin.write(f"{command}\n".encode('utf-8'))
                    print(f"stderr: {command}")
                    queue.put_nowait({'timestamp': datetime.utcnow().timestamp(), 'module':  "stdin", 'message': command})
                    await proc.stdin.drain()
                    await asyncio.sleep(0.5)
                    await conn.publish(CHANNEL_NAME, json.dumps({
                        "msg": "shell_response",
                        "level": "info",
                        "service": "shell",
                        "timestamp": datetime.utcnow().timestamp()
                    }))
            except Exception as e:
                print(e)
    except Exception as exc:
        print(exc)
    print("consumer_handler end")


async def adb_connect(conn: any, shell_id: int, ADB_HOST: str, ADB_PORT: int, CHANNEL_NAME: str, testinfo: dict):
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
    process_log_task = asyncio.create_task(process_log_queue(queue, conn, CHANNEL_NAME, "adb", shell_id, testinfo))
    consumer_task = asyncio.create_task(consumer_adb_handler(conn=conn, shell_id=shell_id,
                                                             proc=proc, CHANNEL_NAME=CHANNEL_NAME, queue=queue))
    print("start task")
    done, pending = await asyncio.wait(
        [read_stderr_task, read_stdout_task, consumer_task, process_log_task], return_when=asyncio.FIRST_COMPLETED,
    )
    print(f"Done task: {done}")
    for task in pending:
        print(f"Canceling task: {task}")
        task.cancel()
