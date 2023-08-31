
from typing import Tuple, List
import logging

import numpy as np

from scripts.monkey.format import FrameInfo
from scripts.monkey.util import (get_current_image, check_cursor_is_same,
                                exec_keys, head_to_next, optimize_path)
from scripts.analysis.image import find_roku_cursor
from scripts.monkey.monkey import Monkey
from scripts.monkey.format import SmartSenseArgs

logger = logging.getLogger('monkey_test')


class IntelligentMonkeyTestRoku:
    def __init__(self, key_interval: float, duration_per_menu: float,
                 smart_sense_args: SmartSenseArgs):
        # set arguments
        self.key_interval = key_interval
        self.duration_per_menu = duration_per_menu
        self.smart_sense_args = smart_sense_args

        # init variables
        self.analysis_type = 'intelligent_monkey'
        self.profile = 'roku'
        self.depth_key = 'right'
        self.breadth_key = 'down'
        self.key_histories = []
        self.section_id = 0

    ##### Entry Point #####
    def run(self):
        self.set_root_keyset(external_keys=['home'])
        if not self.root_cursor:
            self.set_root_keyset(external_keys=['home'])  # try one more

        self.visit()

    ##### Visit #####
    def visit(self):
        last_fi = None

        while True:
            self.exec_keys(self.key_histories)

            # check current depth end
            image, cursor = get_current_image(), self.get_cursor()
            if last_fi and check_cursor_is_same(last_fi.image, last_fi.cursor, image, cursor):
                try:
                    logger.info('head to next.')
                    self.head_to_next()
                    logger.info(f'head to next done. {self.key_histories}')
                    last_fi = None
                    continue
                except IndexError as err:
                    logger.info(f'visit done. {self.key_histories}. {err}')
                    return
            
            # check next node exists
            image = get_current_image()
            cursor = self.get_cursor()
            fi = FrameInfo(image, cursor)
            self.exec_keys([self.depth_key])
            if self.check_leftmenu_is_opened(image, cursor, get_current_image(), self.get_cursor()):
                logger.info('next node exists.')
                self.append_key(self.depth_key)
            else:
                logger.info('next node does not exist.')
                current_node = [*self.key_histories, self.depth_key]
                logger.info(f'current_node: {current_node}')

                self.start_monkey(current_node)

                self.section_id += 1
                self.append_key(self.breadth_key)
            last_fi = fi

    ##### Functions #####
    def get_cursor(self) -> Tuple:
        return find_roku_cursor(get_current_image())

    def set_root_keyset(self, external_keys: List[str] = []):
        self.key_histories = external_keys
        logger.info(f'root keyset: {self.key_histories}')

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

    def append_key(self, key: str):
        self.key_histories.append(key)
        self.key_histories = optimize_path(self.key_histories)

    def start_monkey(self, current_node: List[str]):
        monkey = Monkey(
            duration=self.duration_per_menu,
            key_candidates=['right', 'up', 'down', 'ok'],
            root_keyset=current_node,
            key_interval=self.key_interval,
            profile=self.profile,
            enable_smart_sense=self.smart_sense_args.enable_smart_sense,
            waiting_time=self.smart_sense_args.waiting_time,
            report_data={
                'analysis_type': self.analysis_type,
                'section_id': self.section_id,
            }
        )
        monkey.run()

    ##### Re-Defined Functions #####
    def exec_keys(self, keys: List[str]):
        exec_keys(keys, self.key_interval, self.profile)

    def head_to_next(self):
        self.key_histories = head_to_next(self.key_histories, self.depth_key, self.breadth_key)
