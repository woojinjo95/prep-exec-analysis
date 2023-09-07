from typing import List, Optional

from app.schemas.enum import ExportItemEnum
from pydantic import BaseModel, root_validator
from pydantic.datetime_parse import parse_datetime
from app.schemas.analysis_result import TimestampBaseModel


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

    @root_validator(pre=True)
    def convert_timestamp_with_timezone(cls, values):
        if "start_time" in values:
            values["start_time"] = parse_datetime(values["start_time"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if "end_time" in values:
            values["end_time"] = parse_datetime(values["end_time"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return values


class VideoTimestamp(BaseModel):
    items: VideoTimestampBase


class VideoSnapshotBase(TimestampBaseModel):
    path: str


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
