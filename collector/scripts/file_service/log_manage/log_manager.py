from typing import List, Tuple

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
    def dump(self, output_path: str):
        pass

    def load(self, start: float, end: float):
        pass

    def delete(self, start: float, end: float):
        pass
