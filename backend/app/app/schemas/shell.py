from typing import List

from app.schemas.enum import LogModuleEnum
from app.schemas.analysis_result import PaginationBaseModel
from pydantic import BaseModel


class Log(BaseModel):
    timestamp: str
    module: LogModuleEnum
    message: str


class ShellLogList(PaginationBaseModel):
    items: List[Log]


class ShellList(BaseModel):
    items: List[dict]
