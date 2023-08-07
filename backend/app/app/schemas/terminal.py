from typing import List, Optional

from pydantic import BaseModel


class Terminal(BaseModel):
    class log(BaseModel):
        created_at: str
        log: str

    name: str
    logs: list[log]


class TerminalLogsPage(BaseModel):
    total: Optional[int]
    pages: Optional[int]
    prev: Optional[int]
    next: Optional[int]
    items: List[Terminal.log]


class TerminalList(BaseModel):
    terminal_names: List[dict]