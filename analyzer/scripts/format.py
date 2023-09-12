from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

import numpy as np


@dataclass
class VideoInfo:
    video_path: str
    timestamps: List[float]
    frame_count: int = 0
    fps: float = 0.0


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


@dataclass
class ImageSplitResult:
    patches: List[np.ndarray]
    regions: Tuple[int, int, int, int]
    row_num: int
    col_num: int


@dataclass
class ClassificationResult:
    scores: List[float]  # [0.99, 0.08, ...]
    model_input_shape: Tuple[int, int, int]  # (224, 224, 3)
    total_delay: float
    pred_delay: float


@dataclass
class MacroblockResult:
    status: str  # success | error
    detect: bool = False  # 검출 조건(연속성 등)까지 고려한 검출 여부
    occurred: bool = False  # 현재 프레임에 대한 검출 여부
    start_time: float = 0.0
    end_time: float = 0.0
    duration: float = 0.0
    split_result: ImageSplitResult = None
    cls_result: ClassificationResult = None




class ReportName(Enum):
    COLOR_REFERENCE = 'color_reference'
    FREEZE = 'freeze'
    WARM_BOOT = 'warm_boot'
    COLD_BOOT = 'cold_boot'
    LOG_PATTERN = 'log_pattern'
    CHANNEL_ZAPPING = 'channel_change_time'
    MACROBLOCK = 'macroblock'


class CollectionName(Enum):
    COLOR_REFERENCE = 'an_color_reference'
    FREEZE = 'an_freeze'
    WARM_BOOT = 'an_warm_boot'
    COLD_BOOT = 'an_cold_boot'
    LOG_PATTERN = 'an_log_pattern'
    CHANNEL_ZAPPING = 'an_channel_change_time'
    MACROBLOCK = 'an_macroblock'

    
# command for subscriber
class Command(Enum):
    COLOR_REFERENCE = 'color_reference'
    FREEZE = 'freeze'
    RESUME = 'resume'
    BOOT = 'boot'
    LOG_PATTERN_MATCHING = 'log_pattern_matching'
    CHANNEL_ZAPPING = 'channel_change_time'
    MACROBLOCK = 'macroblock'
    

