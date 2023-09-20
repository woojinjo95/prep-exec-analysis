from typing import List, Optional

from app.schemas.enum import (AnalysisTypeEnum, BootTypeEnum,
                              ChannelChangeTimeTargetEnum, LogLevelEnum,
                              ResumeTypeEnum)
from pydantic import BaseModel


class CommonBaseModel(BaseModel):
    color: str


class Roi(BaseModel):
    x: int
    y: int
    w: int
    h: int


class Frame(BaseModel):
    path: str
    relative_time: float
    roi: Roi


class Freeze(CommonBaseModel):
    duration: int = 3


class Macroblock(CommonBaseModel):
    duration: int = 1
    sampling_interval: int = 1
    score_threshold: float = 0.995


class Loudness(CommonBaseModel):
    pass


class Resume(CommonBaseModel):
    type: ResumeTypeEnum
    frame: Optional[Frame]


class Boot(CommonBaseModel):
    type: BootTypeEnum
    frame: Optional[Frame]


class ChannelChangeTime(CommonBaseModel):
    targets: List[ChannelChangeTimeTargetEnum]


class LogLevelFinder(CommonBaseModel):
    targets: List[LogLevelEnum]


class LogPatternMatchingItems(CommonBaseModel):
    name: str
    level: LogLevelEnum
    regular_expression: str
    color: str


class LogPatternMatching(CommonBaseModel):
    items: List[LogPatternMatchingItems]


class ProcessLifecycle(CommonBaseModel):
    pass


class NetworkFilter(CommonBaseModel):
    pass


class MonkeyTest(CommonBaseModel):
    pass


class IntelligentMonkeyTest(CommonBaseModel):
    pass


class AnalysisConfig(BaseModel):
    freeze: Optional[Freeze]
    macroblock: Optional[Macroblock]
    loudness: Optional[Loudness]
    resume: Optional[Resume]
    boot: Optional[Boot]
    channel_change_time: Optional[ChannelChangeTime]
    log_level_finder: Optional[LogLevelFinder]
    log_pattern_matching: Optional[LogPatternMatching]
    process_lifecycle: Optional[ProcessLifecycle]
    network_filter: Optional[NetworkFilter]
    monkey_test: Optional[MonkeyTest]
    intelligent_monkey_test: Optional[IntelligentMonkeyTest]


class AnalysisConfigBase(BaseModel):
    items: AnalysisConfig


class FrameImage(BaseModel):
    id: str
    path: str


class Analysis(BaseModel):
    scenario_id: str
    testrun_id: str
    measurement: List[AnalysisTypeEnum]
