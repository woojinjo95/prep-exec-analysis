import logging

from .template import Module
from scripts.processor.color_reference import process
from scripts.format import LogName


logger = logging.getLogger(LogName.COLOR_REFERENCE.value)


class ColorReference(Module):
    def __init__(self):
        super().__init__(func=process)
