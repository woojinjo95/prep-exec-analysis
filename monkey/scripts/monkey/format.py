import numpy as np
from typing import Tuple
from dataclasses import dataclass, field


class FrameInfo:
    def __init__(self, image: np.ndarray, cursor: Tuple[int, int, int, int]):
        self.image = image
        self.cursor = cursor  # x,y,w,h


@dataclass
class NodeInfo:
    image: field(default_factory=np.ndarray, repr=False)
    cursor: Tuple[int, int, int, int]
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

