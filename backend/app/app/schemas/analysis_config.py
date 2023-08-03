from typing import List, Optional

from app.schemas.enum import (ChannelChangeTimeTargetEnum,
                              LogLevelFinderTargetEnum,
                              ResumeMeasurementRecognizingKeyEventEnum)
from pydantic import BaseModel


class CommonConfig(BaseModel):
    save_video: bool
    before_occurrence: int
    after_occurrence: int


class Roi(BaseModel):
    # id: Optional[str]
    x: int
    y: int
    w: int
    h: int


class Frame(BaseModel):
    # id: Optional[str]
    image_path: str
    rois: List[Roi]


class Freeze(CommonConfig):
    duration: int


class Macroblock(CommonConfig):
    pass


class Resume(CommonConfig):
    recognizing_key_event: ResumeMeasurementRecognizingKeyEventEnum
    frames: List[Frame]


class Boot(CommonConfig):
    frames: List[Frame]


class ChannelChangeTime(CommonConfig):
    targets: List[ChannelChangeTimeTargetEnum]


class LogLevelFinder(BaseModel):
    targets: List[LogLevelFinderTargetEnum]


class AnalysisConfig(BaseModel):
    freeze: Optional[Freeze]
    macroblock: Optional[Macroblock]
    resume: Optional[Resume]
    boot: Optional[Boot]
    channel_change_time: Optional[ChannelChangeTime]
    log_level_finder: Optional[LogLevelFinder]


class AnalysisConfigBase(BaseModel):
    items: AnalysisConfig
