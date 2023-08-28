from typing import List

from app.schemas.enum import LogLevelEnum
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
    log_level: LogLevelEnum


class LogLevelFinder(BaseModel):
    items: List[LogLevelFinderBase]


class CpuBase(TimestampBaseModel):
    cpu_usage: str
    total: str
    user: str
    kernel: str
    iowait: str
    irq: str
    softirq: str


class Cpu(BaseModel):
    items: List[CpuBase]


class MemoryBase(TimestampBaseModel):
    memory_usage: str
    total_ram: str
    free_ram: str
    used_ram: str
    lost_ram: str


class Memory(BaseModel):
    items: List[MemoryBase]


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
    duration: float


class Freeze(BaseModel):
    items: List[FreezeBase]


class LoudnessBase(TimestampBaseModel):
    m: float  # Momentary LKFS
    # i: float # Integrated LKFS


class Loudness(BaseModel):
    items: List[LoudnessBase]


class MeasurementBootBase(TimestampBaseModel):
    measure_time: int


class MeasurementBoot(BaseModel):
    items: List[MeasurementBootBase]


class LogPatternMatchingBase(TimestampBaseModel):
    log_pattern_name: str
    log_level: str
    message: str


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
