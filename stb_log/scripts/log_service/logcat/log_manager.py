from multiprocessing import Event
import logging
import time

from scripts.log_service.log_collect.collector import collect
from .postprocess import postprocess
from scripts.util.process_maintainer import ProcessMaintainer


logger = logging.getLogger('connection')

class LogFileManager:
    def __init__(self, connection_info: dict, log_type: str):
        # Define ONLY immutable variable or multiprocessing variable
        # DO NOT define mutable variable (will not shared between processes)

        # immutable variable (or will use as immutable)
        self.connection_info = connection_info
        self.log_type = log_type
        
        # multiprocessing variable
        self.local_stop_event = Event()
        self.log_collector = None
        self.log_postprocessor = None

    def get_command_script(self) -> str:
        if self.log_type == 'logcat':
            return 'logcat -c; logcat -v long'
        elif self.log_type == 'top':
            return 'top -b -d 10'
        else:
            raise ValueError(f'Invalid log_type: {self.log_type}')

    # Log Collector
    def __start_log_collector(self):
        self.log_collector = ProcessMaintainer(target=collect, kwargs={
            'connection_info': self.connection_info,
            'command_script': self.get_command_script(),
            'log_type': self.log_type,
            'stop_event': self.local_stop_event,
            }, daemon=True, revive_interval=10)
        self.log_collector.start()

    # Log Postprocessor
    def __start_log_postprocessor(self):
        self.log_postprocessor = ProcessMaintainer(target=postprocess, kwargs={
            'stop_event': self.local_stop_event,
        }, daemon=True, revive_interval=10)
        self.log_postprocessor.start()

    # Control
    def start(self):
        self.local_stop_event.clear()
        self.__start_log_collector()
        self.__start_log_postprocessor()
        logger.info('LogFileManager start')

    def stop(self):
        self.local_stop_event.set()
        self.log_collector.terminate()
        self.log_postprocessor.terminate()
        logger.info('LogFileManager stop')

    def is_alive(self):
        log_alive = self.log_collector.is_alive() if self.log_collector else False
        pp_alive = self.log_postprocessor.is_alive() if self.log_postprocessor else False
        return log_alive and pp_alive

    # WARNING: this method will block the main thread
    # wait until any thread is terminated
    def join(self):
        while self.log_collector.is_alive() and self.log_postprocessor.is_alive():
            time.sleep(1)
