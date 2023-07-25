import logging
import sqlite3
import os
from typing import Any, List, Tuple

logger = logging.getLogger('connection')


class SqliteConnection():
    def __init__(self, db_name: str):
        self.db_name = os.path.join('datas', f'{db_name}.db')

    def create_db(self, statement: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(statement)
        conn.commit()
        conn.close()
    
    def save_data(self, statement: str, params: Tuple):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(statement, params)
        conn.commit()
        conn.close()
    
    def save_datas(self, statement: str, seq_of_params: List):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.executemany(statement, seq_of_params)
        conn.commit()
        conn.close()
    
    def load_data(self, statement: str, params: Tuple) -> List[Any]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(statement, params)
        data = cursor.fetchall()
        conn.close()
        return data
    
