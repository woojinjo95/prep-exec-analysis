from typing import List, Optional

from app.schemas.block import BlockGroup
from pydantic import BaseModel


class CopyScenarioCreate(BaseModel):
    src_scenario_id: str
    name: str
    tags: Optional[List[str]] = []
    block_group: Optional[List[BlockGroup]]


class ScenarioCreate(BaseModel):
    is_active: Optional[bool] = False
    name: Optional[str]
    tags: Optional[List[str]]
    block_group: Optional[List[BlockGroup]]


class ScenarioCreateResult(BaseModel):
    msg: str
    id: str
    testrun_id: str


class ScenarioUpdate(BaseModel):
    is_active: bool
    name: str
    tags: Optional[List[str]] = []
    block_group: List[BlockGroup]


class ScenarioBlock(BaseModel):
    id: str
    name: str
    tags: Optional[List[str]] = []
    is_active: bool
    block_group: List[BlockGroup]


class Scenario(BaseModel):
    items: ScenarioBlock


class ScenarioSummary(BaseModel):
    id: str
    name: str
    tags: Optional[List[str]]
    testrun_count: int
    has_block: bool
    updated_at: Optional[str]


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


class TestrunBase(BaseModel):
    id: str
    measure_targets: List[str]
    updated_at: Optional[str]


class Testrun(BaseModel):
    items: List[TestrunBase]


class TestrunUpdate(BaseModel):
    is_active: bool
