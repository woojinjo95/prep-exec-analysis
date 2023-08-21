import logging
from typing import Callable
from multiprocessing import Process


logger = logging.getLogger('main')


class Module:
    def __init__(self, func: Callable):
        self.func = func
        self.processor = None

    def __start_processor(self):
        self.processor = Process(target=self.func, kwargs={
        }, daemon=True)
        self.processor.start()

    def __stop_processor(self):
        self.processor.terminate()

    def start(self):
        if self.processor and self.processor.is_alive():
            logger.warning(f'{self.__class__.__name__} is already alive')
        else:
            self.__start_processor()
            logger.info(f'{self.__class__.__name__} start')

    def stop(self):
        if self.processor and self.processor.is_alive():
            self.__stop_processor()
            logger.info(f'{self.__class__.__name__} stop')
        else:
            logger.warning(f'{self.__class__.__name__} is not alive')
