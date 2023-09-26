from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TimestampBaseModel(BaseModel):
    timestamp: datetime


class Raw(BaseModel):
    videos: List[dict]


class Analysis(BaseModel):
    from app.schemas.analysis_config import AnalysisConfig
    config: Optional[AnalysisConfig] = AnalysisConfig


class MeasureTargets(TimestampBaseModel):
    type: str
    progress: Optional[float] = 0
    remaining_time: Optional[float] = 0


class Testruns(BaseModel):
    id: str
    raw: Raw
    analysis: Optional[Analysis]
    measure_targets: Optional[List[MeasureTargets]]
    last_updated_timestamp: Optional[datetime]


class ImportScenario(BaseModel):  # --------- scenario
    from app.schemas.block import BlockGroup
    id: str
    updated_at: Optional[datetime]
    is_active: bool
    name: str
    tags: Optional[List[str]] = []
    block_group: Optional[List[BlockGroup]] = []
    testruns: List[Testruns]


class CommonBaseModel(TimestampBaseModel):
    scenario_id: str
    testrun_id: str


class EventLogLine(TimestampBaseModel):
    service: str
    msg: str
    data: dict


class ImportEventLog(CommonBaseModel):  # --------- event_log
    lines: List[EventLogLine]


class LoudnessLine(TimestampBaseModel):
    M: float
    I: float


class ImportLoudness(CommonBaseModel):  # --------- loudness
    lines: List[LoudnessLine]


class ImportMonkeySection(CommonBaseModel):  # --------- monkey_section
    start_timestamp: datetime
    end_timestamp: datetime
    analysis_type: str
    section_id: int
    image_path: str
    smart_sense_times: int
    user_config: dict


class ImportMonkeySmartSense(CommonBaseModel):  # --------- monkey_smart_sense
    analysis_type: str
    section_id: int
    smart_sense_key: List[str]
    user_config: dict


class NetworkTraceLine(TimestampBaseModel):
    from app.schemas.enum import ProtocolEnum
    src: str
    dst: str
    protocol: ProtocolEnum
    length: int
    info: str


class ImportNetworkTrace(CommonBaseModel):  # --------- network_trace
    lines: List[NetworkTraceLine]


class ShellLogLine(TimestampBaseModel):
    from app.schemas.enum import LogModuleEnum
    module: LogModuleEnum
    message: str


class ImportShellLog(CommonBaseModel):  # --------- shell_log
    mode: str
    lines: List[ShellLogLine]


class ImportStbInfo(CommonBaseModel):  # --------- stb_info
    cpu_usage: str
    total: str
    user: str
    kernel: str
    iowait: str
    irq: str
    softirq: str
    memory_usage: str
    total_ram: str
    free_ram: str
    used_ram: str
    lost_ram: str


class StbLogLine(TimestampBaseModel):
    from app.schemas.enum import LogLevelEnum
    module: str
    log_level: LogLevelEnum
    process_name: str
    pid: str
    tid: str
    message: str


class ImportStbLog(CommonBaseModel):  # --------- stb_log
    lines: List[StbLogLine]


class ImportVideoSnapshot(CommonBaseModel):  # --------- video_snapshot
    video_path: str
    path: str
    extension: str
    names: List[str]


class ImportAnColdBoot(CommonBaseModel):  # --------- an_cold_boot
    from app.schemas.analysis_config import Boot
    measure_time: int
    user_config: Boot


class ImportAnColorReference(CommonBaseModel):  # --------- an_color_reference
    color_reference: float
    user_config: Optional[dict] = {}


class ImportAnFreeze(CommonBaseModel):  # --------- an_freeze
    from app.schemas.analysis_config import Freeze
    freeze_type: str
    duration: float
    user_config: Freeze


class ImportAnLogPattern(CommonBaseModel):  # --------- an_log_pattern
    from app.schemas.analysis_config import LogPatternMatchingItems, LogPatternMatching
    module: str
    log_level: str
    process_name: str
    pid: str
    tid: str
    message: str
    matched_target: LogPatternMatchingItems
    user_config: LogPatternMatching


class ImportAnWarmBoot(CommonBaseModel):  # --------- an_warm_boot
    from app.schemas.analysis_config import Resume
    measure_time: int
    user_config: Resume
