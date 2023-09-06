from .template import Module
from scripts.processor.monkey_test import test_monkey


class MonkeyTestModule(Module):
    def __init__(self):
        super().__init__(func=test_monkey)
        