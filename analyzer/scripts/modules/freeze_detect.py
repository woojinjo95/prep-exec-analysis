import logging

from .template import Module
from scripts.processor.freeze_detect import test_freeze_detection
from scripts.format import LogName

logger = logging.getLogger(LogName.FREEZE_DETECT.value)


class FreezeDetect(Module):
    def __init__(self):
        super().__init__(func=test_freeze_detection)
