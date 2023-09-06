import numpy as np
from typing import Tuple
from dataclasses import dataclass


class FrameInfo:
    def __init__(self, image: np.ndarray, cursor: Tuple[int, int, int, int]):
        self.image = image
        self.cursor = cursor  # x,y,w,h


class NodeInfo:
    def __init__(self, image: np.ndarray, cursor: Tuple[int, int, int, int], 
                 name: str='', cursor_image: np.ndarray=None):
        self.name = name
        self.image = image
        self.cursor = cursor  # x,y,w,h
        self.cursor_image = cursor_image
        self.is_breadth_end = False
        self.is_leaf = False


@dataclass
class MonkeyArgs:
    duration: float
    enable_smart_sense: bool
    waiting_time: float


@dataclass
class RemoconInfo:
    remocon_name: str
    remote_control_type: str

