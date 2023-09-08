from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class ImageSplitResult:
    patches: List[np.ndarray]
    regions: Tuple[int, int, int, int]
    row_num: int
    col_num: int


@dataclass
class ClassificationResult:
    scores: List[float]  # [0.99, 0.08, ...]
    model_input_shape: Tuple[int, int, int]  # (224, 224, 3)
    total_delay: float
    pred_delay: float
