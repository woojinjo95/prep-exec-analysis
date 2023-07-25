import logging
import sqlite3
from abc import ABCMeta, abstractmethod
from typing import Any, List, Tuple

logger = logging.getLogger('connection')


# make singleton
class SqliteConnection(metaclass=ABCMeta):
    def __init__(self, db_name: str):
        self.db_name = f'{db_name}.db'
        self.conn = sqlite3.connect(db_name)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def __del__(self):
        if self.conn:
            self.conn.close()

    @abstractmethod
    def create_db(self, statement: str):
        cursor = self.conn.cursor()
        cursor.execute(statement)
        self.conn.commit()
        self.conn.close()
    
    @abstractmethod
    def save_data(self, statement: str, params: Tuple):
        cursor = self.conn.cursor()
        cursor.execute(statement, params)
        self.conn.commit()
        self.conn.close()
    
    @abstractmethod
    def save_datas(self, statement: str, seq_of_params: List):
        cursor = self.conn.cursor()
        cursor.executemany(statement, seq_of_params)
        self.conn.commit()
        self.conn.close()
    
    @abstractmethod
    def load_data(self, statement: str, params: Tuple) -> List[Any]:
        cursor = self.conn.cursor()
        cursor.execute(statement, params)
        data = cursor.fetchall()
        self.conn.close()
        return data
