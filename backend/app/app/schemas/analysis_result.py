from typing import List

from app.schemas.enum import LogLevelEnum, FreezeTypeEnum, ResumeTypeEnum
from pydantic import BaseModel, root_validator
from pydantic.datetime_parse import parse_datetime
from typing import Optional


class TimestampBaseModel(BaseModel):
    timestamp: str

    @root_validator(pre=True)
    def convert_timestamp_with_timezone(cls, values):
        if "timestamp" in values:
            values["timestamp"] = parse_datetime(values["timestamp"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return values
    

class PaginationBaseModel(BaseModel):
    total: int = 0
    pages: int = None
    prev: int = None
    next: int = None


class LogLevelFinderBase(TimestampBaseModel):
    log_level: LogLevelEnum


class LogLevelFinder(PaginationBaseModel):
    items: List[LogLevelFinderBase]


class CpuBase(TimestampBaseModel):
    cpu_usage: str
    total: str
    user: str
    kernel: str
    iowait: str
    irq: str
    softirq: str


class Cpu(PaginationBaseModel):
    items: List[CpuBase]


class MemoryBase(TimestampBaseModel):
    memory_usage: str
    total_ram: str
    free_ram: str
    used_ram: str
    lost_ram: str


class Memory(PaginationBaseModel):
    items: List[MemoryBase]


class EventLogBase(TimestampBaseModel):
    service: str
    msg: str
    data: dict


class EventLog(PaginationBaseModel):
    items: List[EventLogBase]


class ColorReferenceBase(TimestampBaseModel):
    color_reference: float


class ColorReference(PaginationBaseModel):
    items: List[ColorReferenceBase]


class FreezeBase(TimestampBaseModel):
    freeze_type: FreezeTypeEnum
    duration: float


class Freeze(PaginationBaseModel):
    items: List[FreezeBase]


class LoudnessBase(TimestampBaseModel):
    m: float  # Momentary LKFS
    # i: float # Integrated LKFS


class Loudness(PaginationBaseModel):
    items: List[LoudnessBase]


class MeasurementBootBase(TimestampBaseModel):
    target: ResumeTypeEnum
    measure_time: int


class MeasurementBoot(PaginationBaseModel):
    items: List[MeasurementBootBase]


class LogPatternMatchingBase(TimestampBaseModel):
    log_pattern_name: str
    log_level: str
    color: str
    regex: str
    message: str


class LogPatternMatching(PaginationBaseModel):
    items: List[LogPatternMatchingBase]


class ProcessLifecycleBase(BaseModel):
    pass


class ProcessLifecycle(BaseModel):
    items: List[ProcessLifecycleBase]


class NetworkFilterBase(BaseModel):
    pass


class NetworkFilter(BaseModel):
    items: List[NetworkFilterBase]


# ----- Summary Schemas -----
class SummaryBase(BaseModel):
    total: int


class FreezeSummary(SummaryBase):
    target: FreezeTypeEnum


class ResumeSummary(SummaryBase):
    target: ResumeTypeEnum
    avg_time: float


class BootSummary(SummaryBase):
    target: ResumeTypeEnum
    avg_time: float


class ChannelChangeTimeSummary(SummaryBase):
    target: str # Enum type TBD
    avg_time: int


class LogLevelFinderSummary(SummaryBase):
    target: LogLevelEnum


class LogPatternMatchingSummary(SummaryBase):
    log_pattern_name: str
    color: str


class LoudnessSummary(BaseModel):
    lkfs: int


class MonkeyTestSummary(BaseModel):
    duration_time: int # TBD
    smart_sense: int


class IntelligentMonkeyTestSummary(BaseModel):
    smart_sense: int # TBD


class MacroblockSummary(BaseModel):
    pass # TBD


class DataSummaryBase(BaseModel):
    boot: Optional[List[BootSummary]] = None
    # channel_change_time: Optional[List[ChannelChangeTimeSummary]] = None
    freeze: Optional[List[FreezeSummary]] = None
    intelligent_monkey_test: Optional[List[IntelligentMonkeyTestSummary]] = None
    log_level_finder: Optional[List[LogLevelFinderSummary]] = None
    log_pattern_matching: Optional[List[LogPatternMatchingSummary]] = None
    loudness: Optional[List[LoudnessSummary]] = None
    resume: Optional[List[ResumeSummary]] = None
    # macro_block: Optional[List[MacroblockSummary]] = None
    monkey_test: Optional[List[MonkeyTestSummary]] = None


class DataSummary(BaseModel):
    items: DataSummaryBase
