import logging
from typing import List

from .db_connection import LogManagerDBConnection


logger = logging.getLogger('connection')

db_conn = LogManagerDBConnection()


def load_page(start: float, end: float, page_number: int=1, page_size: int=1) -> List:
    return db_conn.load_data_with_paging(start, end, page_number, page_size)

# def delete(self, start: float, end: float):
#     pass
