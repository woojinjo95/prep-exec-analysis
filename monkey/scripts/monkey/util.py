import logging
from typing import List, Tuple

import cv2
import numpy as np
from scripts.analysis.image import (calc_diff_rate, calc_iou, find_roku_cursor,
                                    get_cropped_image, get_cursor_xywh,
                                    is_similar_by_compare_ssim)
from scripts.control.image import get_snapshot
from scripts.control.remocon import publish_remocon_msg
from scripts.format import Cursor, NodeInfo

logger = logging.getLogger('monkey_test')


inverse_keys = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}


def get_current_image() -> np.ndarray:
    return get_snapshot()


def exec_key(key: str, key_interval: float, company: str, type: str):
    publish_remocon_msg(company, key, sleep=key_interval, type=type)


def exec_keys(keys: List[str], *args, **kwargs):
    logger.info(f'exec_keys: {keys}')
    for key in keys:
        exec_key(key, *args, **kwargs)
    # time.sleep(3)


def exec_keys_with_each_interval(key_and_intervals: List[Tuple[str, float]], company: str, type: str):
    logger.info(f'exec_keys: {key_and_intervals}')
    for key, interval in key_and_intervals:
        exec_key(key, interval, company, type)


def cursor_to_xywh(cursor: Cursor) -> Tuple[int, int, int, int]:
    return cursor.x, cursor.y, cursor.w, cursor.h


def get_cursor(company: str, image: np.ndarray) -> Cursor:
    try:
        if company == 'roku':
            cursor = find_roku_cursor(image)
            return Cursor(x=cursor[0], y=cursor[1], w=cursor[2], h=cursor[3])
        elif company == 'skb':
            cursor = get_cursor_xywh(image)
            return Cursor(x=cursor[0], y=cursor[1], w=cursor[2], h=cursor[3])
        else:
            raise Exception(f'invalid company. => {company}')
    except Exception as err:
        raise Exception(f'get cursor error. {err}')


def check_cursor_is_same(image1: np.ndarray, cursor1: Cursor, image2: np.ndarray, cursor2: Cursor, 
                        iou_thld: float=0.9, min_color_depth_diff: int=10, sim_thld: float=0.95) -> bool:
    if image1 is None or image2 is None or cursor1 is None or cursor2 is None:
        return False
    else:
        positional_similar = check_positional_similar(cursor1, cursor2, iou_thld)
        temporal_similar = check_image_similar(get_cropped_image(image1, cursor_to_xywh(cursor1)), 
                                            get_cropped_image(image2, cursor_to_xywh(cursor2)), 
                                            min_color_depth_diff, 
                                            sim_thld)
        same = positional_similar and temporal_similar
        # logger.info(f'check cursor is same. same: {same}, positional_similar: {positional_similar}, temporal_similar: {temporal_similar}')
        return same


def check_positional_similar(cursor1: Cursor, cursor2: Cursor, iou_thld: float=0.9) -> bool:
    iou_rate = calc_iou(cursor_to_xywh(cursor1), cursor_to_xywh(cursor2))
    return iou_rate > iou_thld


def check_image_similar(image1: np.ndarray, image2: np.ndarray, min_color_depth_diff: int=10, sim_thld: float=0.95) -> bool:
    def preprocess_image(image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(cv2.resize(image, (960, 540)), cv2.COLOR_BGR2GRAY)
    
    diff_rate = calc_diff_rate(preprocess_image(image1), preprocess_image(image2), min_color_depth_diff)
    sim_rate = 1 - diff_rate
    return sim_rate > sim_thld


def check_image_similar_with_ssim(image1: np.ndarray, image2: np.ndarray, sim_thld: float=0.95) -> bool:
    def preprocess_image(image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(cv2.resize(image, (960, 540)), cv2.COLOR_BGR2GRAY)
    
    sim_rate = is_similar_by_compare_ssim(preprocess_image(image1), preprocess_image(image2), match_thres=sim_thld)
    return sim_rate > sim_thld


def check_shape_similar(cursor1: Cursor, cursor2: Cursor, max_width_diff: int=10, max_height_diff: int=10) -> bool:
    width_diff = abs(cursor1.w - cursor2.w)
    height_diff = abs(cursor1.h - cursor2.h)
    is_width_similar = width_diff < max_width_diff
    is_height_similar = height_diff < max_height_diff
    return True if is_width_similar and is_height_similar else False


def optimize_path(path: List[str]) -> List[str]:
    stack = []
    for action in path:
        if stack and stack[-1] == inverse_keys.get(action):
            stack.pop()
        else:
            stack.append(action)
    return stack


# 다음 노드로 route를 변경
def head_to_parent_sibling(key_histories: List[str], depth_key: str, breadth_key: str) -> List[str]:
    try:
        while True:
            if key_histories[-1] == breadth_key:
                key_histories.pop()
            elif key_histories[-1] == depth_key:
                key_histories.pop()
                key_histories.append(breadth_key)
                logger.info(f'head to parent sibling. key_histories: {key_histories}')
                return key_histories
            else:
                logger.info(f'key_histories is invalid. key_histories: {key_histories}')
                raise ValueError('key_histories is invalid.')
    except IndexError:
        logger.info(f'key_histories is empty. key_histories: {key_histories}')
        raise IndexError('key_histories is empty.')


def get_last_breadth_start_image(node_histories: List[NodeInfo]):
    try:
        for i in range(len(node_histories) - 1, 0, -1):
            if not node_histories[i].is_leaf:
                return node_histories[i+1].image
        else:
            return node_histories[0].image
    except Exception as err:
        raise Exception(f'get last breadth start cursor image error. {err}')
