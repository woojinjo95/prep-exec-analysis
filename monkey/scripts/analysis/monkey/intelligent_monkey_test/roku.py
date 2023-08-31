
from typing import Tuple, List
import logging

import numpy as np

from scripts.analysis.image import find_roku_cursor
from scripts.analysis.monkey.util import (get_current_image, check_cursor_is_same,
                                          exec_key, exec_keys, head_to_next, append_key,
                                          FrameInfo)

logger = logging.getLogger('monkey_test')


class IntelligentMonkeyTestRoku:
    def __init__(self, key_interval: float, duration_per_menu: float,
                 enable_smart_sense: bool, waiting_time: float):
        # set arguments
        self.key_interval = key_interval
        self.duration_per_menu = duration_per_menu
        self.enable_smart_sense = enable_smart_sense
        self.waiting_time = waiting_time

        # init variables
        self.profile = 'roku'
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

    ##### Visit #####
    def visit(self):
        candidates = []
        last_fi = None

        while True:
            self.exec_keys(self.key_histories)  # TODO: exit이랑 menu의 경우 interval이 다를 수 있어서, key,interval 형식으로 저장 필요

            image, cursor = get_current_image(), self.get_cursor()

            if last_fi and check_cursor_is_same(last_fi.image, last_fi.cursor, image, cursor):
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
            image = get_current_image()
            cursor = self.get_cursor()
            fi = FrameInfo(image, cursor)
            self.exec_key(self.depth_key)
            if self.check_leftmenu_is_opened(image, cursor, get_current_image(), self.get_cursor()):
                logger.info('right menu exists.')
                self.append_key(self.depth_key)
            else:
                logger.info('right menu does not exist.')
                candidates.append([*self.key_histories, self.depth_key])
                logger.info(f'candidates: {len(candidates)}')
                self.append_key('down')
                # 이미 위에서 right이 불가능하다고 판단하였으므로, 다음 시점에 down도 불가능하다면 이것은 leaf node일 것이므로, 현재 cursor를 저장해두기
                last_fi = fi

    ##### Re-Defined Functions #####
    def exec_key(self, key: str):
        exec_key(self.profile, key, self.key_interval)

    def exec_keys(self, keys: List[str]):
        exec_keys(keys, self.profile, self.key_interval)

    def append_key(self, key: str):
        append_key(self.key_histories, key)

    def head_to_next(self):
        head_to_next(self.key_histories, self.depth_key)

    ##### Functions #####
    def get_cursor(self) -> Tuple:
        return find_roku_cursor(get_current_image())

    def set_root_keys(self, external_keys: List[str] = []):
        self.key_histories = external_keys
        logger.info(f'root keys: {self.key_histories}')

        self.exec_keys(self.key_histories)
        self.root_cursor = self.get_cursor()
        logger.info(f'root cursor: {self.root_cursor}')

    def check_leftmenu_is_opened(self, prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple, max_height_diff: int=10) -> bool:
        if cursor is None:
            return False
        else:
            height_diff = abs(cursor[3] - self.root_cursor[3])
            is_height_similar = height_diff < max_height_diff

            is_cursor_same = check_cursor_is_same(prev_image, prev_cursor, image, cursor)
            
            return True if is_height_similar and not is_cursor_same else False
