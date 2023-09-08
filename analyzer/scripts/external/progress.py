import logging
import time
from scripts.format import Command
from scripts.external.scenario import update_progress_to_scenario


logger = logging.getLogger('main')


class ProgressManager:
    def __init__(self, command: Command):
        self.start_time = time.time()
        self.command = command
        self.progress = 0
        self.remaining_time = 0
        self.update_progress(0)

    def __del__(self):
        self.update_progress(1)

    def calculate_progress(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        try:
            self.remaining_time = elapsed_time / self.progress - elapsed_time
        except ZeroDivisionError:
            self.remaining_time = 0
        logger.info(f'Progress: {self.progress:.2%} | Remaining time: {self.remaining_time:.2f}s')

    def update_progress(self, progress: float):
        self.progress = progress
        self.calculate_progress()
        self.report_progress()

    def report_progress(self):
        update_progress_to_scenario(self.command.value, {
            'progress': self.progress,
            'remaining_time': self.remaining_time
        })
    