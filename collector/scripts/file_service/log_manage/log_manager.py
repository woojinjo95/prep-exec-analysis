import time
from typing import List, Generator
from multiprocessing import Event

from .db_connection import LogManagerDBConnection
from scripts.connection.stb_connection.connector import Connection
from scripts.log_service.log_generate.generate import create_stb_output_channel


class LogFileManager():
    def __init__(self, connection_info: dict, global_stop_event: Event = None):
        self.connection_info = connection_info
        self.local_stop_event = Event()
        self.global_stop_event = global_stop_event
        # set connections
        self.stb_conn = self.__create_stb_connection()
        self.db_conn = self.__create_db_connection()
        self.stb_output = self.__create_stb_output_channel('logcat')

    # Connection factory
    def __create_stb_connection(self) -> Connection:
        return Connection(**self.connection_info)

    def __create_db_connection(self) -> LogManagerDBConnection:
        return LogManagerDBConnection()

    def __create_stb_output_channel(self, command: str) -> Generator[str, None, None]:
        return create_stb_output_channel(command, self.connection_info, [self.local_stop_event, self.global_stop_event])

    # Essential methods
    def save(self, log_line: str):
        self.db_conn.save_data((time.time(), log_line))

    def load_page(self, start: float, end: float, page_number: int=1, page_size: int=1) -> List:
        return self.db_conn.load_data_with_paging(start, end, page_number, page_size)

    def delete(self, start: float, end: float):
        pass
