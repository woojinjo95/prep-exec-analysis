from typing import Optional, List

from pydantic import BaseModel


class BlockCreate(BaseModel):
    type: str
    value: str
    delay_time: float = 3000  # ms단위


class BlockDelete(BaseModel):
    block_ids: List[str]


class Block(BlockCreate):
    id: str


class BlockUpdate(BaseModel):
    type: Optional[str]
    value: Optional[str]
    delay_time: Optional[float]


class BlockGroupUpdate(BaseModel):
    repeat_cnt: Optional[int]


class BlockGroup(BaseModel):
    id: str
    repeat_cnt: int
    block: List[Block]
