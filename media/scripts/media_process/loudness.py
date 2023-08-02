import logging
import math
import os
import re
import traceback
from multiprocessing import Event, Process

from ..configs.config import set_value
from ..configs.constant import AudioDevice, RedisChannel
from ..connection.local_connect import run_command_in_docker_host
from ..connection.redis_pubsub import Subscribe, get_strict_redis_connection

logger = logging.getLogger('audio')

default_loudness_values = {'t': 0, 'M': -90, 'I': -90, 'inactive': True}


def set_device_volume(audio_name: str, audio_gain: float = None):
    if audio_gain is None:
        audio_gain = AudioDevice.gain

    if os.name == 'nt':
        try:
            cmd = f'setvol {audio_gain} device {audio_name}'
            with subprocess.Popen(cmd, stdout=subprocess.PIPE) as process:
                out = process.stdout.read()
                if out and out.decode().strip() != '':
                    logger.error(out.decode().strip())
                else:
                    logger.info(f'Set {audio_name} volume to {audio_gain} ({AudioDevice.gain} is default)')
        except FileNotFoundError:
            logger.error('Fail to find SetVol.exe. please add executor path to environmental variable')
        except Exception as e:
            logger.error(f'Failed to set audio gain: {traceback.format_exc()}')
    else:
        try:
            card_num = audio_name.split(':')[1]
            logger.info(f'Set {audio_name} volume to {audio_gain} ({AudioDevice.gain} is default)')
            run_command_in_docker_host(f'amixer -c {card_num} set Capture {audio_gain}%')
        except:
            logger.error(f'Failed to set audio gain: {traceback.format_exc()}')


def pattern_value(value: str) -> str:
    return f'{value}:\s*(?P<{value}>[^\s]+)\s+.*'


def value2float(value_str: str, default=-90) -> float:
    try:
        value = float(value_str)
        if math.isnan(value):
            raise ValueError
    except ValueError:
        value = default
    return value


def get_sound_values(start_time: float, line: str) -> dict:
    values = default_loudness_values
    if re.search(r'\[Parsed_ebur128_0.+\] t:', line):
        patterns = ''.join([pattern_value(v) for v in ['t', 'M', 'I']])
        result = re.search(re.compile(patterns), line)
        if result:
            values = result.groupdict()

            for key, value in values.items():
                values[key] = value2float(value)

            values['t'] = round(values['t'] + start_time, 2)
            values['M'] = max(values['M'], -90)
            values['I'] = max(values['I'], -90)
            values['inactive'] = False
        else:
            pass
    else:
        pass

    return values


def test_audio_redis_update(stop_event: Event):
    def job():
        with get_strict_redis_connection() as src:
            idx = 0
            for loudness in Subscribe(src, RedisChannel.loudness, stop_event):
                if idx % 10 == 0:
                    set_value('test', 'sound_level', loudness)

    Process(target=job).start()
