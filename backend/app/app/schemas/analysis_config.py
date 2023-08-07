from typing import List, Optional

from app.schemas.enum import (AnalysisTypeEnum, ChannelChangeTimeTargetEnum,
                              LogLevelFinderTargetEnum,
                              ResumeMeasurementRecognizingKeyEventEnum)
from pydantic import BaseModel


class CommonConfig(BaseModel):
    save_video: bool
    before_occurrence: int
    after_occurrence: int


class Roi(BaseModel):
    x: int
    y: int
    w: int
    h: int


class Frame(BaseModel):
    image_path: str
    roi: Roi


class Freeze(CommonConfig):
    analysis_type: AnalysisTypeEnum = AnalysisTypeEnum.freeze
    duration: int


class Macroblock(CommonConfig):
    analysis_type: AnalysisTypeEnum = AnalysisTypeEnum.macroblock


class Loudness(BaseModel):
    analysis_type: AnalysisTypeEnum = AnalysisTypeEnum.loudness


class Resume(CommonConfig):
    analysis_type: AnalysisTypeEnum = AnalysisTypeEnum.resume
    recognizing_key_event: ResumeMeasurementRecognizingKeyEventEnum
    frame: Frame


class Boot(CommonConfig):
    analysis_type: AnalysisTypeEnum = AnalysisTypeEnum.boot
    frame: Frame


class ChannelChangeTime(CommonConfig):
    analysis_type: AnalysisTypeEnum = AnalysisTypeEnum.channel_change_time
    targets: List[ChannelChangeTimeTargetEnum]


class LogLevelFinder(BaseModel):
    analysis_type: AnalysisTypeEnum = AnalysisTypeEnum.log_level_finder
    targets: List[LogLevelFinderTargetEnum]


class LogPatternMatching(BaseModel):
    analysis_type: AnalysisTypeEnum = AnalysisTypeEnum.log_pattern_matching


class AnalysisConfig(BaseModel):
    freeze: Optional[Freeze]
    macroblock: Optional[Macroblock]
    loudness: Optional[Loudness]
    resume: Optional[Resume]
    boot: Optional[Boot]
    channel_change_time: Optional[ChannelChangeTime]
    log_level_finder: Optional[LogLevelFinder]
    log_pattern_matching: Optional[LogPatternMatching]


class AnalysisConfigBase(BaseModel):
    items: AnalysisConfig
