
import logging
import time

from scripts.monkey.format import MonkeyArgs, RemoconInfo
from scripts.monkey.monkey import Monkey
from scripts.external.report import report_section

logger = logging.getLogger('monkey_test')


class MonkeyTest:
    def __init__(self, key_interval: float, monkey_args: MonkeyArgs, remocon_info: RemoconInfo):
        # set arguments
        self.key_interval = key_interval
        self.monkey_args = monkey_args
        self.remocon_info = remocon_info

        # init constants
        self.analysis_type = 'monkey'
        self.section_id = 0

    ##### Entry Point #####
    def run(self):
        logger.info('start monkey test.')
        self.start_monkey()
        logger.info('stop monkey test.')

    ##### Functions #####
    def start_monkey(self):
        start_time = time.time()

        monkey = Monkey(
            duration=self.monkey_args.duration,
            key_candidates=['left', 'right', 'up', 'down', 'ok', 'back', 'home'],
            root_keyset=['home'],
            key_interval=self.key_interval,
            company=self.remocon_info.remocon_name,
            remocon_type=self.remocon_info.remote_control_type,
            enable_smart_sense=self.monkey_args.enable_smart_sense,
            waiting_time=self.monkey_args.waiting_time,
            report_data={
                'analysis_type': self.analysis_type,
                'section_id': self.section_id,
            }
        )
        monkey.run()

        report_section(
            start_time=start_time,
            end_time=time.time(),
            analysis_type=self.analysis_type,
            section_id=self.section_id,
            image=None,
            smart_sense_times=monkey.smart_sense_count
        )
