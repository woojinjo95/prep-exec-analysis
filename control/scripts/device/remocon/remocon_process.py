import logging
import math
import traceback
from multiprocessing import Event, Manager, Queue
from time import perf_counter_ns
from typing import List, Tuple

from scripts.device.serial.serial_device import SerialDevice
from scripts.utils._multi_process import ProcessUtil
from scripts.utils.common import group_duplicated_value_in_dict

from ...configs.config import get_value
from ...configs.constant import RedisDBEnum
from ...connection.redis_connection import (get_redis_key_list,
                                            get_strict_redis_connection)
from .types.abstract_remocon import AbstractRemocon
from .types.adb_android_keyboard import ADBAndroidKeyboard
from .types.bt_android_keyboard import BTAndroidKeyboard
from .types.serial_remocon import SerialRemocon, is_pronto_code_pattern

logger = logging.getLogger('remocon')


class RemoconProcess(ProcessUtil):
    def __init__(self, serial_devices: Tuple[SerialDevice]):
        ProcessUtil.__init__(self)

        self.start_event = Event()
        self.stop_event = Event()
        self.serial_devices = serial_devices
        self.ir_serial_device = self.serial_devices[0]
        self.bt_serial_device = self.serial_devices[1]

        self.init_multiprocess_objects()

        self.remocon_types = {
            'ir': SerialRemocon(self.event_time_dict, self.ir_serial_device),
            'bt': BTAndroidKeyboard(self.event_time_dict, self.bt_serial_device),
            # 'adb': ADBAndroidKeyboard(self.event_time_dict, slot_index),
        }

        # start when remocon is constructed
        for device_thread in self.remocon_types.values():
            device_thread.start()
        self.start()

    def init_multiprocess_objects(self):
        self.manager = Manager()
        self.transmit_command_queue = Queue()
        self.event_time_dict = self.manager.dict()
        self.configs = self.manager.dict()
        self.remocon_commands = self.manager.dict()
        self.remocon_name_list = [el.split(':')[1]
                                  for el
                                  in get_redis_key_list(get_strict_redis_connection(db=RedisDBEnum.hardware), 'remocon:*')]
        self.configs['remocon_name'] = ''
        self.set_remocon_model(self.remocon_name_list[0])

    def set_remocon_model(self, remocon_name: str):
        if self.configs['remocon_name'] != remocon_name:
            self.load_remocon_commands_from_name(remocon_name)
            self.configs['remocon_name'] = remocon_name

    def put_command(self, key: str, _type: str, code: str = '', sleep: float = 0, press_time: float = 0) -> str:
        _id = f'{_type}_{perf_counter_ns()}'

        if not is_pronto_code_pattern(code) and _type == 'ir':
            # '키'가 아닌 pronto_code가 필요한 것은 ir, bt, adb 중 ir이 유일하며, 나머지 2개는 사실상 키보드라 통신사마다 다르지 않음
            # 만약 다른 코드를 관리할 필요성이 생기면 여기서 분리할 것.
            code = self.remocon_commands[key.lower()]

        command = {'key': key,
                   'code': code,
                   'id': _id,
                   'press_time': press_time,
                   'sleep': sleep,
                   'type': _type}
        self.transmit_command_queue.put(command)
        return _id

    def press_key_by_commands(self, command_queue: dict):
        """
            {'key': 'channelup',
            'code': '0000 006e ..... ',
            'id': ir_177246.226097541,
            'press': 2,
            'interval': 2.3, 
            'type': 'ir'}
        """
        remocon_type = command_queue.get('type', '')
        if remocon_type not in self.remocon_types.keys():
            logger.error(f'{remocon_type} is not support!')

        def get_remocon_device(remocon_type: str) -> AbstractRemocon:
            # dict obj를 AbstractRemocon 로 지정해서 type hint를 보여주기 위한 함수로, 그 이상의 의미 없음
            return self.remocon_types[remocon_type]

        remocon_device = get_remocon_device(remocon_type)
        remocon_device.put_command(command_queue)

    def clear_event_time_dict(self):
        self.event_time_dict.clear()

    def run(self):
        try:
            while not self.stop_event.is_set():
                if not self.start_event.is_set():
                    self.start_event.set()
                command_queue = self.get_queue(self.transmit_command_queue)
                self.press_key_by_commands(command_queue)

        except Exception as e:
            logger.error(f'RemoconProcess raise error => {e}')
            logger.info(traceback.format_exc())
        finally:
            self.release()

    def stop(self):
        self.stop_queue(self.transmit_command_queue)
        self.stop_event.set()

    def release(self):
        self.clear_queue(self.transmit_command_queue)
        self.transmit_command_queue.close()
        logger.info(f'RemoconProcess Terminated.')

    def load_remocon_commands_from_name(self, remocon_name: str):
        try:
            self.remocon_commands.clear()  # 초기화
            logger.info(f'Get remocon model: {remocon_name}')
            remocon_codes = get_value(f'remocon:{remocon_name}', 'remocon_codes', db=RedisDBEnum.hardware)

            if len(remocon_codes) == 0:
                return

            for remocon_code in remocon_codes:
                name = remocon_code['name'].lower()
                code_name = remocon_code['code_name'].lower()
                pronto_code = remocon_code['pronto_code']

                self.remocon_commands[name] = pronto_code
                self.remocon_commands[code_name] = pronto_code

            total_key_number = len(self.remocon_commands)
            unique_key_number = len(set(self.remocon_commands.values()))
            if total_key_number > 0:
                logger.info(
                    f'Command number: {total_key_number}, unique count: {unique_key_number}')
                unique_keys_list = group_duplicated_value_in_dict(self.remocon_commands)
                logger.debug('Keys: \n' + '\n'.join([f'{idx + 1:{math.ceil(math.log(len(unique_keys_list), 10))}d}: ' + ', '.join(keys)
                                                     for idx, keys in enumerate(unique_keys_list)]))
            else:
                logger.error(f'Remocon id {remocon_name} has no remocon valid key in list.')

        except Exception as e:
            logger.error(f'Fail to load ir lists {e}')

            # TODO custom exception
            raise Exception('Fail to load ir lists')
