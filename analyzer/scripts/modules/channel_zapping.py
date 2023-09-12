from .template import Module
from scripts.processor.channel_zapping import test_channel_zapping


class ChannelZapping(Module):
    def __init__(self):
        super().__init__(func=test_channel_zapping)
        