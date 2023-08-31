import cv2
import numpy as np
from typing import Tuple, List
import logging
import threading
import time

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


def exec_key(key: str, key_interval: float, profile: str):
    publish_remocon_msg(profile, key, sleep=key_interval)


def exec_keys(keys: List[str], *args, **kwargs):
    logger.info(f'exec_keys: {keys}')
    for key in keys:
        exec_key(key, *args, **kwargs)
    # time.sleep(3)


def check_cursor_is_same(prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple, 
                        iou_thld: float=0.9, min_color_depth_diff: int=10, diff_thld: float=0.05) -> bool:
    # logger.info(f'cursor same check. prev_cursor: {prev_cursor}, cursor: {cursor}')
    if prev_image is None or image is None or prev_cursor is None or cursor is None:
        return False
    else:
        positional_similar = check_positional_similar(prev_cursor, cursor, iou_thld)
        temporal_similar = check_temporal_similar(get_cropped_image(prev_image, prev_cursor), 
                                        get_cropped_image(image, cursor), 
                                        min_color_depth_diff, 
                                        diff_thld)
        # 1. 위치적 동일성이 일정 수준 이하 => 커서가 움직임
        # 2. 위치적 동일성이 높지만, 시간적 동일성이 낮음 => 커서는 움직이지 않았지만, 내용물이 변함
        same = False if not positional_similar or (positional_similar and not temporal_similar) else True
        logger.info(f'check cursor is same. same: {same}, positional_similar: {positional_similar}, temporal_similar: {temporal_similar}')
        return same


def optimize_path(path: List[str]) -> List[str]:
    stack = []
    for action in path:
        if stack and stack[-1] == inverse_keys.get(action):
            stack.pop()
        else:
            stack.append(action)
    return stack


# 다음 노드로 route를 변경
def head_to_next(key_histories: List[str], depth_key: str, breadth_key: str) -> List[str]:
    try:
        while True:
            if key_histories[-1] == breadth_key:
                key_histories.pop()
            elif key_histories[-1] == depth_key:
                key_histories.pop()
                key_histories.append(breadth_key)
                return key_histories
            else:
                logger.warning(f'key_histories: {key_histories}')
                raise ValueError('key_histories is invalid.')
    except IndexError:
        logger.warning(f'key_histories: {key_histories}')
        raise IndexError('key_histories is empty.')


def check_positional_similar(prev_cursor: Tuple, cursor: Tuple, iou_thld: float=0.9) -> bool:
    iou_rate = calc_iou(prev_cursor, cursor)
    # logger.info(f'check positional similar. iou_rate: {iou_rate:.6f}, iou_thld: {iou_thld:.6f}')
    return iou_rate > iou_thld


def check_temporal_similar(prev_image: np.ndarray, image: np.ndarray, min_color_depth_diff: int=10, diff_thld: float=0.05) -> bool:
    def preprocess_image(image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(cv2.resize(image, (960, 540)), cv2.COLOR_BGR2GRAY)
    
    diff_rate = calc_diff_rate(preprocess_image(prev_image), preprocess_image(image), min_color_depth_diff)
    # logger.info(f'check temporal similar. diff_rate: {diff_rate:.6f}, diff_thld: {diff_thld:.6f}')
    return diff_rate < diff_thld
