import json
import logging
import math
import os
import traceback
from multiprocessing import Event, Manager, Queue, Value
from time import perf_counter_ns
from typing import List, Tuple

from scripts.device.serial.serial_device import SerialDevice
from scripts.utils._multi_process import ProcessUtil
from scripts.utils.common import group_duplicated_value_in_dict
from scripts.utils.file_manage import get_file_dir_path

from .types.abstract_remocon import AbstractRemocon
from .types.bt_android_keyboard import BTAndroidKeyboard
from .types.adb_android_keyboard import ADBAndroidKeyboard
from .types.serial_remocon import SerialRemocon, is_pronto_code_pattern

logger = logging.getLogger('remocon')


class RemoconProcess(ProcessUtil):
    def __init__(self, slot_index: int, serial_devices: Tuple[SerialDevice]):
        ProcessUtil.__init__(self)

        self.start_event = Event()
        self.stop_event = Event()
        self.remocon_id_pointer = Value('i', -1)
        self.slot_index = slot_index
        self.serial_devices = serial_devices
        self.ir_serial_device = self.serial_devices[0]
        self.bt_serial_device = self.serial_devices[1]
        self.manager = Manager()
        self.transmit_command_queue = Queue()
        self.event_time_dict = self.manager.dict()
        self.remocon_commands = self.manager.dict()
        self.remocon_types = {
            'ir': SerialRemocon(self.event_time_dict, self.ir_serial_device),
            'bt': BTAndroidKeyboard(self.event_time_dict, self.bt_serial_device),
            # 'adb': ADBAndroidKeyboard(self.event_time_dict, slot_index),
        }

        # start when remocon is constructed
        for device_thread in self.remocon_types.values():
            device_thread.start()
        self.start()

    def set_remocon_id(self, remocon_id: int):
        if self.remocon_id_pointer.value != remocon_id:
            self.load_remocon_commands_from_id(remocon_id)
            self.remocon_id_pointer.value = remocon_id

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

    def load_remocon_commands_from_id(self, remocon_id: int):
        try:
            self.remocon_commands.clear()  # 초기화

            remocon_id_key = {1: 'sk', 2: 'lg', 3: 'kt', 4: 'playz'}
            pronto_code_path = os.path.join(get_file_dir_path(__file__), 'static/pronto_code.json')
            logger.info(f'Load local preset remocon from {pronto_code_path}, key info: {remocon_id_key}')
            with open(pronto_code_path, 'r', encoding='utf-8') as pronto_code_file:
                key_info_list = json.loads(pronto_code_file.read())
            for name, pronto_code in key_info_list.get(remocon_id_key.get(remocon_id, 4), {}).items():
                self.remocon_commands[name] = pronto_code

            total_key_number = len(self.remocon_commands)
            unique_key_number = len(set(self.remocon_commands.values()))
            if total_key_number > 0:
                logger.info(
                    f'Command number: {total_key_number}, unique count: {unique_key_number}')
                unique_keys_list = group_duplicated_value_in_dict(self.remocon_commands)
                logger.info('Keys: \n' + '\n'.join([f'{idx + 1:{math.ceil(math.log(len(unique_keys_list), 10))}d}: ' + ', '.join(keys)
                            for idx, keys in enumerate(unique_keys_list)]))
            else:
                logger.error(f'Remocon id {remocon_id} has no remocon valid key in list.')

        except Exception as e:
            logger.error(f'Fail to load ir lists {e}')

            # TODO custom exception
            raise Exception('Fail to load ir lists')
