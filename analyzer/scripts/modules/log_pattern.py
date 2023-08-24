import logging

from .template import Module
from scripts.processor.log_pattern import match_log_pattern


logger = logging.getLogger('log_pattern')


class LogPattern(Module):
    def __init__(self):
        super().__init__(func=match_log_pattern)
