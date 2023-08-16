from typing import List, Optional

from app.schemas.block import BlockGroup
from pydantic import BaseModel


class TestrunVideo(BaseModel):
    created_at: float
    path: str
    name: str


class TestrunRaw(BaseModel):
    videos: Optional[List[TestrunVideo]]


class TestrunAnalysis(BaseModel):
    videos: Optional[List[TestrunVideo]]


class Testrun(BaseModel):
    dir: str
    raw: TestrunRaw
    analysis: TestrunAnalysis


class ScenarioBase(BaseModel):
    id: str
    name: str
    tags: Optional[List[str]]
    updated_at: float
    block_group: List[BlockGroup]
    testrun: Testrun


class ScenarioCreate(BaseModel):
    name: Optional[str]
    tags: Optional[List[str]]


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
    updated_at: float


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
