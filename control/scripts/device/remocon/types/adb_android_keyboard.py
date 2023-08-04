import logging
import traceback
from multiprocessing.managers import DictProxy

from .abstract_remocon import AbstractRemocon
from .adb_remocon.adb_remocon import transmit_adb

logger = logging.getLogger('remocon')


class ADBAndroidKeyboard(AbstractRemocon):

    def __init__(self, event_time_dict: DictProxy, slot_index: int):

        AbstractRemocon.__init__(self, event_time_dict)
        self.slot_index = slot_index

    # pronto_code 로 직접 리모콘 명령
    def press_key_by_command(self, command_queue: dict) -> float:
        try:
            key = command_queue['key']
            # pronto_code = command_queue['code']
            # press_time = command_queue['press_time']

            event_time = transmit_adb(self.slot_index, key)

            return event_time

        except Exception as e:
            logger.error(f'Error in consuming command: {e}')
            logger.debug(traceback.format_exc())
            return -1
