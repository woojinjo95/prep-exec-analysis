import logging

from multiprocessing import Process
from scripts.processor.color_reference import process


logger = logging.getLogger('color_reference')


class ColorReference:
    def __init__(self):
        self.processor = None

    def __start_processor(self):
        self.processor = Process(target=process, kwargs={
        }, daemon=True)
        self.processor.start()

    def __stop_processor(self):
        self.processor.terminate()

    def start(self):
        if self.processor and self.processor.is_alive():
            logger.warning('ColorReference is already alive')
        else:
            self.__start_processor()
            logger.info('ColorReference start')

    def stop(self):
        if self.processor and self.processor.is_alive():
            self.__stop_processor()
            logger.info('ColorReference stop')
        else:
            logger.warning('ColorReference is not alive')
