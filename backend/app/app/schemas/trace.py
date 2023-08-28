from typing import List

from app.schemas.enum import LogLevelEnum, ProtocolEnum
from pydantic import BaseModel, root_validator
from pydantic.datetime_parse import parse_datetime


class TimestampBaseModel(BaseModel):
    timestamp: str

    @root_validator(pre=True)
    def convert_timestamp_with_timezone(cls, values):
        if "timestamp" in values:
            values["timestamp"] = parse_datetime(values["timestamp"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return values


class Logcat(TimestampBaseModel):
    module: str
    log_level: LogLevelEnum
    process_name: str
    pid: int
    tid: int
    message: str


class ReadLogcat(BaseModel):
    items: List[Logcat]


class Network(TimestampBaseModel):
    src: str
    dst: str
    protocol: ProtocolEnum
    length: int
    info: str


class ReadNetwork(BaseModel):
    items: List[Network]
