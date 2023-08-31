from typing import Optional

from pydantic import BaseModel


class Timezone(BaseModel):
    timezone: str


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