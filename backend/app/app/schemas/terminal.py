from typing import List

from pydantic import BaseModel
from app.schemas.enum import LogModuleEnum


class Terminal(BaseModel):
    class log(BaseModel):
        timestamp: str
        module: LogModuleEnum
        message: str

    time: str
    mode: str
    shell_id: str
    lines: List[log]


class TerminalLogList(BaseModel):
    items: List[Terminal.log]


class TerminalList(BaseModel):
    items: List[dict]