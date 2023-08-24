import logging

from .template import Module
from scripts.processor.cold_boot import test_cold_boot
from scripts.format import LogName

logger = logging.getLogger(LogName.BOOT_TEST.value)


class ColdBoot(Module):
    def __init__(self):
        super().__init__(func=test_cold_boot)
