import logging

from .template import Module
from scripts.processor.cold_boot import test_cold_boot


logger = logging.getLogger('boot_test')


class ColdBoot(Module):
    def __init__(self):
        super().__init__(func=test_cold_boot)
