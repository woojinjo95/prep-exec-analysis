from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class SectionData:
    start_time: datetime = None
    end_time: datetime = None
    analysis_type: str = ''
    section_id: int = 0
    image_path: str = ''
    smart_sense_times: int = 0
    user_config: Dict = {}

