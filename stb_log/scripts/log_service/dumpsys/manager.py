from multiprocessing import Event
import logging

from .postprocess import postprocess
from scripts.util.process_maintainer import ProcessMaintainer


logger = logging.getLogger('dumpsys')

class DumpsysManager:
    def __init__(self):
        self.postprocessor = None

    def __start_postprocessor(self):
        self.postprocessor = ProcessMaintainer(
            name='dumpsys_postprocessor', 
            target=postprocess,
            daemon=True, 
            revive_interval=10
        )
        self.postprocessor.start()

    def start(self):
        self.__start_postprocessor()
        logger.info('DumpsysManager start')

    def stop(self):
        if self.postprocessor:
            self.postprocessor.terminate()
        else:
            logger.warning('Postprocessor is not alive')
        logger.info('DumpsysManager stop')

    def is_alive(self) -> bool:
        return self.postprocessor.is_alive() if self.postprocessor else False
