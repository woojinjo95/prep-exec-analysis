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


# 이미지 GET
def get_current_image() -> np.ndarray:
    return get_snapshot()


# 키 입력
def exec_key(key: str, key_interval: float, profile: str):
    publish_remocon_msg(profile, key, sleep=key_interval)


# 여러 키 입력
def exec_keys(keys: List[str], *args, **kwargs):
    logger.info(f'exec_keys: {keys}')
    for key in keys:
        exec_key(key, *args, **kwargs)
    # time.sleep(3)


# 이전과 현재 커서의 동일성 체크
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


# 주어진 루트 최적화
def optimize_path(path: List[str]) -> List[str]:
    stack = []
    for action in path:
        if stack and stack[-1] == inverse_keys.get(action):
            stack.pop()
        else:
            stack.append(action)
    return stack


# 다음 노드로 루트를 변경
def head_to_next(key_histories: List[str], depth_key: str) -> List[str]:
    try:
        while True:
            if key_histories[-1] == 'down':
                key_histories.pop()
            elif key_histories[-1] == depth_key:
                key_histories.pop()
                key_histories.append('down')
                return key_histories
            else:
                logger.warning(f'key_histories: {key_histories}')
                raise ValueError('key_histories is invalid.')
    except IndexError:
        logger.warning(f'key_histories: {key_histories}')
        raise IndexError('key_histories is empty.')

    

class FrameInfo:
    def __init__(self, image: np.ndarray, cursor: Tuple[int, int, int, int]):
        self.image = image
        self.cursor = cursor
    