import time
from typing import List, Generator
from multiprocessing import Event, Queue

from .db_connection import LogManagerDBConnection
from scripts.connection.stb_connection.connector import Connection
from scripts.log_service.log_generate.generate import create_stb_output_channel
from scripts.log_service.log_collect.collector import collect
from scripts.log_service.log_collect.save import save
from scripts.util.process_maintainer import ProcessMaintainer


class LogFileManager():
    def __init__(self, connection_info: dict, global_stop_event: Event = None):
        self.connection_info = connection_info
        self.local_stop_event = Event()
        self.global_stop_event = global_stop_event
        self.upload_queue = Queue(maxsize=1000)
        self.is_running = Event()
        # set connections
        # self.stb_conn = self.__create_stb_connection()
        self.db_conn = self.__create_db_connection()
        # self.stb_output = self.__create_stb_output_channel('logcat')

        # start modules
        self.__start_log_collector()
        self.__start_log_saver()

    # Connection factory
    def __create_stb_connection(self) -> Connection:
        return Connection(**self.connection_info)

    def __create_db_connection(self) -> LogManagerDBConnection:
        return LogManagerDBConnection()

    def __create_stb_output_channel(self, command: str) -> Generator[str, None, None]:
        return create_stb_output_channel(command, self.connection_info, [self.local_stop_event, self.global_stop_event])

    # Modules
    def __start_log_collector(self):
        log_collector = ProcessMaintainer(func=collect, kwargs={
            'connection_info': self.connection_info,
            'command_script': 'logcat -v long',
            'log_type': 'logcat',
            'stop_events': [self.local_stop_event, self.global_stop_event],
            }, revive_interval=10)
        log_collector.start()

    def __start_log_saver(self):
        log_saver = ProcessMaintainer(func=save, kwargs={
            'stop_events': [self.local_stop_event, self.global_stop_event],
            }, revive_interval=10)
        log_saver.start()

    # Essential methods
    def save(self, log_line: str):
        self.db_conn.save_data((time.time(), log_line))

    def load_page(self, start: float, end: float, page_number: int=1, page_size: int=1) -> List:
        return self.db_conn.load_data_with_paging(start, end, page_number, page_size)

    def delete(self, start: float, end: float):
        pass
