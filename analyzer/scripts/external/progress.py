import logging
import time
from scripts.external.scenario import update_analysis_to_scenario
from scripts.format import Command


logger = logging.getLogger('main')


class ProgressManager:
    def __init__(self, analysis_type: str):
        self.start_time = time.time()
        self.analysis_type = analysis_type
        self.progress = 0
        self.remaining_time = 0
        self.update_progress(0)

    def __del__(self):
        self.update_progress(1)

    def calculate_remaining_time(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        try:
            self.remaining_time = elapsed_time / self.progress - elapsed_time
        except ZeroDivisionError:
            self.remaining_time = 0
        logger.info(f'Progress: {self.progress:.2%} | Remaining time: {self.remaining_time:.2f}s')

    def update_progress(self, progress: float):
        self.progress = progress
        self.calculate_remaining_time()
        self.report_progress()

    def report_progress(self):
        if self.analysis_type != Command.COLOR_REFERENCE.value:
            update_analysis_to_scenario(self.analysis_type, {
                'progress': self.progress,
                'remaining_time': self.remaining_time,
            })
