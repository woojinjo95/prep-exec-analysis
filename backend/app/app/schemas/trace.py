from typing import List

# from app.schemas.analysis_result import TimestampBaseModel
from app.schemas.enum import LogLevelEnum, ProtocolEnum
from pydantic import BaseModel


class Logcat(BaseModel):
    timestamp: str
    module: str
    log_level: LogLevelEnum
    process_name: str
    pid: int
    tid: int
    message: str


class ReadLogcat(BaseModel):
    items: List[Logcat]


class Network(BaseModel):
    timestamp: str
    src: str
    dst: str
    protocol: ProtocolEnum
    length: int
    info: str


class ReadNetwork(BaseModel):
    items: List[Network]
