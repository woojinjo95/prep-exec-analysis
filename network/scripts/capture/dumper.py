import logging
import math
import os
import re
import subprocess
import time
from glob import glob
from threading import Thread
from typing import List

from multiprocessing import Event
from scripts.control.command import get_pid_list, kill_process
from ..utils.docker import is_running_in_docker

logger = logging.getLogger('capture')


dirpath = os.path.dirname(os.path.abspath(__file__))
dirname = 'pcaps'
os.makedirs(os.path.join(dirpath, dirname), exist_ok=True)
FILENAME = 'result_%s.pcap'
DIRNAME = os.path.join(dirpath, dirname)
TCPDUMP = 'tcpdump'
TSHARK = 'tshark'
ROTATING_FILE_COUNT = 12


def get_pcap_file_list(dirname: str = DIRNAME) -> List[str]:
    return glob(os.path.join(dirname, '*.pcap'))


def clear_pcap_file():
    file_list = get_pcap_file_list()
    for pcap_file in file_list:
        os.remove(pcap_file)
    logger.info(f'Remove previous pcap files: {len(file_list)}')


def remove_old_pcap_file(max_count: int = 100):
    while len(get_pcap_file_list()) > max_count:
        oldest_file = sorted(get_pcap_file_list())[0]
        os.remove(oldest_file)
        logger.info(f'Remove: {oldest_file}')


def start_capture(interface: str, interval: int, dump_interval: int = 5, clear: bool = True,
                  rotating_file_count: int = ROTATING_FILE_COUNT, state: dict = {}, stop_event: Event = Event()):
    file_path = os.path.join(DIRNAME, FILENAME)
    if clear:
        clear_pcap_file()

    if interval > 0:
        count = math.ceil(interval / dump_interval)
        interval_option = f'-W {count}'
    else:
        interval_option = ''

    if is_running_in_docker():
        # https://bugzilla.redhat.com/show_bug.cgi?id=214377
        # 버그가 아니라 고치지 않겠다는 선언
        docker_option = '-Z root'
    else:
        docker_option = ''

    start_time = time.time()
    cmd = f'{TCPDUMP} -i "{interface}" -G {dump_interval} {interval_option} -w {file_path} {docker_option}'
    logger.info(f'Dump : {cmd}')

    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        time.sleep(1)  # wait for tcpdump process start.
        while not stop_event.is_set() and process.returncode is None:
            # rotating file manager
            remove_old_pcap_file(rotating_file_count)
            time.sleep(dump_interval / 5)

            if interval > 0 and time.time() > start_time + interval + max(1, interval * 0.1):
                logger.warning('Capture process is not completed by 10% offset. kill process.')
                break

        stdout_pipe = process.stdout.read()
        stderr_pipe = process.stderr.read()

    logger.info(f'Capture parse process ended')

    stdout = stdout_pipe.decode() if stderr_pipe is not None else ''
    stderr = stderr_pipe.decode() if stderr_pipe is not None else ''
    stdout = stdout + '\n' + stderr

    try:
        captured_count, dropped_count = 0, 0
        for line in stdout.split('\n'):
            # tcpdump only if tshark function added, this one need to update.
            for line in line.split('\n'):
                if 'captured' in line:
                    captured_count = int(re.search('\d+', line).group())
                if 'dropped' in line:
                    dropped_count = int(re.search('\d+', line).group())
                    break
    except:
        captured_count, dropped_count = 0, 0

    logger.info(f'{captured_count} packet is captured for {interval} seconds.')
    if dropped_count > 0:
        logger.warning(f'{dropped_count} packet is dropped! some error maybe occured by this dropped packet.')
        state['dropped'] = True
        state['dropped_count'] = dropped_count
    else:
        state['dropped'] = False
        state['dropped_count'] = 0

    kill_process(TCPDUMP)  # to protect zombie process. but it is too strong, kill all tcpdump process in os.


def start_capture_thread(*args, **kwargs) -> dict:
    logger.info('Start capture thread')
    capture_thread = Thread(target=start_capture, args=args, kwargs=kwargs)
    capture_thread.start()

    return {'thread': capture_thread,
            'start_time': time.time()}


def stop_capture():
    logger.warning(f'Kill {TCPDUMP} process by pid kill')
    kill_process(TCPDUMP)
