import logging
import time
import traceback
from abc import ABCMeta, abstractmethod
from multiprocessing.managers import DictProxy
from multiprocessing import Queue
from threading import Event, Thread

from scripts.configs.constant import RemoconSetting

logger = logging.getLogger('remocon')


# 리모콘 인터페이스 정의
class AbstractRemocon(metaclass=ABCMeta):

    def __init__(self, event_time_dict: DictProxy):
        self.stop_flag = Event()
        self.command_queue = Queue()
        self.remocon_setting = RemoconSetting()
        self.event_time_dict = event_time_dict
        self.default_interval = 0.2

    # pronto code를 이용한 명령 송신

    def put_command(self, command_queue: dict):
        self.command_queue.put(command_queue)

    def consume(self):
        command_queue = self.command_queue.get()
        # wait until value get
        start_time = time.monotonic()
        if not command_queue.get('mute'):
            logger.debug(f'command_queue accepted: {command_queue}')

        interval = command_queue.get('sleep', 0)
        _id = command_queue.get('id', 'default')
        event_time = self.press_key_by_command(command_queue)
        self.event_time_dict[_id] = event_time
        if not command_queue.get('mute'):
            logger.debug(f'event_time has been get, {_id}: {event_time}')

        process_time = time.monotonic() - start_time
        time.sleep(max(0, max(self.default_interval, interval) - process_time))

    def run(self):
        while not self.stop_flag.is_set():
            try:
                self.consume()
            except Exception as e:
                logger.error(f'Error in consuming command: {e}')
                logger.debug(traceback.format_exc())

    def start(self):
        # Thread로 무한 수신, 
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    @abstractmethod
    def press_key_by_command(self, command_queue: dict) -> float:
        """ 
        command queue 를 이용한 통합 수신
            {'key': 'channelup',
            'code': '0000 006e ..... ',
            'id': ir_177246.226097541,
            'press': 2,
            'sleep': 2.3, 
            'type': 'ir'}
        """
        pass
