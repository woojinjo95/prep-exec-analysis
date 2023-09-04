import logging
import os
import shlex
import subprocess
import traceback

from typing import Tuple

logger = logging.getLogger('main')


# 명령에 대한 output을 가져옴. 단, 명령은 수행 후 종료되는 명령이어야 함
def get_output(cmd: str) -> str:
    try:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as process:
            outputs = process.stdout.read().decode()
            return outputs
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        return ''


def command_generator(command: str, max_count: int = None):
    """_summary_
    tail처럼 foreground 상에서 지속되는 명령에 대한 output을 하나씩 yield 하여 가져옴
    Args:
        command (str): command string for shell
        max_count (int, optional): count for yielding output. if None, yield result infinitely
    Yields:
        _type_: _description_
    """
    count = 0
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            logger.info('command generator terminated')
            break
        if output:
            ret = output.strip()
            yield ret

            count += 1
            if max_count and count >= max_count:
                break

    rc = process.poll()
    return rc


def get_pid(name: str) -> Tuple[str]:
    if os.name == 'posix':
        pids = get_output(f'pidof {name}').split()
    else:
        pids = None
    return pids


def get_pid_grep(*names: str) -> Tuple[str]:
    if os.name == 'posix':
        grep_cmd = " | grep ".join([f'"{name}"' for name in names])
        pids = get_output(f'ps -eaf | grep {grep_cmd} | grep -v grep | awk \'{{print $2}}\'').split()
    else:
        pids = None
    return pids


def kill_pid(name: str):
    try:
        pids = get_pid(name)
        if pids is not None:
            for pid in pids:
                os.kill(int(pid), 9)
    except Exception as e:
        print(str(e).encode())


def kill_pid_grep(*names: str):
    try:
        pids = get_pid_grep(*names)
        if pids is not None:
            for pid in pids:
                os.kill(int(pid), 9)
    except Exception as e:
        print(str(e).encode())
