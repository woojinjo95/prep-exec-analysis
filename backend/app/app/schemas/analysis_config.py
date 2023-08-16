from typing import List, Optional

from app.schemas.enum import (BootTypeEnum, ChannelChangeTimeTargetEnum,
                              ResumeRecognizingKeyEventEnum, ResumeTypeEnum)
from pydantic import BaseModel


class CommonBaseModel(BaseModel):
    is_active: bool


class Roi(BaseModel):
    x: int
    y: int
    w: int
    h: int


class Frame(BaseModel):
    image_path: str
    roi: Roi


class Freeze(CommonBaseModel):
    duration: int


class Macroblock(CommonBaseModel):
    frame_sampling_interval: int
    threshold_score: float


class Loudness(CommonBaseModel):
    pass


class Resume(CommonBaseModel):
    recognizing_key_event: ResumeRecognizingKeyEventEnum
    type: ResumeTypeEnum
    frame: Optional[Frame]


class Boot(CommonBaseModel):
    type: BootTypeEnum
    frame: Optional[Frame]


class ChannelChangeTime(CommonBaseModel):
    targets: List[ChannelChangeTimeTargetEnum]


class LogLevelFinder(CommonBaseModel):
    pass
    # targets: List[LogLevelFinderTargetEnum]


class LogPatternMatching(CommonBaseModel):
    pass


class ProcessLifecycleAnalysis(CommonBaseModel):
    pass


class NetworkFilter(CommonBaseModel):
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
    process_lifecycle_analysis: Optional[ProcessLifecycleAnalysis]
    network_filter: Optional[NetworkFilter]


class AnalysisConfigBase(BaseModel):
    items: AnalysisConfig
