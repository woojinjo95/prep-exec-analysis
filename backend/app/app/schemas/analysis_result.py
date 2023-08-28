from typing import List

from pydantic import BaseModel, root_validator
from pydantic.datetime_parse import parse_datetime


class TimestampBaseModel(BaseModel):
    timestamp: str

    @root_validator(pre=True)
    def convert_timestamp_with_timezone(cls, values):
        if "timestamp" in values:
            values["timestamp"] = parse_datetime(values["timestamp"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return values


class LogLevelFinderBase(TimestampBaseModel):
    log_level: str


class LogLevelFinder(BaseModel):
    items: List[LogLevelFinderBase]


class CpuAndMemoryBase(TimestampBaseModel):
    cpu_usage: str
    memory_usage: str


class CpuAndMemory(BaseModel):
    items: List[CpuAndMemoryBase]


class EventLogBase(TimestampBaseModel):
    service: str
    msg: str
    data: dict


class EventLog(BaseModel):
    items: List[EventLogBase]


class ColorReferenceBase(TimestampBaseModel):
    color_reference: float


class ColorReference(BaseModel):
    items: List[ColorReferenceBase]


class FreezeBase(TimestampBaseModel):
    freeze_type: str


class Freeze(BaseModel):
    items: List[FreezeBase]


class LoudnessBase(TimestampBaseModel):
    m: float # Momentary LKFS
    i: float # Integrated LKFS


class Loudness(BaseModel):
    items: List[LoudnessBase]


class MeasurementBootBase(TimestampBaseModel):
    measure_time: int


class MeasurementBoot(BaseModel):
    items: List[MeasurementBootBase]


class VideoAnalysisResultBase(BaseModel):
    pass


class VideoAnalysisResult(BaseModel):
    items: List[VideoAnalysisResultBase]


class LogPatternMatchingBase(BaseModel):
    pass


class LogPatternMatching(BaseModel):
    items: List[LogPatternMatchingBase]


class ProcessLifecycleBase(BaseModel):
    pass


class ProcessLifecycle(BaseModel):
    items: List[ProcessLifecycleBase]


class NetworkFilterBase(BaseModel):
    pass


class NetworkFilter(BaseModel):
    items: List[NetworkFilterBase]
