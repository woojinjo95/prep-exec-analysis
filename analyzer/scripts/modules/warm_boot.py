import logging

from .template import Module


logger = logging.getLogger('warm_boot')


class WarmBoot(Module):
    def __init__(self):
        super().__init__(func=test_warm_boot)
