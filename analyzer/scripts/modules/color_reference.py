import logging

from .template import Module
from scripts.processor.color_reference import process


logger = logging.getLogger('color_reference')


class ColorReference(Module):
    def __init__(self):
        super().__init__(func=process)
