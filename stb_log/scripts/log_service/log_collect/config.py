from dataclasses import dataclass
from typing import Tuple
import os

@dataclass
class CollectorConfig:
    DUMP_FILESIZE_LIMIT: int = (1024 * 1024 * 1)  # bytes
    # DUMP_TIME_LIMIT: float = 60 * 15  # seconds
    # DUMP_TIME_LIMIT: float = 10
    DUMP_TIME_LIMIT: float = os.getenv("DUMP_TIME_LIMIT")
    LOG_CELL_SPLITER: Tuple[str] = ("[ ", "Timestamp")
    LOG_STREAM_TIMEOUT: int = 1
