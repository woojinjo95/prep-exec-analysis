import logging

from .template import Module
from scripts.processor.warm_boot import test_warm_boot


logger = logging.getLogger('boot_test')


class WarmBoot(Module):
    def __init__(self):
        super().__init__(func=test_warm_boot)
