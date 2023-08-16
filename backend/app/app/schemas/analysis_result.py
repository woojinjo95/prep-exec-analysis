from typing import List
from datetime import datetime

from pydantic import BaseModel


class LogLevelFinderBase(BaseModel):
    timestamp: datetime
    log_level: str


class LogLevelFinder(BaseModel):
    items: List[LogLevelFinderBase]


class CpuAndMemoryBase(BaseModel):
    timestamp: datetime
    cpu_usage: float
    memory_usage: float


class CpuAndMemory(BaseModel):
    items: List[CpuAndMemoryBase]


class EventLogBase(BaseModel):
    timestamp: datetime
    service: str
    msg: str
    data: dict


class EventLog(BaseModel):
    items: List[EventLogBase]


class ColorReferenceBase(BaseModel):
    pass


class ColorReference(BaseModel):
    items: List[ColorReferenceBase]


class VideoAnalysisResultBase(BaseModel):
    pass


class VideoAnalysisResult(BaseModel):
    items: List[VideoAnalysisResultBase]


class LogPatternMatchingBase(BaseModel):
    pass


class LogPatternMatching(BaseModel):
    items: List[LogPatternMatchingBase]


class MeasurementBase(BaseModel):
    pass


class Measurement(BaseModel):
    items: List[MeasurementBase]


class ProcessLifecycleBase(BaseModel):
    pass


class ProcessLifecycle(BaseModel):
    items: List[ProcessLifecycleBase]


class NetworkFilterBase(BaseModel):
    pass


class NetworkFilter(BaseModel):
    items: List[NetworkFilterBase]