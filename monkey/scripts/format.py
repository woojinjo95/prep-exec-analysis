from typing import List
from dataclasses import dataclass


@dataclass
class SmartSenseData:
    analysis_type: str
    section_id: int
    smart_sense_key: List[str]
    