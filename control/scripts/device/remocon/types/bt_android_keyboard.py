import logging
import time
from multiprocessing.managers import DictProxy

import serial
from scripts.configs.constant import BTRemoconSetting
from scripts.device.serial.serial_device import SerialDevice

from ....configs.constant import RedisChannel
from ....connection.redis_pubsub import get_strict_redis_connection, publish
from .abstract_remocon import AbstractRemocon
from .bluetooth.bt_key import btnPageRemoconKey

logger = logging.getLogger('remocon')


class BTAndroidKeyboard(AbstractRemocon):

    def __init__(self, event_time_dict: DictProxy, serial_device: SerialDevice):

        AbstractRemocon.__init__(self, event_time_dict)
        self.remocon_setting = BTRemoconSetting()
        self.serial_device = serial_device
        self.redis_connection = get_strict_redis_connection()
        self.error_count = 0
        self.time_offset = 0.0005
        
        
    # pronto_code 로 직접 리모콘 명령
    def press_key_by_command(self, command_queue: dict) -> float:
        logger.info(f'bt remocon transmit: {command_queue}')
        if self.serial_device is None:
            logger.error('Failed to detect bt serial device.')
            raise Exception('Failed to detect bt serial device.')
        try:
            key = command_queue['key'].lower()
            press_time = command_queue['press_time']
            remocon_type = command_queue['type']
            logger.info(f'key, pree_time = {key}, {press_time}')

            with serial.Serial(self.serial_device.serial_port.value, self.serial_device.baud_rate, timeout=1) as ser:
                start_time = time.time()
                if key in btnPageRemoconKey:
                    btnPageRemoconKey[key](ser, key, press_time)
                    log = 'ok'
                else:
                    logger.info(f'{key} is not in btnPage')
                    log = f'{key} is not in btnPage'

            event_time = start_time + self.time_offset
            if log == 'ok':
                publish(self.redis_connection, RedisChannel.command, {'msg': 'remocon_response',
                                                                      'data': {"key": key,
                                                                               "type": remocon_type,
                                                                               "press_time": press_time,
                                                                               "sensor_time": event_time}})
            self.error_count = 0
            return event_time

        except Exception as e:
            error_level = 'error' if self.error_count < 3 else 'critical'
            publish(self.redis_connection, RedisChannel.command, {'msg': 'remocon_response',
                                                                  'level': error_level,
                                                                  'data': {"key": key,
                                                                           "type": remocon_type,
                                                                           "press_time": press_time,
                                                                           "log": str(e)}})

            self.error_count += 1
            return -1
