import logging
import asyncio
import traceback
from sub.context import get_redis_pool, CHANNEL_NAME
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

    while True:
        try:
            stb_connection = await conn.hgetall('stb_connection')
            testrun = await conn.hgetall('testrun')

            testinfo = {}
            testinfo['scenario_id'] = testrun.get('scenario_id', '')
            testinfo['testrun_id'] = testrun.get('id', '')

            SHELL_TYPE = stb_connection.get('mode', 'adb')
            ADB_HOST = stb_connection.get('host', 'localhost')
            ADB_PORT = stb_connection.get('port', 22)
            SSH_HOST = stb_connection.get('host', 'localhost')
            SSH_PORT = stb_connection.get('port', 5555)
            SSH_USERNAME = stb_connection.get('username', 'root')
            SSH_PASSWORD = stb_connection.get('password', '')

            print(stb_connection)
            print(testrun)
            if SHELL_TYPE == 'adb':
                await adb_connect(conn=conn, shell_id=1, ADB_HOST=ADB_HOST,
                                  ADB_PORT=int(ADB_PORT), CHANNEL_NAME=CHANNEL_NAME, testinfo=testinfo)
            if SHELL_TYPE == 'ssh':
                await ssh_connect(conn=conn, shell_id=2, SSH_HOST=SSH_HOST,
                                  SSH_PORT=int(SSH_PORT), SSH_USERNAME=SSH_USERNAME,
                                  SSH_PASSWORD=SSH_PASSWORD, CHANNEL_NAME=CHANNEL_NAME, testinfo=testinfo)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        print('try reconnect')
        await asyncio.sleep(3)


asyncio.run(main())
