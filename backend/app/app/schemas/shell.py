from typing import List

from app.schemas.enum import LogModuleEnum
from pydantic import BaseModel


class Shell(BaseModel):
    class log(BaseModel):
        timestamp: str
        module: LogModuleEnum
        message: str

    time: str
    mode: str
    shell_id: int
    lines: List[log]


class ShellLogList(BaseModel):
    items: List[Shell.log]


class ShellList(BaseModel):
    items: List[dict]
