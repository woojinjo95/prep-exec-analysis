import logging

from .template import Module
from scripts.processor.log_level import parse_log_level


logger = logging.getLogger('log_level')


class LogLevel(Module):
    def __init__(self):
        super().__init__(func=parse_log_level)
