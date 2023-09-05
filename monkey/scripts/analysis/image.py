# 이미지 처리와 관련된 일반 함수 (응용 함수를 여기서 정의하지 말 것.)

import logging
from typing import List, Tuple

import cv2
import numpy as np
from algorithm.ui_reaction.cursor.detector import CursorDetector
from skimage.metrics import structural_similarity as compare_ssim

logger = logging.getLogger('analysis')


def get_cropped_image(image: np.ndarray, roi: List[int]) -> np.ndarray:
    """_summary_
    Crop image by roi

    Args:
        image (np.ndarray): target image
        roi (List[int]): region of interest, [x, y, w, h]

    Returns:
        np.ndarray: cropped image
    """
    x, y, w, h = roi
    y_min = y
    y_max = y + h
    x_min = x
    x_max = x + w

    height, width = image.shape[:2]

    if height == 0 or width == 0:
        logger.error(f'Invald_image: {image.shape[2:]}')
    elif y_max - y_min < 0 or x_max - x_min < 0:
        logger.warn(f'ROI is not enclosed: y_min, y_max, x_min, x_max: {y_min}, {y_max}, {x_min}, {x_max}')
    elif w * h > width * height or y_min < 0 or x_min < 0:
        logger.warn(f'ROI is exceed image size, w:{width}, h:{height}, roi: {roi}')

    return image[y_min:y_max, x_min:x_max]


def is_similar_by_match_template(image: np.ndarray, template: np.ndarray, match_thres: float = 0.8) -> bool:
    """_summary_
    Matching two image by cv2.match_template

    Args:
        image (np.ndarray): image
        template (np.ndarray): template
        match_thres (float, optional): threshold for match template using TM_CCOEFF_NORMED. Defaults to 0.8.

    Returns:
        bool: matched
    """
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, max_value, _, _ = cv2.minMaxLoc(result)

    return max_value > match_thres


def is_similar_by_compare_ssim(image1: np.ndarray, image2: np.ndarray, match_thres: float = 0.99, resize_length: int = 224) -> bool:
    """_summary_
    Matching two image by cv2.match_template

    Args:
        image1 (np.ndarray): image1
        image2 (np.ndarray): image2
        match_thres (float, optional): threshold for compare ssim. Defaults to 0.99.
        resize_length (int, optional): resize size for same image space. Defaults to 224.

    Returns:
        bool: matched
    """
    image1 = cv2.resize(cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY), (resize_length, resize_length))
    image2 = cv2.resize(cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY), (resize_length, resize_length))

    return compare_ssim(image1, image2) > match_thres


def calc_diff_rate(image1: np.ndarray, image2: np.ndarray, min_color_depth_diff: int = 0) -> float:
    """_summary_

    Calculate diff rate for image1 and image2 by cv2.absdiff function

    Args:
        img1 (np.ndarray): image1
        img2 (np.ndarray): image2
        min_color_depth_diff (int, optional): pixel difference threshold. Defaults to 0. if this value is set to 0, only same image return 0

    Returns:
        float: Ratio to the number of pixels with a difference of more than a certain color depth
    """
    diff_image = cv2.absdiff(image1, image2)
    diff_num = np.count_nonzero(diff_image > min_color_depth_diff)
    pixels_num = np.prod(diff_image.shape)
    diff_rate = diff_num / pixels_num

    return diff_rate


def calc_image_value_rate(image: np.ndarray) -> float:
    """_summary_

    Calculate ratio of image pixel value to 0 to 1.

    Args:
        image (np.ndarray): image

    Returns:
        float: image pixel sum rate
    """

    image_value_sum = np.sum(image)
    pixels_num = int(np.prod(image.shape))
    value_rate = (image_value_sum / pixels_num) / 255
    return value_rate


def calc_image_whole_stdev(image: np.ndarray) -> float:
    """_summary_

    Calculate standard deviation of grayscaled image and normalize value to 0 to 1. 

    Args:
        image (np.ndarray): image

    Returns:
        float: grayscaled image standard deviation
    """
    mult = 2 / 255  # normalize stdev 0 ~ 127.5 to 0 ~ 1
    return np.std(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)) * mult


def calc_image_colorfulness(image: np.ndarray) -> float:
    """_summary_

    Calculate image colorfulness 
    https://www.researchgate.net/publication/243135534_Measuring_Colourfulness_in_Natural_Images

    Args:
        image (np.ndarray): _description_

    Returns:
        float: _description_
    """

    B, G, R = cv2.split(image.astype("float"))
    rg = np.absolute(R - G)
    yb = np.absolute(0.5 * (R + G) - B)
    rbMean, rbStd = np.mean(rg), np.std(rg)
    ybMean, ybStd = np.mean(yb), np.std(yb)
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
    return stdRoot + (0.3 * meanRoot)


def get_cursor_xywh(image: np.ndarray, cursor_type: str = 'universal') -> Tuple[int, int, int, int]:
    detector = CursorDetector(cursor_type)
    cursor_info = detector.get_cursor(image)
    if cursor_info is None:
        return None
    else:
        return cursor_info


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


def calc_iou(box1, box2):
    # xywh to x1y1x2y2
    box1 = [box1[0], box1[1], box1[0] + box1[2], box1[1] + box1[3]]
    box2 = [box2[0], box2[1], box2[0] + box2[2], box2[1] + box2[3]]

    # box = (x1, y1, x2, y2)
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    # obtain x1, y1, x2, y2 of the intersection
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # compute the width and height of the intersection
    w = max(0, x2 - x1 + 1)
    h = max(0, y2 - y1 + 1)

    inter = w * h
    iou = inter / (box1_area + box2_area - inter)
    return iou


def find_roku_cursor(image: np.ndarray, min_width: int=10) -> Tuple[int, int, int, int]:
    def is_rectangle(contour):
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        return len(approx) == 4

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 215, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    for contour in contours:
        if is_rectangle(contour):
            x, y, w, h = cv2.boundingRect(contour)
            if w >= min_width:
                candidates.append((x, y, w, h))
                # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw rectangle with green outline

    if len(candidates) > 0:
        x, y, w, h = max(candidates, key=lambda c: c[2])

        canvas = image.copy()
        cv2.rectangle(canvas, (x, y), (x+w, y+h), (0, 0, 255), 2)
        # cv2.imwrite('/app/datas/orig.png', image)
        # cv2.imwrite('/app/datas/cursor.png', canvas)

        return (x, y, w, h)
    else:
        return None
