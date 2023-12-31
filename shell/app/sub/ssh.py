import sys
import json
from datetime import datetime
import asyncio
import traceback
from typing import Optional
import asyncssh
from .log import process_log_queue
from .message import check_skip_message


class QAASClientSession(asyncssh.SSHClientSession):
    def set_queue(self, queue: asyncio.Queue):
        self._queue = queue

    def data_received(self, data: str, datatype: asyncssh.DataType) -> None:
        print(data, end='')
        self._queue.put_nowait({'timestamp': datetime.utcnow().timestamp(), 'module':  "stdout", 'message': data})

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            print('SSH session error: ' + str(exc), file=sys.stderr)


class QAASSSHClient(asyncssh.SSHClient):
    def connection_made(self, conn: asyncssh.SSHClientConnection) -> None:
        print('Connection made to %s.' % conn.get_extra_info('peername')[0])

    def auth_completed(self) -> None:
        print('Authentication successful.')


async def consumer_ssh_handler(conn: any, channel: any, shell_id: int, CHANNEL_NAME: str, queue: asyncio.Queue):
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
                    
                    print(message)
                    command = f"{message['data']['command']}\n"
                    channel.write(command)
                    queue.put_nowait({'timestamp': datetime.utcnow().timestamp(), 'module':  "stdin", 'message': command})
                    await conn.publish(CHANNEL_NAME, json.dumps({
                        "msg": "shell_response",
                        "level": "info",
                        "data": {
                            "mode": "ssh",
                            "command": command
                        },
                        "service": "shell",
                        "timestamp": datetime.utcnow().timestamp()
                    }))
            except Exception as e:
                print(e)
                print(traceback.format_exc())

    except Exception as exc:
        print(exc)
    print("consumer_handler end")


async def ssh_connect(conn: any, shell_id: int, SSH_HOST: str,
                      SSH_PORT: int, SSH_USERNAME: str, SSH_PASSWORD: str, CHANNEL_NAME: str, testinfo: dict):
    queue = asyncio.Queue()

    connection, client = await asyncssh.create_connection(QAASSSHClient, host=SSH_HOST, port=SSH_PORT,
                                                          username=SSH_USERNAME, password=SSH_PASSWORD,
                                                          known_hosts=None)
    async with connection:
        channel, session = await connection.create_session(QAASClientSession)
        session.set_queue(queue)

        consumer_task = asyncio.create_task(consumer_ssh_handler(conn=conn,
                                                                 channel=channel, shell_id=shell_id,
                                                                 CHANNEL_NAME=CHANNEL_NAME, queue=queue))
        process_log_task = asyncio.create_task(process_log_queue(queue, conn, CHANNEL_NAME, "ssh"))
        await conn.publish(CHANNEL_NAME, json.dumps({
            "msg": "config_response",
            "level": "info",
            "data": {
                "mode": "adb",
                "host": SSH_HOST,
                "port": SSH_PORT,
                "username": SSH_USERNAME,
                "password": SSH_PASSWORD
            },
            "service": "shell",
            "timestamp": datetime.utcnow().timestamp()
        }))
        # await channel.wait_closed()
        done, pending = await asyncio.wait(
            [consumer_task, process_log_task], return_when=asyncio.FIRST_COMPLETED,
        )
        print(f"Done task: {done}")
        for task in pending:
            print(f"Canceling task: {task}")
            task.cancel()
