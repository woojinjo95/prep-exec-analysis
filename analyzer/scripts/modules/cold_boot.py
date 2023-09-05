from .template import Module
from scripts.processor.cold_boot import test_cold_boot


class ColdBoot(Module):
    def __init__(self):
        super().__init__(func=test_cold_boot)
        