from typing import List, Tuple
import logging

from scripts.connection.sqlite import SqliteConnection


logger = logging.getLogger('logcat')

class LogManagerDBConnection(SqliteConnection):
    def __init__(self):
        super().__init__(db_name='log_file_manager')
        self.table_name = 'log_data'
        # create db
        self.create_db()

    # File manager methods
    def create_db(self):
        super().create_db(f'''CREATE TABLE IF NOT EXISTS {self.table_name} 
                               (timestamp real, content text)''')
        logger.info(f"Create {self.table_name} table")

    def save_data(self, text: Tuple[float, str]):
        super().save_data(f"INSERT INTO {self.table_name} VALUES (?,?)", text)
        logger.info(f"Save 1 data")

    def save_datas(self, texts: List[Tuple[float, str]]):
        super().save_datas(f"INSERT INTO {self.table_name} VALUES (?,?)", texts)
        logger.info(f"Save {len(texts)} datas")

    def load_data(self, start: float, end: float) -> List[Tuple[float, str]]:
        logger.info(f"Load data")
        return super().load_data(f"SELECT * FROM {self.table_name} WHERE timestamp BETWEEN ? AND ?", (start, end))

    def load_data_with_paging(self, start: float, end: float, page_number: int=1, page_size: int=1) -> List[Tuple[float, str]]:
        logger.info(f"Load data with paging")
        return super().load_data_with_paging(f"SELECT * FROM {self.table_name} WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp", (start, end), page_number, page_size)
