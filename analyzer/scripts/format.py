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


@dataclass
class ReportData:
    scenario_id: str
    testrun_id: str
    timestamp: datetime


@dataclass
class ColorReferenceReport(ReportData):
    color_reference: float


@dataclass
class FreezeReport(ReportData):
    freeze_type: str


@dataclass
class InputData:
    video_path: str
    timestamps: List[float]
