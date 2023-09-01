import numpy as np
from typing import Tuple
from dataclasses import dataclass


class FrameInfo:
    def __init__(self, image: np.ndarray, cursor: Tuple[int, int, int, int]):
        self.image = image
        self.cursor = cursor


@dataclass
class MonkeyArgs:
    duration_per_menu: float
    enable_smart_sense: bool
    waiting_time: float