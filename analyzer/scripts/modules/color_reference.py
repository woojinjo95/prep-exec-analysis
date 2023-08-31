from .template import Module
from scripts.processor.color_reference import test_color_reference


class ColorReference(Module):
    def __init__(self):
        super().__init__(func=test_color_reference)
        