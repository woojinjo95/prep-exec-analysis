from typing import List, Optional

from app.schemas.enum import StbConnectionTypeEnum
from pydantic import BaseModel


class StbConnectionCreate(BaseModel):
    connection_type: StbConnectionTypeEnum
    ip: str
    port: str
    username: Optional[str]
    password: Optional[str]


class StbConnection(StbConnectionCreate):
    id: str


class StbConnectionBase(BaseModel):
    items: List[StbConnection]
