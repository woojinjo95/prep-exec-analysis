from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class VideoData:
    video_path: str
    stat_path: str


@dataclass
class InputData:
    video_path: str
    timestamps: List[float]


@dataclass
class CroppedInfo:
    video_path: str
    timestamps: List[float]


@dataclass
class IgmpJoinData:
    timestamp: float
    src: str = ''
    dst: str = ''
    channel_info: str = ''


@dataclass
class RemoconKeyData:
    timestamp: float
    key: str = ''


class ReportName(Enum):
    COLOR_REFERENCE = 'color_reference'
    FREEZE = 'freeze'
    WARM_BOOT = 'warm_boot'
    COLD_BOOT = 'cold_boot'
    LOG_PATTERN = 'log_pattern'


class CollectionName(Enum):
    COLOR_REFERENCE = 'an_color_reference'
    FREEZE = 'an_freeze'
    WARM_BOOT = 'an_warm_boot'
    COLD_BOOT = 'an_cold_boot'
    LOG_PATTERN = 'an_log_pattern'

    
# command for subscriber
class Command(Enum):
    COLOR_REFERENCE = 'color_reference'
    FREEZE = 'freeze'
    RESUME = 'resume'
    BOOT = 'boot'
    LOG_PATTERN_MATCHING = 'log_pattern_matching'

