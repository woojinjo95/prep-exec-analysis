from multiprocessing import Event

from scripts.log_service.log_collect.collector import collect
from threading import Thread
from scripts.util.process_maintainer import ProcessMaintainer
from .log_save import save


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
            'command_script': 'logcat -v long',
            # 'command_script': 'logcat',
            # 'command_script': 'top -b -d 10',
            'log_type': 'logcat',
            # 'log_type': 'top',
            'stop_event': self.local_stop_event,
            })
        self.log_collector.start()

    # Log Saver
    def __start_log_saver(self):
        self.log_saver = Thread(target=save, kwargs={
            'stop_event': self.local_stop_event,
        })
        self.log_saver.start()

    # Control
    def start(self):
        self.__start_log_collector()
        self.__start_log_saver()

    def stop(self):
        self.local_stop_event.set()