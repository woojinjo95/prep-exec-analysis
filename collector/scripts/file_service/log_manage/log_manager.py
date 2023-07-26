from typing import List
from multiprocessing import Event

from scripts.log_service.log_collect.collector import collect
from scripts.util.process_maintainer import ProcessMaintainer
from scripts.file_service.log_manage.save import save


class LogFileManager():
    def __init__(self, connection_info: dict, global_stop_event: Event = None):
        # Define ONLY immutable variable or multiprocessing variable
        # DO NOT define mutable variable (will not shared between processes)

        # immutable variable (or will use as immutable)
        self.connection_info = connection_info
        
        # multiprocessing variable
        self.global_stop_event = global_stop_event

    # Log Collector
    def __start_log_collector(self):
        self.log_collector = ProcessMaintainer(target=collect, kwargs={
            'connection_info': self.connection_info,
            'command_script': 'logcat -v long',
            'log_type': 'logcat'
            }, revive_interval=10)
        self.log_collector.start()

    def __stop_log_collector(self):
        self.log_collector.stop()

    # Log Saver
    def __start_log_saver(self):
        self.log_saver = ProcessMaintainer(target=save, revive_interval=10)
        self.log_saver.start()

    def __stop_log_saver(self):
        self.log_saver.stop()

    # Control
    def start(self):
        self.__start_log_collector()
        self.__start_log_saver()

    def stop(self):
        self.__stop_log_collector()
        self.__stop_log_saver()

    # def load_page(self, start: float, end: float, page_number: int=1, page_size: int=1) -> List:
    #     return self.db_conn.load_data_with_paging(start, end, page_number, page_size)

    # def delete(self, start: float, end: float):
    #     pass
