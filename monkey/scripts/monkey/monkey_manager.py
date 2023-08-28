import logging

from scripts.util.process_maintainer import ProcessMaintainer
from scripts.monkey.monkey_test import MonkeyTest


logger = logging.getLogger('monkey_test')


class MonkeyManager:
    def __init__(self, company: str):
        self.monkey_proc = None
        self.company = company

    def __start_monkey_test(self):
        monkey_test = MonkeyTest(company=self.company)
        self.monkey_proc = ProcessMaintainer(
            name='monkey_test',
            target=monkey_test.run,
            daemon=True, 
            revive_interval=10
        )
        self.monkey_proc.start()

    def start(self):
        self.__start_monkey_test()
        logger.info('MonkeyManager start')

    def stop(self):
        if self.monkey_proc:
            self.monkey_proc.terminate()
        logger.info('MonkeyManager stop')
