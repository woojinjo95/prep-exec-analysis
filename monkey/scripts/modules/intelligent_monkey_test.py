from .template import Module
from scripts.processor.intelligent_monkey_test import test_intelligent_monkey


class IntelligentMonkeyTestModule(Module):
    def __init__(self):
        super().__init__(func=test_intelligent_monkey)
        