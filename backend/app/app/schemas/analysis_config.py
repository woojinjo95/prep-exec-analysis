from typing import List, Optional

from app.schemas.enum import ResumeMeasurementRecognizingKeyEvent
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
    rois: List[Roi]


class Freeze(CommonConfig):
    duration: int = 0


class Macroblock(CommonConfig):
    pass


class Resume(CommonConfig):
    recognizing_key_event: ResumeMeasurementRecognizingKeyEvent
    frames: List[Frame]


class Boot(CommonConfig):
    frames: List[Frame]


class ChannelChangeTime(CommonConfig):
    targets: List[str]


class LogLevelFinder(BaseModel):
    targets: List[str]


class AnalysisConfig(BaseModel):
    freeze: Freeze
    macroblock: Macroblock
    resume: Resume
    boot: Boot
    channel_change_time: ChannelChangeTime
    log_level_finder: LogLevelFinder


class AnalysisConfigBase(BaseModel):
    items: AnalysisConfig


class AnalysisConfigUpdate(BaseModel):
    pass
