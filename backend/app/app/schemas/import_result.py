from datetime import datetime
from typing import List, Optional

from app.schemas.block import BlockGroup
from pydantic import BaseModel


class Raw(BaseModel):
    videos: List[dict]


class MeasureTargets(BaseModel):
    type: str
    timestamp: datetime


class Testruns(BaseModel):
    id: str
    is_active: bool
    raw: Raw
    analysis: dict
    measure_targets: Optional[List[MeasureTargets]]
    last_updated_timestamp: Optional[datetime]


class ImportScenario(BaseModel):
    id: str
    updated_at: Optional[datetime]
    is_active: bool
    name: str
    tags: Optional[List[str]] = []
    block_group: Optional[List[BlockGroup]] = []
    testruns: List[Testruns]
