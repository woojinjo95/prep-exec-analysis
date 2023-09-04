from typing import List, Optional

from app.schemas.enum import (BootTypeEnum, ChannelChangeTimeTargetEnum,
                              LogLevelEnum, ResumeTypeEnum)
from pydantic import BaseModel


class CommonBaseModel(BaseModel):
    color: str


class Roi(BaseModel):
    x: int
    y: int
    w: int
    h: int


class Frame(BaseModel):
    id: str
    path: str
    roi: Roi


class Freeze(CommonBaseModel):
    duration: int


class Macroblock(CommonBaseModel):
    frame_sampling_interval: int
    threshold_score: float


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


class ProcessLifecycleAnalysis(CommonBaseModel):
    pass


class NetworkFilter(CommonBaseModel):
    pass


class MonkeyTest(CommonBaseModel):
    pass


class IntelligentMonkeyTest(CommonBaseModel):
    pass


class AnalysisConfig(BaseModel):
    freeze: Optional[Freeze]
    # macroblock: Optional[Macroblock]
    loudness: Optional[Loudness]
    resume: Optional[Resume]
    boot: Optional[Boot]
    channel_change_time: Optional[ChannelChangeTime]
    log_level_finder: Optional[LogLevelFinder]
    log_pattern_matching: Optional[LogPatternMatching]
    # process_lifecycle_analysis: Optional[ProcessLifecycleAnalysis]
    # network_filter: Optional[NetworkFilter]
    monkey_test: Optional[MonkeyTest]
    intelligent_monkey_test: Optional[IntelligentMonkeyTest]


class AnalysisConfigBase(BaseModel):
    items: AnalysisConfig


class FrameImage(BaseModel):
    id: str
    path: str
