import base64
from typing import List, Tuple

import cv2
import numpy as np


def decode_image_from_base64(base64_str: str) -> np.ndarray:
    decoded = base64.b64decode(base64_str)
    np_array = np.frombuffer(decoded, np.uint8)
    np_image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    return np_image


def split_image_with_row_col(image: np.ndarray, row_num: int, col_num: int) -> np.ndarray:
    height, width = image.shape[:2]
    crop_width, crop_height = width // col_num, height // row_num
    sub_image_matrix = []

    for ys in range(0, height, crop_height):
        ye = min(ys + crop_height, height)  # 끝 부분 이미지는 잘리는 단점이 있음
        sub_image_matrix.append([])

        for xs in range(0, width, crop_width):
            xe = min(xs + crop_width, width)
            sub_image_matrix[-1].append(image[ys:ye, xs:xe])

    return np.array(sub_image_matrix, dtype=np.uint8)


def split_image_with_shape(image: np.ndarray, patch_shape: Tuple) -> Tuple[np.ndarray, List]:
    height, width = image.shape[:2]
    crop_height, crop_width = patch_shape[:2]
    sub_image_matrix = []
    regions = []

    for ys in range(0, height, crop_height):
        ye = ys + crop_height
        if ye > height:  # if overflowed, pull ys
            ys = height - crop_height
            ye = height
        sub_image_matrix.append([])
        regions.append([])

        for xs in range(0, width, crop_width):
            xe = xs + crop_width
            if xe > width:  # if overflowed, pull xs
                xs = width - crop_width
                xe = width
            sub_image_matrix[-1].append(image[ys:ye, xs:xe])
            regions[-1].append((ys, ye, xs, xe))  # y1, y2, x1, x2

    splitted_array = np.array(sub_image_matrix, dtype=np.uint8)
    return splitted_array, regions


def draw_region_to_image(image: np.ndarray, regions: List) -> np.ndarray:
    """_summary_
    Args:
        image (np.ndarray): image to draw
        regions (List): region (y1, y2, x1, x2)
    Returns:
        np.ndarray: image to draw
    """
    image = image.copy()
    for y1, y2, x1, x2 in regions:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3, cv2.LINE_AA)
    return image
