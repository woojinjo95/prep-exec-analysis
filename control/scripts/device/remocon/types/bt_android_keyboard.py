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
from .lcd.lcd_setting import LCDStrings
from operator import attrgetter

logger = logging.getLogger('remocon')

BT = 'bt'
# LCD는 부득이하게 BT를 제어하는 시리얼 장비와 같은 것이 관장해서 임시로 여기에 같이 있음
LCD = 'lcd'


class BTAndroidKeyboard(AbstractRemocon):

    def __init__(self, event_time_dict: DictProxy, serial_device: SerialDevice):

        AbstractRemocon.__init__(self, event_time_dict)
        self.remocon_setting = BTRemoconSetting()
        self.serial_device = serial_device
        self.redis_connection = get_strict_redis_connection()
        self.error_count = 0
        self.time_offset = 0.0005
        self.lcd_functions = LCDStrings()

    # pronto_code 로 직접 리모콘 명령

    def press_key_by_command(self, command_queue: dict) -> float:
        if command_queue.get('type') == 'bt':
            logger.info(f'bt remocon transmit: {command_queue}')
        else:
            # lcd
            pass

        if self.serial_device is None:
            logger.error('Failed to detect bt serial device.')
            raise Exception('Failed to detect bt serial device.')

        key = command_queue['key'].lower()
        press_time = command_queue['press_time']
        remocon_type = command_queue['type']

        try:
            if remocon_type == BT:
                event_time = self.bt_remocon(key, press_time)
            elif remocon_type == LCD:
                self.lcd_command(key)
                event_time = time.time()
        except Exception as e:
            error_level = 'error' if self.error_count < 3 else 'critical'
            publish(self.redis_connection, RedisChannel.command, {'msg': 'remocon_response',
                                                                  'level': error_level,
                                                                  'data': {"key": key,
                                                                           "type": remocon_type,
                                                                           "press_time": press_time,
                                                                           "log": str(e)}})
            self.error_count += 1
            event_time = -1
        finally:
            return event_time

    def bt_remocon(self, key: str, press_time: float):
        logger.info(f'key, press_time = {key}, {press_time}')
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
                                                                           "type": BT,
                                                                           "press_time": press_time,
                                                                           "sensor_time": event_time}})
        self.error_count = 0
        return event_time

    def lcd_command(self, key: str):
        with serial.Serial(self.serial_device.serial_port.value, self.serial_device.baud_rate, timeout=1) as ser:
            func_str, arg = (key.split(':') + [None, None])[:2]
            for string in attrgetter(self.lcd_functions)(func_str)(arg):
                # attrgetter(self.lcd_functions)(func_str)(arg) is same to self.lcd_functions.{func_str}(arg)
                start_time = time.time()  # count last command
                ser.write(string)
            event_time = start_time + self.time_offset

        publish(self.redis_connection, RedisChannel.command, {'msg': 'lcd_control_response',
                                                              'data': {"key": key,
                                                                       "type": LCD,
                                                                       "sensor_time": event_time}})
        self.error_count = 0
        return event_time
