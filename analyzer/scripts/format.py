from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class VideoData:
    video_path: str
    stat_path: str


class CollectionName(Enum):
    COLOR_REFERENCE = 'an_color_reference'
    FREEZE = 'an_freeze'
    WARM_BOOT = 'an_warm_boot'
    COLD_BOOT = 'an_cold_boot'
    LOG_PATTERN = 'an_log_pattern'


@dataclass
class InputData:
    video_path: str
    timestamps: List[float]


@dataclass
class CroppedInfo:
    video_path: str
    timestamps: List[float]


class LogName(Enum):
    COLOR_REFERENCE = 'color_reference'
    FREEZE_DETECT = 'freeze_detect'
    BOOT_TEST = 'boot_test'
    LOG_PATTERN = 'log_pattern'
    