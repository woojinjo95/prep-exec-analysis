import logging

from scripts.util.process_maintainer import ProcessMaintainer
from scripts.monkey.intelligent_monkey_test import IntelligentMonkeyTest


logger = logging.getLogger('monkey_test')


class MonkeyManager:
    def __init__(self, company: str, key_interval: float):
        self.monkey_proc = None
        self.company = company
        self.key_interval = key_interval

    def __start_monkey_test(self):
        monkey_test = IntelligentMonkeyTest(company=self.company, key_interval=self.key_interval)
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
