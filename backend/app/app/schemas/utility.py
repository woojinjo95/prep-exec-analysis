from typing import List, Optional

from app.schemas.enum import ExportItemEnum
from pydantic import BaseModel


class ServiceStateBase(BaseModel):
    state: Optional[str]


class ServiceState(BaseModel):
    items: ServiceStateBase


class LogConnectionStatusBase(BaseModel):
    status: Optional[str]


class LogConnectionStatus(BaseModel):
    items: LogConnectionStatusBase


class VideoTimestampBase(BaseModel):
    start_time: str
    end_time: str


class VideoTimestamp(BaseModel):
    items: VideoTimestampBase


class ExportResult(BaseModel):
    scenario_id: Optional[str]
    testrun_id: Optional[str]
    items: List[ExportItemEnum]
