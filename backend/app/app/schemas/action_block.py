from typing import Optional

from pydantic import BaseModel


class ActionBlockCreateBase(BaseModel):
    type: str
    value: str
    delay_time: float


class ActionBlockCreate(BaseModel):
    id: str
    type: str
    value: str
    sort_idx: int
    delay_time: float
    group_id: str


class ActionBlockUpdate(BaseModel):
    type: Optional[str]
    value: Optional[str]
    delay_time: Optional[float]


class ActionBlock(BaseModel):
    id: str
    sort_idx: int
