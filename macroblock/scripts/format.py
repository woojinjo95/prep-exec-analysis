from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class ImageSplitResult:
    patches: List[np.ndarray]
    regions: Tuple[int, int, int, int]
    row_num: int
    col_num: int
