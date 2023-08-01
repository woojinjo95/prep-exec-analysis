from typing import List, Optional

from app.schemas.block import BlockGroup
from pydantic import BaseModel


class ScenarioBase(BaseModel):
    block_group: Optional[List[BlockGroup]]


class Scenario(BaseModel):
    items: ScenarioBase
