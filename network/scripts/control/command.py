from typing import Tuple
import subprocess
import os
import signal


def get_stdout(cmd: str) -> str:
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) as process:
        stdout = process.stdout.read().decode()
        return stdout


def get_pid_list(name: str) -> Tuple[int]:
    pid_list = get_stdout(f'pidof {name}').split()
    return tuple(int(pid) for pid in pid_list) or ()


def kill_process(name: str):
    try:
        pids = get_pid_list(name)
        for pid in pids:
            os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(str(e).encode())
