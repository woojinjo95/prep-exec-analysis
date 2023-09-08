import base64
from typing import List, Tuple

import cv2
import numpy as np

from scripts.format import ImageSplitResult


def decode_image_from_base64(base64_str: str) -> np.ndarray:
    decoded = base64.b64decode(base64_str)
    np_array = np.frombuffer(decoded, np.uint8)
    np_image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    return np_image


def split_image_with_shape(image: np.ndarray, patch_shape: Tuple) -> ImageSplitResult:
    height, width = image.shape[:2]
    crop_height, crop_width = patch_shape[:2]
    patches = []
    regions = []
    row_num = 0

    for ys in range(0, height, crop_height):
        ye = ys + crop_height
        if ye > height:  # if overflowed, pull ys
            ys = height - crop_height
            ye = height
        row_num += 1

        col_num = 0
        for xs in range(0, width, crop_width):
            xe = xs + crop_width
            if xe > width:  # if overflowed, pull xs
                xs = width - crop_width
                xe = width
            col_num += 1
            patches.append(image[ys:ye, xs:xe])
            regions.append((ys, ye, xs, xe))  # y1, y2, x1, x2

    return ImageSplitResult(
        patches=patches,
        regions=regions,
        row_num=row_num,
        col_num=col_num
    )
