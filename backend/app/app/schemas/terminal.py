from typing import List

from pydantic import BaseModel


class Terminal(BaseModel):
    class log(BaseModel):
        timestamp: str
        module: str
        message: str

    time: str
    mode: str
    lines: List[log]


class TerminalLogList(BaseModel):
    items: List[Terminal.log]


class TerminalList(BaseModel):
    items: List[dict]