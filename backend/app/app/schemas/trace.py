from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from schemas.enum import LogLevelFinderTargetEnum

class Logcat(BaseModel):
    timestamp: datetime
    module: str
    log_level: LogLevelFinderTargetEnum
    process_name: str
    pid: int
    tid: int
    message: str


class ReadLogcat(BaseModel):
    items: List[Logcat]


class Network(BaseModel):
    timestamp: datetime
    source: str
    destination: str
    protocol: str
    length: int
    info: str


class ReadNetwork(BaseModel):
    items: List[Network]