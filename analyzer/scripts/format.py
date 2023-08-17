from datetime import datetime
from dataclasses import dataclass


@dataclass
class VideoData:
    video_path: str
    stat_path: str


@dataclass
class ReportData:
    scenario_id: str
    timestamp: datetime


@dataclass
class ColorReferenceReport(ReportData):
    color_reference: float
