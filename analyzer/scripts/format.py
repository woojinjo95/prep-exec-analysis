from datetime import datetime
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


@dataclass
class InputData:
    video_path: str
    timestamps: List[float]


@dataclass
class CroppedInfo:
    video_path: str
    timestamps: List[float]
