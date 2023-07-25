import time
from typing import List

from .db_connection import LogManagerDBConnection
from scripts.connection.stb_connection.connector import Connection


class LogFileManager():
    def __init__(self, connection_info: dict):
        self.connection_info = connection_info
        # set connections
        self.stb_conn = self.__create_stb_connection()
        self.db_conn = self.__create_db_connection()

    # Connection factory
    def __create_stb_connection(self) -> Connection:
        return Connection(**self.connection_info)

    def __create_db_connection(self) -> LogManagerDBConnection:
        return LogManagerDBConnection()

    # Essential methods
    def save(self, log_line: str):
        self.db_conn.save_data((time.time(), log_line))

    def load_page(self, start: float, end: float, page_number: int=1, page_size: int=1) -> List:
        return self.db_conn.load_data_with_paging(start, end, page_number, page_size)

    def delete(self, start: float, end: float):
        pass
