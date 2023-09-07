from dataclasses import dataclass


@dataclass
class RedisDB:
    hardware: int = 0
    analyzer: int = 5
    
@dataclass
class RedisChannel:
    command = 'command'

CHANNEL_KEY_INPUT_CANDIDATES = ['channelup', 'channeldown', 
                                'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'ok']
