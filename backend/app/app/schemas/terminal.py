from typing import List, Optional

from pydantic import BaseModel


class Terminal(BaseModel):
    class log(BaseModel):
        created_at: str
        command: str
        response: str

    name: str
    logs: List[log]


class TerminalLogList(BaseModel):
    items: List[Terminal.log]


class TerminalList(BaseModel):
    items: List[dict]