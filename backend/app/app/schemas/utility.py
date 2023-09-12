from typing import List, Optional

from app.schemas.enum import ExportItemEnum
from pydantic import BaseModel, root_validator
from pydantic.datetime_parse import parse_datetime


class ServiceStateBase(BaseModel):
    state: Optional[str]


class ServiceState(BaseModel):
    items: ServiceStateBase


class LogConnectionStatusBase(BaseModel):
    status: Optional[str]


class LogConnectionStatus(BaseModel):
    items: LogConnectionStatusBase


class VideoTimestampBase(BaseModel):
    path: str
    start_time: str
    end_time: str


class VideoTimestamp(BaseModel):
    items: VideoTimestampBase


class VideoSnapshotBase(BaseModel):
    path: str
    timestamp: str


class VideoSnapshot(BaseModel):
    items: List[VideoSnapshotBase]


class ExportResult(BaseModel):
    scenario_id: Optional[str]
    testrun_id: Optional[str]
    items: List[ExportItemEnum]


class Regex(BaseModel):
    regex: str


class RegexResult(BaseModel):
    is_valid: bool
    msg: str
    detail: Optional[str]
    keys: Optional[list]
