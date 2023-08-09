import logging
import os
import subprocess
import time
from multiprocessing import Event, Process, Queue

from ..configs.config import get_value, set_value
from ..configs.constant import RedisChannel
from ..utils._subprocess import kill_pid_grep
from .rotation import RotationFileManager
from ..connection.redis_pubsub import publish, get_strict_redis_connection


logger = logging.getLogger('main')
file_logger = logging.getLogger('file')


def construct_tshark_cmd() -> str:
    network_capture_configs = get_value('network')
    # nic = 'enx00e09900866a', 10
    nic = network_capture_configs['nic']
    segment_interval = network_capture_configs['segment_interval']
    output_path = network_capture_configs['real_time_packet_path']

    os.makedirs(output_path, exist_ok=True)

    # -a duration:30
    cmd = f'tshark -i {nic} -b interval:{segment_interval} -w {output_path}/packet.pcap -F pcap '
    return cmd


def start_capture(audio_values: Queue, stop_event: Event):
    network_capture_configs = get_value('network')
    segment_interval = network_capture_configs['segment_interval']
    check_intreval = segment_interval / 10
    cmd = construct_tshark_cmd()
    rotation_file_manager = RotationFileManager()

    try:
        set_value('state', 'packet', 'capturing')
        logger.info('Capture Start')
        with subprocess.Popen(cmd, shell=True) as process:
            while process.poll() is None and not stop_event.is_set():

                file_created_info = rotation_file_manager.check_new_file()
                if file_created_info is not None:
                    file_logger.error(f'Pcap: {file_created_info[0]} / {file_created_info[1]}')
                    rotation_file_manager.add_new_file(*file_created_info)
                else:
                    time.sleep(check_intreval)

            process.stdin.write(b'q')
            process.stdin.close()

    finally:
        # kill process
        time.sleep(0.5)
        kill_pid_grep('tshark')
        set_value('state', 'packet', 'idle')
        logger.info('Streaming ended')

    pass


def capture(stop_event: Event = Event()) -> Event:
    audio_values = Queue()

    capture_process = Process(target=start_capture, args=(audio_values, stop_event), daemon=True)

    capture_process.start()

    return stop_event
