
import logging
from typing import List, Tuple
import time

import numpy as np

from scripts.analysis.image import find_roku_cursor, get_cropped_image
from scripts.external.report import report_data
from scripts.monkey.format import FrameInfo, MonkeyArgs
from scripts.monkey.monkey import Monkey
from scripts.monkey.util import (check_cursor_is_same, exec_keys,
                                 get_current_image, head_to_next,
                                 optimize_path)
from scripts.util._timezone import get_utc_datetime
from scripts.external.image import save_image
from scripts.external.redis import get_monkey_test_arguments

logger = logging.getLogger('monkey_test')


class IntelligentMonkeyTestRoku:
    def __init__(self, key_interval: float, monkey_args: MonkeyArgs):
        # set arguments
        self.key_interval = key_interval
        self.monkey_args = monkey_args

        # init variables
        self.analysis_type = 'intelligent_monkey'
        self.profile = 'roku'
        self.depth_key = 'right'
        self.breadth_key = 'down'
        self.key_histories = []
        self.section_id = 0

    ##### Entry Point #####
    def run(self):
        logger.info('start intelligent monkey test. mode: ROKU.')
        self.set_root_keyset(external_keys=['home'])
        if not self.root_cursor:
            self.set_root_keyset(external_keys=['home'])  # try one more

        self.visit()
        logger.info('stop intelligent monkey test. mode: ROKU.')

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
                current_node_keyset = [*self.key_histories, self.depth_key]
                logger.info(f'current_node_keyset: {current_node_keyset}')

                self.start_monkey(current_node_keyset)

                self.section_id += 1
                self.append_key(self.breadth_key)
            last_fi = fi

    ##### Functions #####
    def get_cursor(self, image: np.ndarray=None) -> Tuple:
        if image is None:
            image = get_current_image()
        return find_roku_cursor(image)

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

    def start_monkey(self, current_node_keyset: List[str]):
        start_time = time.time()

        # go to root_keyset of section and get snapshot
        self.exec_keys(current_node_keyset + ['left'])
        image = get_current_image()
        cursor_image = get_cropped_image(image, self.get_cursor(image))

        monkey = Monkey(
            duration=self.monkey_args.duration,
            key_candidates=['right', 'up', 'down', 'ok'],
            root_keyset=current_node_keyset,
            key_interval=self.key_interval,
            profile=self.profile,
            enable_smart_sense=self.monkey_args.enable_smart_sense,
            waiting_time=self.monkey_args.waiting_time,
            report_data={
                'analysis_type': self.analysis_type,
                'section_id': self.section_id,
            }
        )
        monkey.run()

        end_time = time.time()
        self.report_section(start_time, end_time, cursor_image, monkey.smart_sense_count)

    def report_section(self, start_time: float, end_time: float, image: np.ndarray, smart_sense_times: int):
        image_path = save_image(get_utc_datetime(time.time()).strftime('%y-%m-%d %H:%M:%S'), image)

        report_data('monkey_section', {
            'start_timestamp': get_utc_datetime(start_time),
            'end_timestamp': get_utc_datetime(end_time),
            'analysis_type': self.analysis_type,
            'section_id': self.section_id,
            'image_path': image_path,
            'smart_sense_times': smart_sense_times,
            'user_config': get_monkey_test_arguments()
        })

    ##### Re-Defined Functions #####
    def exec_keys(self, keys: List[str]):
        exec_keys(keys, self.key_interval, self.profile)

    def head_to_next(self):
        self.key_histories = head_to_next(self.key_histories, self.depth_key, self.breadth_key)
