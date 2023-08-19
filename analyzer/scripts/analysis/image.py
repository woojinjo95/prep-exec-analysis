import numpy as np
import cv2


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
