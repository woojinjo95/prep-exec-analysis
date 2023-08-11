import logging
import re
from multiprocessing.managers import DictProxy

from scripts.configs.constant import SerialRemoconSetting
from scripts.device.serial.serial_device import SerialDevice

from ....configs.constant import RedisChannel
from ....connection.redis_pubsub import get_strict_redis_connection, publish
from .abstract_remocon import AbstractRemocon

using_control_board = True


logger = logging.getLogger('remocon')


def is_pronto_code_pattern(code: str) -> bool:
    pattern = '[0-9A-F]{4} ' * 76
    return True if re.match(pattern, code) else False


class SerialRemocon(AbstractRemocon):

    def __init__(self, event_time_dict: DictProxy, serial_device: SerialDevice):

        AbstractRemocon.__init__(self, event_time_dict)
        self.remocon_setting = SerialRemoconSetting()
        self.serial_device = serial_device
        self.redis_connection = get_strict_redis_connection()
        self.error_count = 0

    # pronto_code 로 직접 리모콘 명령
    def press_key_by_command(self, command_queue: dict) -> float:
        logger.info(f'ir remocon transmit: {command_queue}')
        if self.serial_device is None:
            logger.error('failed to detect serial device.')
            raise Exception('failed to detect serial device.')

        key = command_queue['key']
        # ir remocon does not use 'key' itself, just use pronto code
        pronto_code = command_queue['code']
        press_time = command_queue['press_time']

        get_event_time = True
        log, event_time = self.serial_device.transmit_ir(pronto_code, press_time=press_time, serial_get_event_time=get_event_time)

        if log == 'ok':
            publish(self.redis_connection, RedisChannel.command, {'msg': 'remocon_response',
                                                                  'data': {"key": key,
                                                                           "type": "ir",
                                                                           "press_time": press_time,
                                                                           "sensor_time": event_time}})

            self.error_count = 0
            return event_time

        else:

            error_level = 'error' if self.error_count < 3 else 'critical'

            publish(self.redis_connection, RedisChannel.command, {'msg': 'remocon_response',
                                                                  'data': {"key": key,
                                                                           'level': error_level,
                                                                           "type": "ir",
                                                                           "press_time": press_time,
                                                                           "log": log}})

            self.error_count += 1
            return -1
