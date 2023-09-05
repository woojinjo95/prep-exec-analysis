from typing import List

from app.schemas.enum import LogModuleEnum, ShellModeEnum
from pydantic import BaseModel, root_validator
from pydantic.datetime_parse import parse_datetime


class TimestampBaseModel(BaseModel):
    timestamp: str

    @root_validator(pre=True)
    def convert_timestamp_with_timezone(cls, values):
        if "timestamp" in values:
            values["timestamp"] = parse_datetime(values["timestamp"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return values


class Log(TimestampBaseModel):
    module: LogModuleEnum
    message: str


class Shell(TimestampBaseModel):
    mode: ShellModeEnum
    shell_id: int
    lines: List[Log]


class ShellLogList(BaseModel):
    items: List[Log]


class ShellList(BaseModel):
    items: List[dict]
