from typing import List, Tuple

import numpy as np
import cv2

from scripts.format import ImageSplitResult


def calc_image_value_rate(image: np.ndarray) -> float:
    image_value_sum = np.sum(image)
    pixels_num = int(np.prod(image.shape))
    value_rate = (image_value_sum / pixels_num) / 255
    return value_rate


def calc_image_whole_stdev(image: np.ndarray) -> float:
    mult = 2 / 255  # normalize stdev 0 ~ 127.5 to 0 ~ 1
    return np.std(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)) * mult


def calc_diff_rate(image1: np.ndarray, image2: np.ndarray, min_color_depth_diff: int = 0) -> float:
    diff_image = cv2.absdiff(image1, image2)
    diff_num = np.count_nonzero(diff_image > min_color_depth_diff)
    pixels_num = np.prod(diff_image.shape)
    diff_rate = diff_num / pixels_num
    return diff_rate


def is_similar_by_match_template(image: np.ndarray, template: np.ndarray, match_thres: float = 0.8) -> bool:
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, max_value, _, _ = cv2.minMaxLoc(result)

    return max_value > match_thres


def get_cropped_image(image: np.ndarray, roi: List[int]) -> np.ndarray:
    x, y, w, h = roi
    y_min = y
    y_max = y + h
    x_min = x
    x_max = x + w

    height, width = image.shape[:2]

    if height == 0 or width == 0:
        raise Exception(f'Invald_image: {image.shape[2:]}')
    elif y_max - y_min < 0 or x_max - x_min < 0:
        raise Exception(f'ROI is not enclosed: y_min, y_max, x_min, x_max: {y_min}, {y_max}, {x_min}, {x_max}')
    elif w * h > width * height or y_min < 0 or x_min < 0:
        raise Exception(f'ROI is exceed image size, w:{width}, h:{height}, roi: {roi}')

    return image[y_min:y_max, x_min:x_max]


def calc_color_entropy(image: np.ndarray) -> float:
    """_summary_
    Calculate image color entropy
    entropy: the amount of information within pixel value 
    Args:
        image (np.ndarray): image array
    Returns:
        float: entropy value
    """
    _, counts = np.unique(image, return_counts=True)  # unique: occured pixel value(0~255), counts: count of appearance
    pixel_num = np.prod(image.shape)
    probabilities = counts / pixel_num  # array of appearance probability about each pixel value
    entropy = -np.sum(probabilities * np.log2(probabilities))  # Shannon entropy formula (maximum=8)
    return entropy


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
