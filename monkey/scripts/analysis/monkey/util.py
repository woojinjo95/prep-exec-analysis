import cv2
import numpy as np
from typing import Tuple, List
import logging

from scripts.control.image import get_snapshot
from scripts.control.remocon import publish_remocon_msg
from scripts.analysis.image import calc_iou, calc_diff_rate, get_cropped_image


logger = logging.getLogger('monkey_test')


inverse_keys = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}


def get_current_image() -> np.ndarray:
    return get_snapshot()


def exec_key(profile: str, key: str, key_interval: float):
    publish_remocon_msg(profile, key, sleep=key_interval)


def exec_keys(keys: List[str], *args, **kwargs):
    logger.info(f'exec_keys: {keys}')
    for key in keys:
        exec_key(key, *args, **kwargs)
    # time.sleep(3)


def check_cursor_is_same(prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple, 
                        iou_thld: float=0.9, min_color_depth_diff: int=10, diff_thld: float=0.05) -> bool:
    def preprocess_image(image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(cv2.resize(image, (960, 540)), cv2.COLOR_BGR2GRAY)

    logger.info(f'cursor same check. prev_cursor: {prev_cursor}, cursor: {cursor}')
    if prev_image is None or image is None or prev_cursor is None or cursor is None:
        return False
    else:
        iou_rate = calc_iou(prev_cursor, cursor)
        diff_rate = calc_diff_rate(preprocess_image(get_cropped_image(prev_image, prev_cursor)), 
                                preprocess_image(get_cropped_image(image, cursor)), 
                                min_color_depth_diff)
        # 1. iou가 일정 이상 작음 => 커서가 움직임
        # 2. iou가 일정 이상 크지만 diff가 일정이상 큼 => 커서는 움직이지 않았지만, 내용물이 변함
        same = False if iou_rate < iou_thld or (iou_rate > iou_thld and diff_rate > diff_thld) else True
        logger.info(f'same: {same}, iou_rate: {iou_rate}, iou_thld: {iou_thld:.6f}, diff_rate: {diff_rate}, diff_thld: {diff_thld:.6f}')
        return same


def optimize_path(path: List[str]) -> List[str]:
    stack = []
    for action in path:
        if stack and stack[-1] == inverse_keys.get(action):
            stack.pop()
        else:
            stack.append(action)
    return stack


class FrameInfo:
    def __init__(self, image: np.ndarray, cursor: Tuple[int, int, int, int]):
        self.image = image
        self.cursor = cursor
    