import ctypes
import logging
import multiprocessing
import os
import random
import signal
import threading
import time
from typing import List

import numpy as np
from scripts.external.image import get_banned_images
from scripts.external.redis import get_monkey_test_arguments
from scripts.external.report import create_section, report_data, update_section
from scripts.format import MonkeyExternalInfo, SectionData
from scripts.monkey.util import (check_image_similar, exec_keys,
                                 get_current_image)
from scripts.util._timezone import get_utc_datetime

logger = logging.getLogger('monkey_agent')


class Monkey:
    def __init__(self, duration: float,
                 key_candidates: List[str], root_keyset: List[str], 
                 key_interval: float, company: str, remocon_type: str,
                 enable_smart_sense: bool=False, waiting_time: float=3, 
                 external_info: MonkeyExternalInfo=None,
                 root_when_start: bool=True):
        self.duration = duration
        self.key_interval = key_interval
        self.key_candidates = key_candidates
        self.root_keyset = root_keyset
        self.company = company
        self.remocon_type = remocon_type
        self.enable_smart_sense = enable_smart_sense
        self.waiting_time = waiting_time
        self.external_info = external_info
        self.root_when_start = root_when_start
        logger.info(f'set monkey. args: {locals()}')

        if not self.external_info:
            self.external_info = MonkeyExternalInfo()

        self.main_stop_event = multiprocessing.Event()

        self.smart_sense_detected = False
        self.smart_sense_stop_event = threading.Event()
        self.smart_sense_count = 0

        self.banned_images = get_banned_images()
        self.banned_image_detected = multiprocessing.Value(ctypes.c_bool, False)

        self.create_section()

    def run(self):
        logger.info('Start Monkey')
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

        self.stop_smart_sense()
        logger.info('Stop Monkey')

    def stop(self):
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
        while not self.main_stop_event.is_set() and not self.smart_sense_stop_event.is_set():
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
        logger.info('stop smart sense')  # can delayed to stop (because of waiting_time)

    def report_smart_sense(self):
        data = {
            'analysis_type': self.external_info.analysis_type,
            'section_id': self.external_info.section_id,
            'smart_sense_key': self.root_keyset,
            'user_config': get_monkey_test_arguments()
        }
        report_data('monkey_smart_sense', data)
        self.update_section(SectionData(smart_sense_times=self.smart_sense_count))

    ##### Section #####
    def create_section(self):
        section_data = SectionData(
            start_timestamp=get_utc_datetime(time.time()),
            end_timestamp=get_utc_datetime(time.time()),
            analysis_type=self.external_info.analysis_type,
            section_id=self.external_info.section_id,
            image_path=self.external_info.image_path,
            smart_sense_times=0,
            user_config=get_monkey_test_arguments()
        )
        self.section_report_id = create_section(section_data)
        self.start_end_time_updator()

    def update_section(self, section_in: SectionData):
        update_section(self.section_report_id, section_in)

    def start_end_time_updator(self):
        def end_time_updator():
            while not self.main_stop_event.is_set():
                self.update_section(SectionData(end_timestamp=get_utc_datetime(time.time())))
                time.sleep(0.5)
        th = threading.Thread(target=end_time_updator, daemon=True)
        th.start()

    ##### Banned Image #####
    def compare_banned_image(self, image: np.ndarray) -> bool:
        return any([check_image_similar(image, banned_image) for banned_image in self.banned_images])

    def check_banned_image(self):
        snapshot = get_current_image()
        if self.compare_banned_image(snapshot):
            logger.info('banned image is detected.')
            self.banned_image_detected.value = True
            self.stop()


def run_monkey(monkey: Monkey):
    monkey_proc = multiprocessing.Process(target=monkey.run, daemon=True)
    monkey_proc.start()

    def stop_monkey():
        monkey.stop()  # to kill all threads in monkey because threads are not killed though process is daemon.
        monkey_proc.terminate()

    # the process hierachy is A(main) - B(test_module) - C(monkey_agent). 
    # A - B(daemon=False) - C(daemon=True) is forced because python daemon process cannot have child process.
    # so C must have signal handler because B is non daemon process. (non daemon means that it cannot be auto terminated when parent process is terminated.)
    def signal_handler(signum, frame):
        stop_monkey()
        os._exit(0)
    # stop child process(Monkey Agent) when signal is received. (SIGTERM)
    # if not, child process will be alive even if parent process is terminated.
    signal.signal(signal.SIGTERM, signal_handler)

    start_time = time.time()
    current_duration = time.time() - start_time
    while monkey_proc.is_alive() and current_duration < monkey.duration:
        time.sleep(0.1)
        current_duration = time.time() - start_time
    logger.info(f'stop monkey process. current_duration: {current_duration} sec, duration: {monkey.duration} sec')

    stop_monkey()
