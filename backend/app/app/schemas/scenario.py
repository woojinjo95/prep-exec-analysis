from typing import List, Optional

from app.schemas.block import BlockGroup
from pydantic import BaseModel, root_validator
from pydantic.datetime_parse import parse_datetime


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
    updated_at: str

    @root_validator(pre=True)
    def convert_timestamp_with_timezone(cls, values):
        if "updated_at" in values:
            values["updated_at"] = parse_datetime(values["updated_at"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return values


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
