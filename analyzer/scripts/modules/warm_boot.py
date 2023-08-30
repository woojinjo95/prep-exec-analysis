from .template import Module
from scripts.processor.warm_boot import test_warm_boot


class WarmBoot(Module):
    def __init__(self):
        super().__init__(func=test_warm_boot)
        