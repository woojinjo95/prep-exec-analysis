import logging
import sqlite3
import os
from typing import Any, List, Tuple

logger = logging.getLogger('connection')


class SqliteConnection():
    def __init__(self, db_name: str):
        self.output_dir = os.path.join('datas', 'db')
        os.makedirs(self.output_dir, exist_ok=True)
        self.db_name = os.path.join(self.output_dir, f'{db_name}.db')

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

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

    # If you want to get the next page of data, you can simply call this function again, but with page_number incremented by 1.
    # Each time you call load_data_with_paging with page_number incremented, it retrieves the next page of data. If there are no more pages, the function will return an empty list.
    def load_data_with_paging(self, statement: str, params: Tuple, page_number: int=1, page_size: int=1):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            offset = (page_number - 1) * page_size
            cursor.execute(
                f"{statement} LIMIT ? OFFSET ?",
                (*params, page_size, offset)
            )
            data = cursor.fetchall()
            return data
