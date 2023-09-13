from dataclasses import dataclass


@dataclass
class SectionData:
    start_time: float
    end_time: float
    analysis_type: str
    section_id: int
    image_path: str
    smart_sense_times: int
