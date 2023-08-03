from .abstract_remocon import AbstractRemocon
import logging
import traceback
from multiprocessing.managers import DictProxy
import re

from scripts.configs.constant import SerialRemoconSetting
from scripts.device.serial.serial_device import SerialDevice

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

    # pronto_code 로 직접 리모콘 명령
    def press_key_by_command(self, command_queue: dict) -> float:
        logger.info(f'ir remocon transmit: {command_queue}')
        if self.serial_device is None:
            logger.error('failed to detect serial device.')
            raise Exception('failed to detect serial device.')

        try:
            # key = command_queue['key']
            # ir remocon does not use 'key' itself, just use pronto code
            pronto_code = command_queue['code']
            press_time = command_queue['press_time']

            get_event_time = True
            event_time = self.serial_device.transmit_ir(pronto_code, press_time=press_time, serial_get_event_time=get_event_time)
            return event_time

        except Exception as e:
            logger.error(f'Error in consuming command: {e}')
            logger.debug(traceback.format_exc())
            return -1
