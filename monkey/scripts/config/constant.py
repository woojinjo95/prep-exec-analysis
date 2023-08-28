from dataclasses import dataclass


@dataclass
class RedisDB:
    hardware: int = 0
    monkey: int = 6
    
@dataclass
class RedisChannel:
    command = 'command'

