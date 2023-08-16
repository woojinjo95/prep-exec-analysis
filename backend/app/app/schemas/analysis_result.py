from typing import List

from pydantic import BaseModel


class LogLevelFinderBase(BaseModel):
    timestamp: str
    log_level: str


class LogLevelFinder(BaseModel):
    items: List[LogLevelFinderBase]


class CpuAndMemoryBase(BaseModel):
    timestamp: str
    cpu_usage: float
    memory_usage: float


class CpuAndMemory(BaseModel):
    items: List[CpuAndMemoryBase]


class ColorReferenceBase(BaseModel):
    pass


class ColorReference(BaseModel):
    items: List[ColorReferenceBase]


class EventLogBase(BaseModel):
    pass


class EventLog(BaseModel):
    items: List[EventLogBase]


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