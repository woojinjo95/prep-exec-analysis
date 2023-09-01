
import logging
from typing import List
import time

import numpy as np

from scripts.external.report import report_data
from scripts.monkey.format import MonkeyArgs, RemoconInfo
from scripts.monkey.monkey import Monkey
from scripts.util._timezone import get_utc_datetime
from scripts.external.image import save_image
from scripts.external.redis import get_monkey_test_arguments

logger = logging.getLogger('monkey_test')


class MonkeyTest:
    def __init__(self, key_interval: float, monkey_args: MonkeyArgs, remocon_info: RemoconInfo):
        # set arguments
        self.key_interval = key_interval
        self.monkey_args = monkey_args
        self.remocon_info = remocon_info

        # init variables
        self.analysis_type = 'monkey'
        self.profile = 'roku'  # TODO: arg로 전달받은 리모콘을 사용
        self.section_id = 0

    ##### Entry Point #####
    def run(self):
        logger.info('start monkey test.')
        self.start_monkey()
        logger.info('stop monkey test.')

    ##### Functions #####
    def start_monkey(self, current_node_keyset: List[str]):
        start_time = time.time()




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
