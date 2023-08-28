import logging

from .template import Module
from scripts.processor.log_pattern import test_log_pattern_matching
from scripts.format import LogName

logger = logging.getLogger(LogName.LOG_PATTERN.value)


class LogPattern(Module):
    def __init__(self):
        super().__init__(func=test_log_pattern_matching)
