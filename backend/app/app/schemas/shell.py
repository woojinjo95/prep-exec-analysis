from typing import List

from app.schemas.analysis_result import TimestampBaseModel
from app.schemas.enum import LogModuleEnum, ShellModeEnum
from pydantic import BaseModel


class Log(TimestampBaseModel):
    module: LogModuleEnum
    message: str


class Shell(TimestampBaseModel):
    mode: ShellModeEnum
    lines: List[Log]


class ShellLogList(BaseModel):
    items: List[Log]


class ShellList(BaseModel):
    items: List[dict]
