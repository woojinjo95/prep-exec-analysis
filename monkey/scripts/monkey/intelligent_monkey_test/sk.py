
import logging
from typing import List, Tuple
import time
import threading

import numpy as np

from scripts.analysis.image import get_cropped_image
from scripts.monkey.format import NodeInfo, MonkeyArgs
from scripts.monkey.monkey import Monkey
from scripts.monkey.util import (check_cursor_is_same, check_shape_similar, 
                                 exec_keys_with_each_interval, get_current_image, head_to_parent_sibling,
                                 optimize_path, get_last_breadth_start_image,
                                 get_cursor)
from scripts.external.image import get_skipped_images
from scripts.external.image import save_section_cursor_image
from scripts.util._timezone import get_utc_datetime
from scripts.monkey.format import MonkeyExternalInfo


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
        self.skipped_images = get_skipped_images()

        # init variables
        self.main_stop_event = threading.Event()
        self.node_histories = []
        self.keyset = []
        self.section_id = 0

    ##### Entry Point #####
    def run(self):
        logger.info('start intelligent monkey test. mode: SK.')
        self.set_root_keyset(self.root_keyset)

        self.visit()
        logger.info('stop intelligent monkey test. mode: SK.')

    def stop(self):
        self.main_stop_event.set()

    ##### Visit #####
    def visit(self):
        while not self.main_stop_event.is_set():
            self.exec_keys(self.keyset)
            image = get_current_image()
            node_info = NodeInfo(image=image, cursor=self.get_cursor(image))

            if self.check_breadth_end(node_info):
                if self.head_to_next():
                    continue
                else:
                    return

            self.exec_keys([self.depth_key])
            if self.check_leaf_node(node_info):
                node_info.is_leaf = True
                self.start_monkey(node_info, [*self.keyset, self.depth_key])
                self.append_key(self.breadth_key)
            else:
                node_info.is_leaf = False
                self.append_key(self.depth_key)

            self.node_histories.append(node_info)

    def check_breadth_end(self, node_info: NodeInfo) -> bool:
        try:
            logger.info('check breadth end.')

            same_with_prev = check_cursor_is_same(self.node_histories[-1].image, self.node_histories[-1].cursor, 
                                                node_info.image, node_info.cursor, 
                                                sim_thld=0.98)
            last_breadth_start_image = get_last_breadth_start_image(self.node_histories)
            same_with_breadth_start = check_cursor_is_same(last_breadth_start_image, self.get_cursor(last_breadth_start_image),
                                                        node_info.image, node_info.cursor, 
                                                        sim_thld=0.98)

            breadth_end_cond = same_with_prev or same_with_breadth_start
            is_breadth_end = True if breadth_end_cond else False
            logger.info(f'check breadth end done. is_breadth_end: {is_breadth_end}, same_with_prev: {same_with_prev}, same_with_breadth_start: {same_with_breadth_start}')
            return is_breadth_end
        except Exception as err:
            logger.warning(f'check breadth end error. {err}')
            return False

    def check_leaf_node(self, node_info: NodeInfo) -> bool:
        logger.info('check leaf node.')
        leaf_node = False if self.check_leftmenu_opened(node_info.image, node_info.cursor, get_current_image(), self.get_cursor()) else True
        logger.info(f'check leaf node done. leaf node: {leaf_node}')
        return leaf_node

    ##### Functions #####
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

    def check_leftmenu_opened(self, prev_image: np.ndarray, prev_cursor: Tuple, image: np.ndarray, cursor: Tuple) -> bool:
        if cursor is None:
            return False
        shape_similar = check_shape_similar(self.root_cursor, cursor, 10, 10)
        is_cursor_same = check_cursor_is_same(prev_image, prev_cursor, image, cursor)
        return True if shape_similar and not is_cursor_same else False

    def append_key(self, key: str):
        self.keyset.append(key)
        self.keyset = optimize_path(self.keyset)

    def start_monkey(self, node_info: NodeInfo, current_node_keyset: List[str]):
        monkey = Monkey(
            duration=self.monkey_args.duration,
            key_candidates=['right', 'up', 'down', 'ok'],
            root_keyset=current_node_keyset,
            key_interval=self.key_interval,
            company=self.profile,
            remocon_type=self.remocon_type,
            enable_smart_sense=self.monkey_args.enable_smart_sense,
            waiting_time=self.monkey_args.waiting_time,
            external_info=MonkeyExternalInfo(
                analysis_type=self.analysis_type,
                section_id=self.section_id,
                image_path=save_section_cursor_image(get_utc_datetime(time.time()).strftime('%y-%m-%d_%H:%M:%S.%f'), 
                                                     get_cropped_image(node_info.image, node_info.cursor)),
            ),
            root_when_start=False,
        )
        monkey.run()

        if monkey.banned_image_detected:
            self.stop()
        self.section_id += 1

    ##### Skipped Image #####
    def compare_skipped_with_cursor(self, image: np.ndarray) -> bool:
        cursor = self.get_cursor(image)
        for skipped_image in self.skipped_images:
            skipped_cursor = self.get_cursor(skipped_image)
            if check_cursor_is_same(image, cursor, skipped_image, skipped_cursor):
                return True
        else:
            return False

    ##### Re-Defined Functions #####
    def exec_keys(self, keys: List[str]):
        key_and_intervals = [(key, self.key_interval) if key != 'home' else (key, 3) for key in keys]
        exec_keys_with_each_interval(key_and_intervals, self.profile, self.remocon_type)

    def head_to_next(self) -> bool:
        try:
            keyset = head_to_parent_sibling(self.keyset, self.depth_key, self.breadth_key)
            self.keyset = optimize_path(keyset)
            return True
        except Exception:
            return False

    def get_cursor(self, image: np.ndarray=None) -> Tuple[int, int, int, int]:
        try:
            if image is None:
                image = get_current_image()
            cursor = get_cursor(self.profile, image)
            return (cursor.x, cursor.y, cursor.w, cursor.h)
        except Exception as err:
            logger.warning(f'get cursor error. {err}')
            return None
