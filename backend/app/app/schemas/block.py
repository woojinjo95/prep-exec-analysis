from typing import List, Optional

from app.schemas.enum import BlockTypeEnum
from pydantic import BaseModel


class BlockCreate(BaseModel):
    type: BlockTypeEnum
    name: str
    value: str
    delay_time: float = 3000  # ms단위


class BlockDelete(BaseModel):
    block_ids: List[str]


class Block(BlockCreate):
    id: str


class BlockUpdate(BaseModel):
    type: Optional[BlockTypeEnum]
    name: Optional[str]
    value: Optional[str]
    delay_time: Optional[float]


class BlockGroupUpdate(BaseModel):
    repeat_cnt: Optional[int] = 1


class BlockGroup(BaseModel):
    id: str
    repeat_cnt: int
    block: List[Block]