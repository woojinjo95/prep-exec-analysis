
from typing import Tuple, List
import logging
import time

import numpy as np
import cv2

from scripts.control.image import get_snapshot
from scripts.control.remocon import publish_remocon_msg
from scripts.analysis.image import calc_iou, calc_diff_rate, get_cropped_image, find_roku_cursor

logger = logging.getLogger('monkey_test')


class IntelligentMonkeyTest:
    def __init__(self, profile: str, key_interval: float, duration_per_menu: float,
                 enable_smart_sense: bool, waiting_time: float):
        # set arguments
        self.profile = profile
        self.key_interval = key_interval
        self.duration_per_menu = duration_per_menu
        self.enable_smart_sense = enable_smart_sense
        self.waiting_time = waiting_time

        # init variables
        self.depth_key = 'right'
        self.inverse_keys = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }
        self.key_histories = []

    ##### Entry Point #####
    def run(self):
        self.set_root_keys(external_keys=['home'])
        self.visit()

    ##### Control #####
    def get_current_image(self) -> np.ndarray:
        return get_snapshot()

    def exec_key(self, key: str):
        publish_remocon_msg(self.profile, key, sleep=self.key_interval)
        time.sleep(self.key_interval)

    def exec_keys(self, keys: list, *args, **kwargs):
        logger.info(f'exec_keys: {keys}')
        for key in keys:
            self.exec_key(key, *args, **kwargs)
        # time.sleep(3)

    def check_cursor_is_same(self, prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple, 
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

    # 최초 루트 영역으로 이동
    def set_root_keys(self, external_keys: List[str] = []):
        self.key_histories = external_keys
        logger.info(f'root keys: {self.key_histories}')

        self.exec_keys(self.key_histories)
        self.root_cursor = self.get_cursor()
        logger.info(f'root cursor: {self.root_cursor}')

    def head_to_next(self):
        try:
            while True:
                if self.key_histories[-1] == 'down':
                    self.key_histories.pop()
                elif self.key_histories[-1] == self.depth_key:
                    self.key_histories.pop()
                    self.append_key('down')
                    break
                else:
                    logger.warning(f'key_histories: {self.key_histories}')
                    raise ValueError('key_histories is invalid.')
        except IndexError:
            logger.warning(f'key_histories: {self.key_histories}')
            raise IndexError('key_histories is empty.')

    def optimize_path(self, path: List[str]) -> List[str]:
        stack = []
        for action in path:
            if stack and stack[-1] == self.inverse_keys.get(action):
                stack.pop()
            else:
                stack.append(action)
        return stack

    def append_key(self, key: str):
        self.key_histories.append(key)
        self.key_histories = self.optimize_path(self.key_histories)

    def visit(self):
        candidates = []
        last_fi = None

        while True:
            self.exec_keys([*self.key_histories])  # TODO: exit이랑 menu의 경우 interval이 다를 수 있어서, key,interval 형식으로 저장 필요

            image, cursor = self.get_current_image(), self.get_cursor()

            if last_fi and self.check_cursor_is_same(last_fi.image, last_fi.cursor, image, cursor):
                logger.info('cursor does not same.')
                try:
                    logger.info('head to next.')
                    self.head_to_next()
                    logger.info(f'head to next done. {self.key_histories}')
                    last_fi = None
                    continue
                except IndexError as err:
                    logger.info(f'visit done. {self.key_histories}. {err}')
                    return
                
            logger.info('start right menu check.')
            image = self.get_current_image()
            cursor = self.get_cursor()
            fi = FrameInfo(image, cursor)
            self.exec_key(self.depth_key)
            if self.check_leftmenu_is_opened(image, cursor, self.get_current_image(), self.get_cursor()):
                logger.info('right menu exists.')
                self.append_key(self.depth_key)
            else:
                logger.info('right menu does not exist.')
                candidates.append([*self.key_histories, self.depth_key])
                logger.info(f'candidates: {len(candidates)}')
                self.append_key('down')
                # 이미 위에서 right이 불가능하다고 판단하였으므로, 다음 시점에 down도 불가능하다면 이것은 leaf node일 것이므로, 현재 cursor를 저장해두기
                last_fi = fi




    def get_cursor(self) -> Tuple:
        return find_roku_cursor(self.get_current_image())

    def check_leftmenu_is_opened(self, prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple, max_height_diff: int=10) -> bool:
        if cursor is None:
            return False
        else:
            height_diff = abs(cursor[3] - self.root_cursor[3])
            is_height_similar = height_diff < max_height_diff

            is_cursor_same = self.check_cursor_is_same(prev_image, prev_cursor, image, cursor)
            
            return True if is_height_similar and not is_cursor_same else False


class FrameInfo:
    def __init__(self, image: np.ndarray, cursor: Tuple[int, int, int, int]):
        self.image = image
        self.cursor = cursor
    