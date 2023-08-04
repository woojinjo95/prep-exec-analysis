import logging
import time
import traceback
from multiprocessing.managers import DictProxy
from threading import Lock
from typing import List

import serial
from scripts.configs.constant import BTRemoconSetting
from scripts.device.serial.serial_device import SerialDevice

from .abstract_remocon import AbstractRemocon
from .bluetooth.bt_key import btnPageRemoconKey

logger = logging.getLogger('remocon')


class BTAndroidKeyboard(AbstractRemocon):

    def __init__(self, event_time_dict: DictProxy, serial_device: SerialDevice):

        AbstractRemocon.__init__(self, event_time_dict)
        self.remocon_setting = BTRemoconSetting()
        self.serial_device = serial_device
        self.time_offset = 0.0005

    # pronto_code 로 직접 리모콘 명령
    def press_key_by_command(self, command_queue: dict) -> float:
        logger.info('bt remocon transmit')
        if self.serial_device is None:
            logger.error('failed to detect serial device.')
            raise Exception('failed to detect serial device.')
        try:
            key = command_queue['key'].lower()
            press_time = command_queue['press_time']
            logger.info(f'key, pree_time = {key}, {press_time}')

            with serial.Serial(self.serial_device.serial_port.value, self.serial_device.baud_rate, timeout=1) as ser:
                start_time = time.time()
                if key in btnPageRemoconKey:
                    btnPageRemoconKey[key](ser, key, press_time)
                else:
                    logger.info(f'{key} is not in btnPage')

            event_time = start_time + self.time_offset
            return event_time

        except Exception as e:
            logger.error(f'Error in consuming command: {e}')
            logger.debug(traceback.format_exc())
            return -1
