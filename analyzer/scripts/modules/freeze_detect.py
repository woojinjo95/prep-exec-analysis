import logging
from multiprocessing import Process
from scripts.processor.freeze_detect import detect_freeze


logger = logging.getLogger('freeze_detect')


class FreezeDetect:
    def __init__(self):
        self.processor = None

    def __start_processor(self):
        self.processor = Process(target=detect_freeze, kwargs={
        }, daemon=True, revive_interval=10)
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
