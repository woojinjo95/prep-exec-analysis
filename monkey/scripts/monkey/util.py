import logging
from typing import List, Tuple

import cv2
import numpy as np
from scripts.analysis.image import (calc_diff_rate, calc_iou, get_cropped_image, 
                                    get_cursor_xywh, find_roku_cursor)
from scripts.control.image import get_snapshot
from scripts.control.remocon import publish_remocon_msg
from scripts.monkey.format import NodeInfo, Cursor

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
    for key, interval in key_and_intervals:
        exec_key(key, interval, company, type)


def check_cursor_is_same(prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple, 
                        iou_thld: float=0.9, min_color_depth_diff: int=10, sim_thld: float=0.95) -> bool:
    # logger.info(f'cursor same check. prev_cursor: {prev_cursor}, cursor: {cursor}')
    if prev_image is None or image is None or prev_cursor is None or cursor is None:
        return False
    else:
        positional_similar = check_positional_similar(prev_cursor, cursor, iou_thld)
        temporal_similar = check_image_similar(get_cropped_image(prev_image, prev_cursor), 
                                        get_cropped_image(image, cursor), 
                                        min_color_depth_diff, 
                                        sim_thld)
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
def head_to_parent_sibling(key_histories: List[str], depth_key: str, breadth_key: str) -> List[str]:
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


def check_image_similar(image1: np.ndarray, image2: np.ndarray, min_color_depth_diff: int=10, sim_thld: float=0.95) -> bool:
    def preprocess_image(image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(cv2.resize(image, (960, 540)), cv2.COLOR_BGR2GRAY)
    
    diff_rate = calc_diff_rate(preprocess_image(image1), preprocess_image(image2), min_color_depth_diff)
    sim_rate = 1 - diff_rate
    # logger.info(f'check temporal similar. diff_rate: {diff_rate:.6f}, diff_thld: {diff_thld:.6f}')
    return sim_rate > sim_thld


def get_last_breadth_start_image(node_histories: List[NodeInfo]):
    try:
        for i in range(len(node_histories) - 1, 0, -1):
            if not node_histories[i].is_leaf:
                return node_histories[i+1].image
        else:
            return node_histories[0].image
    except Exception as err:
        raise Exception(f'get last breadth start cursor image error. {err}')


def get_cursor(company: str, image: np.ndarray=None) -> Cursor:
    try:
        if image is None:
            image = get_current_image()

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
    
