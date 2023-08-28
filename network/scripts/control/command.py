from typing import Tuple
import subprocess
import os
import signal
import logging

logger = logging.getLogger('shell')


def get_stdout(cmd: str, log=True) -> str:
    if log is True:
        logger.info(cmd)
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        stdout = process.stdout.read().decode()

        if process.stderr and process.stderr.read() != b'':
            logger.warning(f'Error in shell: {process.stderr.read().decode()} / stdout: {stdout}')
        return stdout


def get_pid_list(name: str) -> Tuple[int]:
    pid_list = get_stdout(f'pidof {name}', log=False).split()
    return tuple(int(pid) for pid in pid_list) or ()


def kill_process(name: str):
    try:
        pids = get_pid_list(name)
        for pid in pids:
            os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(str(e).encode())
