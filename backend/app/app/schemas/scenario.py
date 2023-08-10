from typing import List, Optional

from app.schemas.block import BlockGroup
from pydantic import BaseModel


class ScenarioBase(BaseModel):
    name: str
    tags: Optional[List[str]]
    updated_at: float
    block_group: List[BlockGroup]


class ScenarioUpdate(BaseModel):
    block_group: List[BlockGroup]


class Scenario(BaseModel):
    items: Optional[ScenarioBase]
