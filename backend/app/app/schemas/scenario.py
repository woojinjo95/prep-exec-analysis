from typing import Optional, List

from pydantic import BaseModel


class BlockCreate(BaseModel):
    type: str
    value: str
    delay_time: float


class Block(BaseModel):
    id: str
    type: str
    value: str
    delay_time: float


class BlockUpdate(BaseModel):
    type: Optional[str]
    value: Optional[str]
    delay_time: Optional[float]


class BlockGroup(BaseModel):
    id: str
    repeat_cnt: int
    block: List[Block]


class ScenarioBase(BaseModel):
    block_group: Optional[List[BlockGroup]]


class Scenario(BaseModel):
    items: List[ScenarioBase]
