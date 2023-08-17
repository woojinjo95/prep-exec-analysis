from datetime import datetime
from dataclasses import dataclass
from enum import Enum


@dataclass
class VideoData:
    video_path: str
    stat_path: str


class CollecionName(Enum):
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
