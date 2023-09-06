
import logging
from typing import List, Tuple
import time
import threading

import numpy as np

from scripts.analysis.image import find_roku_cursor, get_cropped_image
from scripts.monkey.format import MonkeyArgs, NodeInfo
from scripts.monkey.monkey import Monkey
from scripts.monkey.util import (check_cursor_is_same, exec_keys,
                                 get_current_image, head_to_parent_sibling,
                                 optimize_path)
from scripts.external.report import report_section

logger = logging.getLogger('monkey_test')


class IntelligentMonkeyTestRoku:
    def __init__(self, key_interval: float, monkey_args: MonkeyArgs):
        # set arguments
        self.key_interval = key_interval
        self.monkey_args = monkey_args

        # init constant
        self.analysis_type = 'intelligent_monkey'
        self.profile = 'roku'
        self.remocon_type = 'ir'
        self.depth_key = 'right'
        self.breadth_key = 'down'
        self.root_keyset = ['home']

        # init variables
        self.main_stop_event = threading.Event()
        self.node_histories = []
        self.keyset = []
        self.section_id = 0

    ##### Entry Point #####
    def run(self):
        logger.info('start intelligent monkey test. mode: ROKU.')
        self.set_root_keyset(self.root_keyset)

        self.visit()
        logger.info('stop intelligent monkey test. mode: ROKU.')

    def stop(self):
        self.main_stop_event.set()

    ##### Visit #####
    def visit(self):
        while not self.main_stop_event.is_set():
            self.exec_keys(self.keyset)
            image = get_current_image()
            node_info = NodeInfo(image=image, cursor=self.get_cursor(image))
            node_info.cursor_image = self.get_cursor_image(node_info.image, node_info.cursor)

            status = self.check_end(node_info)
            if status == 'breadth_end':
                continue
            elif status == 'visit_end':
                return

            self.exec_keys([self.depth_key])
            if self.check_leaf_node(node_info):
                self.start_monkey(node_info, [*self.keyset, self.depth_key])
                self.append_key(self.breadth_key)
            else:
                self.append_key(self.depth_key)

            self.node_histories.append(node_info)

    def check_end(self, node_info: NodeInfo) -> str:
        try:
            logger.info('check status.')
            if check_cursor_is_same(self.node_histories[-1].image, self.node_histories[-1].cursor, 
                                    node_info.image, node_info.cursor):
                try:
                    self.head_to_next()
                    logger.info(f'head to next done. {self.keyset}')
                    return 'breadth_end'
                except IndexError as err:
                    logger.info(f'visit done. {self.keyset}. {err}')
                    return 'visit_end'
            else:
                return ''
        except Exception as err:
            logger.warning(f'check end error. {err}')
            return ''

    def check_leaf_node(self, node_info: NodeInfo) -> bool:
        leaf_node = False if self.check_leftmenu_is_opened(node_info.image, node_info.cursor, get_current_image(), self.get_cursor()) else True
        logger.info(f'leaf node: {leaf_node}')
        return leaf_node

    ##### Functions #####
    def get_cursor(self, image: np.ndarray=None) -> Tuple:
        if image is None:
            image = get_current_image()
        return find_roku_cursor(image)

    def set_root_keyset(self, keys: List[str] = [], find_root_cursor_max_try: int=3):
        for try_count in range(find_root_cursor_max_try):
            self.keyset = keys
            logger.info(f'root keyset: {self.keyset}')
            self.exec_keys(self.keyset)
            self.root_cursor = self.get_cursor()
            logger.info(f'root cursor: {self.root_cursor}. try_count: {try_count}')
            if self.root_cursor:
                break
        else:
            logger.info(f'cannot find root cursor. try_count: {try_count}')
            raise Exception('cannot find root cursor')
        
    def check_leftmenu_is_opened(self, prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple, max_height_diff: int=10) -> bool:
        if cursor is None:
            return False
        else:
            height_diff = abs(cursor[3] - self.root_cursor[3])
            is_height_similar = height_diff < max_height_diff

            is_cursor_same = check_cursor_is_same(prev_image, prev_cursor, image, cursor)
            
            return True if is_height_similar and not is_cursor_same else False

    def append_key(self, key: str):
        self.keyset.append(key)
        self.keyset = optimize_path(self.keyset)

    def get_cursor_image(self, image: np.ndarray=None, cursor: Tuple=None) -> np.ndarray:
        if image is None:
            image = get_current_image()
        if cursor is None:
            cursor = self.get_cursor(image)
        return get_cropped_image(image, cursor)

    def start_monkey(self, node_info: NodeInfo, current_node_keyset: List[str]):
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
            },
            root_when_start=False,
        )
        monkey.run()

        report_section(start_time=start_time, 
                       end_time=time.time(),
                       analysis_type=self.analysis_type,
                       section_id=self.section_id,
                       image=node_info.cursor_image,
                       smart_sense_times=monkey.smart_sense_count)

        if monkey.banned_image_detected:
            self.stop()
        self.section_id += 1

    ##### Re-Defined Functions #####
    def exec_keys(self, keys: List[str]):
        exec_keys(keys, self.key_interval, self.profile, self.remocon_type)

    def head_to_next(self):
        self.keyset = head_to_parent_sibling(self.keyset, self.depth_key, self.breadth_key)
