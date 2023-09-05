from typing import List

from app.schemas.enum import LogLevelEnum, FreezeTypeEnum, ResumeTypeEnum, BootTypeEnum
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


class ResumeBase(TimestampBaseModel):
    target: ResumeTypeEnum
    measure_time: int


class Resume(PaginationBaseModel):
    items: List[ResumeBase]


class BootBase(TimestampBaseModel):
    target: BootTypeEnum
    measure_time: int


class Boot(PaginationBaseModel):
    items: List[BootBase]


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
class SummaryInnerBase(BaseModel):
    total: int


class SummaryBase(BaseModel):
    color: str


class FreezeSummaryBase(SummaryInnerBase):
    error_type: FreezeTypeEnum


class FreezeSummary(SummaryBase):
    results: List[FreezeSummaryBase]


class ResumeSummaryBase(SummaryInnerBase):
    avg_time: float
    target: ResumeTypeEnum


class ResumeSummary(SummaryBase):
    results: List[ResumeSummaryBase]


class BootSummaryBase(SummaryInnerBase):
    avg_time: float
    target: BootTypeEnum


class BootSummary(SummaryBase):
    results: List[BootSummaryBase]


class ChannelChangeTimeSummaryBase(SummaryInnerBase):   # 미적용
    target: str
    avg_time: int


class ChannelChangeTimeSummary(SummaryBase):    # 미적용
    results: List[ChannelChangeTimeSummaryBase]


class LogLevelFinderSummaryBase(SummaryInnerBase):
    target: LogLevelEnum
    total: int


class LogLevelFinderSummary(SummaryBase):
    results: List[LogLevelFinderSummaryBase]


class LogPatternMatchingSummaryBase(SummaryInnerBase):
    color: str
    log_pattern_name: str


class LogPatternMatchingSummary(SummaryBase):
    results: List[LogPatternMatchingSummaryBase]


class LoudnessSummary(SummaryBase):
    lkfs: float


class MonkeyTestSummary(BaseModel): # 미적용
    duration_time: int
    smart_sense: int


class IntelligentMonkeyTestSummary(BaseModel):  # 미적용
    smart_sense: int


class MacroblockSummary(BaseModel): # 미적용
    pass


class DataSummaryBase(BaseModel):
    boot: Optional[BootSummary] = None
    # channel_change_time: Optional[ChannelChangeTimeSummary] = None
    freeze: Optional[FreezeSummary] = None
    intelligent_monkey_test: Optional[IntelligentMonkeyTestSummary] = None
    last_timestamp: Optional[str] = None
    log_level_finder: Optional[LogLevelFinderSummary] = None
    log_pattern_matching: Optional[LogPatternMatchingSummary] = None
    loudness: Optional[LoudnessSummary] = None
    resume: Optional[ResumeSummary] = None
    # macro_block: Optional[MacroblockSummary] = None
    monkey_test: Optional[MonkeyTestSummary] = None


class DataSummary(BaseModel):
    items: DataSummaryBase
