from typing import List, Optional

from pydantic import BaseModel


class Terminal(BaseModel):
    class log(BaseModel):
        created_at: str
        command: str
        response: str

    name: str
    logs: list[log]


class TerminalLogList(BaseModel):
    items: List[Terminal.log]


class TerminalList(BaseModel):
    terminal_names: List[str]