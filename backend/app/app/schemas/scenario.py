from typing import List, Optional

from app.schemas.block import BlockGroup
from pydantic import BaseModel, root_validator
from pydantic.datetime_parse import parse_datetime


class TimestampBaseModel(BaseModel):
    updated_at: Optional[str]

    @root_validator(pre=True)
    def convert_timestamp_with_timezone(cls, values):
        if "updated_at" in values:
            values["updated_at"] = parse_datetime(values["updated_at"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return values


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


class ScenarioSummary(TimestampBaseModel):
    id: str
    name: str
    tags: Optional[List[str]]
    testrun_count: int
    has_block: bool


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


class TestrunBase(TimestampBaseModel):
    id: str
    measure_targets: List[str]


class Testrun(BaseModel):
    items: List[TestrunBase]
