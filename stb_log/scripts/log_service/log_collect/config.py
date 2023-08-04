from dataclasses import dataclass
from typing import Tuple
from scripts.config.config import get_setting_with_env

@dataclass
class CollectorConfig:
    DUMP_FILESIZE_LIMIT: int = (1024 * 1024 * 1)  # bytes
    # DUMP_TIME_LIMIT: float = 60 * 15  # seconds
    # DUMP_TIME_LIMIT: float = 10
    DUMP_TIME_LIMIT: float = get_setting_with_env("DUMP_TIME_LIMIT")
    LOG_CELL_SPLITER: Tuple[str] = ("[ ", "Timestamp")
    LOG_STREAM_TIMEOUT: int = 1
