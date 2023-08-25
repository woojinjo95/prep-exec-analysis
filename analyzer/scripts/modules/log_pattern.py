import logging

from .template import Module
from scripts.processor.log_pattern import match_log_pattern
from scripts.format import LogName

logger = logging.getLogger(LogName.LOG_PATTERN.value)


class LogPattern(Module):
    def __init__(self):
        super().__init__(func=match_log_pattern)
