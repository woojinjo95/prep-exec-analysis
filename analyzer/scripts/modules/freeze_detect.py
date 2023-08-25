import logging

from .template import Module
from scripts.processor.freeze_detect import detect_freeze
from scripts.format import LogName

logger = logging.getLogger(LogName.FREEZE_DETECT.value)


class FreezeDetect(Module):
    def __init__(self):
        super().__init__(func=detect_freeze)
