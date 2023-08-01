from multiprocessing import Event
import logging
import time

from scripts.log_service.log_collect.collector import collect
from threading import Thread
from .postprocess import postprocess


logger = logging.getLogger('connection')

class LogFileManager():
    def __init__(self, connection_info: dict):
        # Define ONLY immutable variable or multiprocessing variable
        # DO NOT define mutable variable (will not shared between processes)

        # immutable variable (or will use as immutable)
        self.connection_info = connection_info
        
        # multiprocessing variable
        self.local_stop_event = Event()

    # Log Collector
    def __start_log_collector(self):
        self.log_collector = Thread(target=collect, kwargs={
            'connection_info': self.connection_info,
            'command_script': 'logcat -c; logcat -v long',
            # 'command_script': 'logcat',
            # 'command_script': 'top -b -d 10',
            'log_type': 'logcat',
            # 'log_type': 'top',
            'stop_event': self.local_stop_event,
            }, daemon=True)
        self.log_collector.start()

    # Log Postprocessor
    def __start_log_postprocessor(self):
        self.log_postprocessor = Thread(target=postprocess, kwargs={
            'stop_event': self.local_stop_event,
        }, daemon=True)
        self.log_postprocessor.start()

    # Control
    def start(self):
        self.__start_log_collector()
        self.__start_log_postprocessor()
        logger.info('LogFileManager start')

    def stop(self):
        self.local_stop_event.set()
        logger.info('LogFileManager stop')

    # wait until any thread is terminated
    def join(self):
        while self.log_collector.is_alive() and self.log_postprocessor.is_alive():
            time.sleep(1)
