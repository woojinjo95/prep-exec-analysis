from typing import List, Tuple
from datetime import datetime
from ..file_manager import FileManager
from scripts.connection.stb_connection.connector import Connection
from scripts.connection.sqlite import SqliteConnection


class LogFileManager(FileManager):
    def __init__(self, connection_info: dict):
        self.connection_info = connection_info
        self.db_name = 'log_file_manager'
        
        # set connections
        self.stb_conn = self.create_stb_connection()
        self.db_conn = self.create_db_connection()

    # Connection factory
    def create_stb_connection(self) -> Connection:
        return Connection(**self.connection_info)

    def create_db_connection(self) -> SqliteConnection:
        return SqliteConnection(self.db_name)

    # File manager methods
    def create_db(self):
        self.db_conn.create_db('''CREATE TABLE IF NOT EXISTS log_data
                                (timestamp real, content text)''')

    def save_datas(self, texts: List[Tuple[float, str]]):
        self.db_conn.save_datas("INSERT INTO log_data VALUES (?,?)", texts)

    def load_data(self, start: float, end: float) -> List[Tuple[float, str]]:
        return self.db_conn.load_data("SELECT * FROM log_data WHERE timestamp BETWEEN ? AND ?", (start, end))

    # Essential methods
    def dump(self, output_path: str):
        pass

    def load(self, start: float, end: float):
        pass

    def delete(self, start: float, end: float):
        pass
