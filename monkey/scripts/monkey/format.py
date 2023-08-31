import numpy as np
from typing import Tuple


class FrameInfo:
    def __init__(self, image: np.ndarray, cursor: Tuple[int, int, int, int]):
        self.image = image
        self.cursor = cursor
    