from dataclasses import dataclass


@dataclass
class RedisDB:
    hardware: int = 0
    analyzer: int = 5
    
@dataclass
class RedisChannel:
    command = 'command'

CHANNEL_KEY_ADJOINT_CANDIDATES = ['channelup', 'channeldown']
CHANNEL_KEY_NON_ADJOINT_CANDIDATES = ['num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'ok']
