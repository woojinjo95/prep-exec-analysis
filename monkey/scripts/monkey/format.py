import numpy as np
from typing import Tuple
from dataclasses import dataclass, field


@dataclass
class NodeInfo:
    image: field(default_factory=lambda: np.array([]), repr=False)
    cursor: Tuple[int, int, int, int] = (0, 0, 0, 0)  # x,y,w,h
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


@dataclass
class Cursor:
    x: int
    y: int
    w: int
    h: int
