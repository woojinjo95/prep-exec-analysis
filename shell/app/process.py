import logging
import asyncio
import traceback
from sub.context import get_redis_pool, SHELL_TYPE, ADB_HOST, ADB_PORT, SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, CHANNEL_NAME
from sub.adb import adb_connect
from sub.ssh import ssh_connect

logger = logging.getLogger(__name__)


async def main():
    conn = await get_redis_pool()

    # 여기서 환경설정을 읽어오는 코드를 넣음
    # 각 커넥션 루프는 환경설정 변경을 인지하는 시점에서 종료되어야 함
    # 잔여작업
    # 데이터 로깅 Mongodb 등록
    # 규정된 메시지 처리

    # while True:
    try:
        if SHELL_TYPE == 'adb':
            await adb_connect(conn=conn, shell_id=1, ADB_HOST=ADB_HOST, ADB_PORT=int(ADB_PORT), CHANNEL_NAME=CHANNEL_NAME)
        if SHELL_TYPE == 'ssh':
            await ssh_connect(conn=conn, shell_id=2, SSH_HOST=SSH_HOST, SSH_PORT=int(SSH_PORT), SSH_USERNAME=SSH_USERNAME,
                              SSH_PASSWORD=SSH_PASSWORD, CHANNEL_NAME=CHANNEL_NAME)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    print('try reconnect')
    await asyncio.sleep(3)

asyncio.run(main())
