from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class SectionData:
    start_timestamp: datetime = None
    end_timestamp: datetime = None
    analysis_type: str = None
    section_id: int = None
    image_path: str = None
    smart_sense_times: int = None
    user_config: Dict = None
