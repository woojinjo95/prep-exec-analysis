import logging

from scripts.util.process_maintainer import ProcessMaintainer
from scripts.processor.color_reference import postprocess


logger = logging.getLogger('color_reference')


class ColorReference:
    def __init__(self):
        self.processor = None

    def __start_processor(self):
        self.processor = ProcessMaintainer(target=postprocess, kwargs={
        }, daemon=True, revive_interval=10)
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
