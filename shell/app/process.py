import logging
import asyncio
from .context import get_redis_pool, SHELL_TYPE, ADB_HOST, ADB_PORT, SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD
from .adb import adb_connect
from .ssh import ssh_connect

logger = logging.getLogger(__name__)


async def main():
    conn = await get_redis_pool()
    pubsub = conn.pubsub()

    # 여기서 환경설정을 읽어오는 코드를 넣음
    # 각 커넥션 루프는 환경설정 변경을 인지하는 시점에서 종료되어야 함
    # 잔여작업
    # 데이터 로깅 Mongodb 등록
    # 규정된 메시지 처리

    while True:
        try:
            if SHELL_TYPE == 'adb':
                await adb_connect(pubsub, ADB_HOST, ADB_PORT)
            if SHELL_TYPE == 'ssh':
                await ssh_connect(pubsub, SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD)
        except Exception as e:
            print(e)

asyncio.run(main())
