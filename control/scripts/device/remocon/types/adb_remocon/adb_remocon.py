import time
from typing import List, Tuple
# from scripts.log_service.stb_log.stb_connection.utils import get_connection_info
# from ppadb.client import Client as AdbClient
from typing import Tuple
import logging

from .adb_keymap import keymap

logger = logging.getLogger('remocon')


# TODO

def is_adb_keyformat(code: str) -> bool:
    # ADB key는 기본적으로 모두 대문자이거나, 아예 숫자
    # 리모콘 키는 Capitalized Camel이며, _가 기본적으로 없음
    return True if code.isdigit() or code.isupper() else False


class Connect:
    # 기존 로그의 exec_command와 달리, 이 명령은 명령 수행 시간이 순간인 것을 가정하며 그 결괏값을 중시함
    def __init__(self, ip: str, port: int):
        self.client = AdbClient(host='127.0.0.1', port=5037)
        self.client.remote_connect(ip, int(port))
        self.device = self.client.device(f'{ip}:{port}')
        self.conn = self.device.create_connection()

    def __enter__(self):
        # with 문 사용을 위한 문법
        return self

    def __exit__(self, type, value, traceback):
        # 이렇게 정리하지 않으면, ResourceWarning 발생
        self.conn.close()

    def exec_command(self, command: str) -> Tuple[float, float, str]:
        # 일반적 셋톱이 리모콘 명령 하나를 날렸을 때 error_bound 값은 4~7 ms로 수준
        # errorbound 값은 일단 로그에 남기는 용도로만 사용함.
        # exec_time 은 명령을 날린다 -> 다시 명령이 돌아온다가 같고, 명령 수행시간은 0에 수렴한다고 가정하여 정확히 왕복 중간점을 지정함
        # 실제로는 어떻게 될지 모르나, error_bound를 보았을 때 오차는 2~4 ms 수준이며 60 FPS 기준 이미지가 16.7 ms 간격이니 충분하다 판단.add()
        # 단 인터넷 환경에 따라 영향을 받을수 있음.

        cmd = f'shell:{command}'
        exec_start_time = time.time()
        self.conn.send(cmd)
        exec_end_time = time.time()
        stdout = self.conn.socket.makefile()

        exec_time = (exec_end_time + exec_start_time) / 2
        error_bound = (exec_end_time - exec_start_time) / 2

        return exec_time, error_bound, stdout.read().strip()


def transmit_adb(slot_index: int, key: str):
    connection_info = get_connection_info(slot_index)
    ip = connection_info['host']
    port = connection_info['port']
    with Connect(ip, port) as connection:
        key_code = keymap[key.lower()] if not is_adb_keyformat(key) and key.lower() not in keymap.keys() else key
        exec_time, error_bound, _ = connection.exec_command(f'input keyevent {key_code}')
        logger.debug(f'ADB remocon result: {exec_time} {error_bound}')
    return exec_time
