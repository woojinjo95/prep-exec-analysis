import logging
import sqlite3
import os
from typing import Any, List, Tuple

logger = logging.getLogger('connection')


class SqliteConnection():
    def __init__(self, db_name: str):
        self.db_name = os.path.join('datas', f'{db_name}.db')

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_db(self, statement: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            conn.commit()
    
    def save_data(self, statement: str, params: Tuple):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(statement, params)
            conn.commit()
    
    def save_datas(self, statement: str, seq_of_params: List):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(statement, seq_of_params)
            conn.commit()
    
    def load_data(self, statement: str, params: Tuple) -> List[Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(statement, params)
            data = cursor.fetchall()
        return data
