import numpy as np
from dataclasses import dataclass, field


@dataclass
class Cursor:
    x: int
    y: int
    w: int
    h: int


@dataclass
class NodeInfo:
    image: field(default_factory=lambda: np.array([]), repr=False)
    cursor: field(default_factory=lambda: Cursor(0, 0, 0, 0))
    is_leaf: bool = False


@dataclass
class MonkeyArgs:
    duration: float
    enable_smart_sense: bool
    waiting_time: float


@dataclass
class RemoconInfo:
    remocon_name: str
    remote_control_type: str


# 외부에서 주입받아야 하는 정보
@dataclass
class MonkeyExternalInfo:
    analysis_type: str = ''  # 분석 종류
    section_id: int = 0  # 현재 섹션 번호
    image_path: str = ''  # 현재 섹션 대표 이미지 경로

