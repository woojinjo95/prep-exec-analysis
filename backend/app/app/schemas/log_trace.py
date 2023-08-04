from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class Logcat(BaseModel):
    timestamp: datetime
    module: str
    log_level: str
    process_name: str
    PID: int
    TID: int
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


class NetworkPage(BaseModel):
    total: Optional[int]
    pages: Optional[int]
    prev: Optional[int]
    next: Optional[int]
    items: List[Network]