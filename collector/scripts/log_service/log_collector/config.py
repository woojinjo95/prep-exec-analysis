from dataclasses import dataclass
from typing import List


@dataclass
class CollectorConfig:
    # for process maintainer
    PROCESS_CHECK_INTERVAL: int = 10

    # collector parameters
    SESSION_UPDATE_CHUNK_CNT: int = 20
    DUMP_FILESIZE_LIMIT: int = (1024 * 1024 * 1)  # bytes
    DUMP_TIME_LIMIT: float = 60 * 15  # seconds
    LOG_CELL_SPLITER: List = ['[ ', 'Timestamp']
    LOG_STREAM_TIMEOUT: int = 1

    # uploader parameters
    UPLOAD_TRY_COUNT: int = 10
    UPLOAD_TIMEOUT: int = 60
