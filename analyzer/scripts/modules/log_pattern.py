from .template import Module
from scripts.processor.log_pattern import test_log_pattern_matching


class LogPattern(Module):
    def __init__(self):
        super().__init__(func=test_log_pattern_matching)
        