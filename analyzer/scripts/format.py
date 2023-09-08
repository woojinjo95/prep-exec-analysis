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


@dataclass
class ChannelZappingEventData:
    event_time: float
    key: str = ''
    src: str = ''
    dst: str = ''
    channel_name: str = ''


@dataclass
class ChannelZappingResult:
    status: str
    total: int = 0
    a: int = 0
    b: int = 0
    c: int = 0



class ReportName(Enum):
    COLOR_REFERENCE = 'color_reference'
    FREEZE = 'freeze'
    WARM_BOOT = 'warm_boot'
    COLD_BOOT = 'cold_boot'
    LOG_PATTERN = 'log_pattern'
    CHANNEL_ZAPPING = 'channel_change_time'


class CollectionName(Enum):
    COLOR_REFERENCE = 'an_color_reference'
    FREEZE = 'an_freeze'
    WARM_BOOT = 'an_warm_boot'
    COLD_BOOT = 'an_cold_boot'
    LOG_PATTERN = 'an_log_pattern'
    CHANNEL_ZAPPING = 'an_channel_change_time'

    
# command for subscriber
class Command(Enum):
    COLOR_REFERENCE = 'color_reference'
    FREEZE = 'freeze'
    RESUME = 'resume'
    BOOT = 'boot'
    LOG_PATTERN_MATCHING = 'log_pattern_matching'
    CHANNEL_ZAPPING = 'channel_change_time'

