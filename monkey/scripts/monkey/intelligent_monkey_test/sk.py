
import logging
from typing import List, Tuple
import time
import threading

import numpy as np

from scripts.analysis.image import get_cursor_xywh, get_cropped_image
from scripts.external.report import report_data
from scripts.monkey.format import FrameInfo, MonkeyArgs
from scripts.monkey.monkey import Monkey
from scripts.monkey.util import (check_cursor_is_same, exec_keys_with_each_interval,
                                 get_current_image, head_to_next,
                                 optimize_path)
from scripts.util._timezone import get_utc_datetime
from scripts.external.image import save_image
from scripts.external.redis import get_monkey_test_arguments

logger = logging.getLogger('monkey_test')


class IntelligentMonkeyTestSK:
    def __init__(self, key_interval: float, monkey_args: MonkeyArgs):
        # set arguments
        self.key_interval = key_interval
        self.monkey_args = monkey_args

        # init constant
        self.analysis_type = 'intelligent_monkey'
        self.profile = 'skb'
        self.remocon_type = 'ir'
        self.depth_key = 'right'
        self.breadth_key = 'down'
        # root keyset 근거
        # 1. 배터리 방전 팝업 없애기 위해 home 두번 입력
        # 2. 검증 대상 셋탑의 경우, up 4회
        self.root_keyset = ['home', 'home', 'left'] + ['up'] * 4

        # init variables
        self.last_fi = None
        self.key_histories = []
        self.section_id = 0
        self.main_stop_event = threading.Event()

    ##### Entry Point #####
    def run(self):
        logger.info('start intelligent monkey test. mode: SK.')
        self.set_root_keyset(self.root_keyset)
        if not self.root_cursor:
            self.set_root_keyset(self.root_keyset)  # try one more

        self.visit()
        logger.info('stop intelligent monkey test. mode: SK.')

    def stop(self):
        self.main_stop_event.set()

    ##### Visit #####
    def visit(self):
        while not self.main_stop_event.is_set():
            self.exec_keys(self.key_histories)
            status = self.check_status()
            if status == 'depth_end':
                continue
            elif status == 'visit_end':
                return

            if self.check_leaf_node():
                current_node_keyset = [*self.key_histories, self.depth_key]
                logger.info(f'current_node_keyset: {current_node_keyset}')
                self.start_monkey(current_node_keyset, self.cursor_image)
                self.append_key(self.breadth_key)
            else:
                self.append_key(self.depth_key)

    def check_status(self) -> str:
        logger.info('check status.')
        image, cursor = get_current_image(), self.get_cursor()
        if self.last_fi and check_cursor_is_same(self.last_fi.image, self.last_fi.cursor, image, cursor):
            try:
                self.head_to_next()
                logger.info(f'head to next done. {self.key_histories}')
                self.last_fi = None
                return 'depth_end'
            except IndexError as err:
                logger.info(f'visit done. {self.key_histories}. {err}')
                return 'visit_end'
        else:
            return 'none'

    def check_leaf_node(self):
        logger.info('check leaf node.')
        image = get_current_image()
        cursor = self.get_cursor()
        fi = FrameInfo(image, cursor)
        self.cursor_image = self.get_cursor_image(image, cursor)

        self.exec_keys([self.depth_key])

        leaf_node = False
        if self.check_leftmenu_is_opened(image, cursor, get_current_image(), self.get_cursor()):
            leaf_node = False
        else:
            leaf_node = True
        logger.info(f'leaf node: {leaf_node}')

        self.last_fi = fi
        return leaf_node

    ##### Functions #####
    def get_cursor(self, image: np.ndarray=None) -> Tuple:
        if image is None:
            image = get_current_image()
        return get_cursor_xywh(image)

    def set_root_keyset(self, keys: List[str] = []):
        self.key_histories = keys
        logger.info(f'root keyset: {self.key_histories}')

        self.exec_keys(self.key_histories)
        self.root_cursor = self.get_cursor()
        logger.info(f'root cursor: {self.root_cursor}')

    def check_leftmenu_is_opened(self, prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple, 
                                 max_width_diff: int=10, max_height_diff: int=10) -> bool:
        if cursor is None:
            return False
        else:
            width_diff = abs(cursor[2] - self.root_cursor[2])
            height_diff = abs(cursor[3] - self.root_cursor[3])
            is_width_similar = width_diff < max_width_diff
            is_height_similar = height_diff < max_height_diff

            is_cursor_same = check_cursor_is_same(prev_image, prev_cursor, image, cursor)
            
            return True if is_width_similar and is_height_similar and not is_cursor_same else False

    def append_key(self, key: str):
        self.key_histories.append(key)
        self.key_histories = optimize_path(self.key_histories)

    def get_cursor_image(self, image: np.ndarray=None, cursor: Tuple=None) -> np.ndarray:
        if image is None:
            image = get_current_image()
        if cursor is None:
            cursor = self.get_cursor(image)
        return get_cropped_image(image, cursor)

    def start_monkey(self, current_node_keyset: List[str], cursor_image: np.ndarray):
        start_time = time.time()

        monkey = Monkey(
            duration=self.monkey_args.duration,
            key_candidates=['right', 'up', 'down', 'ok'],
            root_keyset=current_node_keyset,
            key_interval=self.key_interval,
            company=self.profile,
            remocon_type=self.remocon_type,
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

        if monkey.banned_image_detected:
            self.stop()
        
        self.section_id += 1

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
        logger.info(f'exec_keys: {keys}')
        key_and_intervals = [(key, self.key_interval) if key != 'home' else (key, 3) for key in keys]
        exec_keys_with_each_interval(key_and_intervals, self.profile, self.remocon_type)

    def head_to_next(self):
        self.key_histories = head_to_next(self.key_histories, self.depth_key, self.breadth_key)
