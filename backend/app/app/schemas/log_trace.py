from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class Logcat(BaseModel):
    timestamp: datetime
    PID: int
    TID: int
    process_name: str
    log_level: str
    module: Optional[str]
    message: str


class LogcatPage(BaseModel):
    total: Optional[int]
    pages: Optional[int]
    prev: Optional[int]
    next: Optional[int]
    items: List[Logcat]


class Network(BaseModel):
    timestamp: datetime
    source: str
    destination: str
    protocol: str
    length: int
    info: str


class NetworkPage(BaseModel):
    total: Optional[int]
    pages: Optional[int]
    prev: Optional[int]
    next: Optional[int]
    items: List[Network]