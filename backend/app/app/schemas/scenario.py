from datetime import datetime
from typing import List, Optional

from app.schemas.block import BlockGroup
from pydantic import BaseModel


class ScenarioCreate(BaseModel):
    is_active: bool
    name: Optional[str]
    tags: Optional[List[str]]
    block_group: Optional[List[BlockGroup]]


class ScenarioUpdate(ScenarioCreate):
    block_group: List[BlockGroup]


class ScenarioBlock(BaseModel):
    id: str
    block_group: List[BlockGroup]


class Scenario(BaseModel):
    items: ScenarioBlock


class ScenarioSummary(BaseModel):
    id: str
    name: str
    tags: Optional[List[str]]
    updated_at: datetime


class ScenarioPage(BaseModel):
    total: Optional[int]
    pages: Optional[int]
    prev: Optional[int]
    next: Optional[int]
    items: List[ScenarioSummary]


class ScenarioTagBase(BaseModel):
    tags: Optional[List[str]]


class ScenarioTag(BaseModel):
    items: ScenarioTagBase


class ScenarioTagUpdate(BaseModel):
    tag: str
