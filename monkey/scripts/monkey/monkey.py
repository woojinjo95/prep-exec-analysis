import logging
import random
import threading
import time
from typing import Dict, List

import numpy as np

from scripts.external.report import report_data
from scripts.external.redis import get_monkey_test_arguments
from scripts.external.image import get_banned_images
from scripts.monkey.util import (check_image_similar, exec_keys,
                                 get_current_image)

logger = logging.getLogger('monkey_agent')


class Monkey:
    """_summary_
    press random keys for duration seconds.
    if smart sense is detected, go to root.
    """
    def __init__(self, duration: float, 
                 key_candidates: List[str], root_keyset: List[str], 
                 key_interval: float, company: str, remocon_type: str,
                 enable_smart_sense: bool=False, waiting_time: float=3, 
                 report_data: Dict={},
                 root_when_start: bool=True):
        self.duration = duration
        self.key_interval = key_interval
        self.key_candidates = key_candidates
        self.root_keyset = root_keyset
        self.company = company
        self.remocon_type = remocon_type
        self.enable_smart_sense = enable_smart_sense
        self.waiting_time = waiting_time
        self.report_data = report_data
        self.root_when_start = root_when_start
        logger.info(f'set monkey. args: {locals()}')

        self.main_stop_event = threading.Event()
        self.smart_sense_detected = False
        self.smart_sense_stop_event = threading.Event()
        self.smart_sense_count = 0

        self.banned_images = get_banned_images()
        self.banned_image_detected = False

    def run(self):
        logger.info('Start Monkey')
        self.main_stop_event.clear()
        start_time = time.time()

        if self.root_when_start:
            self.go_to_root()
        self.start_smart_sense()

        while not self.main_stop_event.is_set() and time.time() - start_time < self.duration:
            self.check_banned_image()
            self.press_random_key()

            if self.enable_smart_sense:
                if self.smart_sense_detected:
                    self.smart_sense_detected = False
                    self.stop_smart_sense()
                    self.report_smart_sense()
                    self.go_to_root()
                    self.start_smart_sense()

        logger.info('Stop Monkey')

    def stop(self):
        self.stop_smart_sense()
        self.main_stop_event.set()

    ##### Control Keys #####
    def exec_keys(self, keys: List[str]):
        exec_keys(keys, self.key_interval, self.company, self.remocon_type)

    def go_to_root(self):
        self.exec_keys(self.root_keyset)
        logger.info(f'go to root. {self.root_keyset}')

    def press_random_key(self):
        key = random.choice(self.key_candidates)
        self.exec_keys([key])

    ##### Smart Sense #####
    def smart_sense(self):
        prev_frame = None
        while not self.smart_sense_stop_event.is_set():
            time.sleep(self.waiting_time)
            frame = get_current_image()
            if prev_frame is not None:
                if check_image_similar(prev_frame, frame):
                    logger.info(f'smart sense is detected.')
                    self.smart_sense_detected = True
                    self.smart_sense_count += 1
                    break
            prev_frame = frame

    def start_smart_sense(self):
        self.smart_sense_stop_event.clear()
        th = threading.Thread(target=self.smart_sense, daemon=True)
        th.start()
        logger.info('start smart sense')

    def stop_smart_sense(self):
        self.smart_sense_stop_event.set()
        logger.info('stop smart sense')

    def report_smart_sense(self):
        data = {
            **self.report_data,
            'smart_sense_key': self.root_keyset,
            'user_config': get_monkey_test_arguments()
        }
        report_data('monkey_smart_sense', data)

    ##### Banned Image #####
    def compare_banned_image(self, image: np.ndarray) -> bool:
        return any([check_image_similar(image, banned_image) for banned_image in self.banned_images])

    def check_banned_image(self):
        snapshot = get_current_image()
        if self.compare_banned_image(snapshot):
            logger.info('banned image is detected.')
            self.stop()
            self.banned_image_detected = True
