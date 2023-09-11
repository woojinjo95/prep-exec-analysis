from .template import Module
from scripts.processor.macroblock import test_macroblock


class Macroblock(Module):
    def __init__(self):
        super().__init__(func=test_macroblock)
        