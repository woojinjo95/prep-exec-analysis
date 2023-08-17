import logging

from .template import Module
from scripts.processor.freeze_detect import detect_freeze


logger = logging.getLogger('freeze_detect')


class FreezeDetect(Module):
    def __init__(self):
        super().__init__(func=detect_freeze)
