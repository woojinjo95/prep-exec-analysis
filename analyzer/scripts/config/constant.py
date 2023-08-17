from dataclasses import dataclass


@dataclass
class RedisDB:
    hardware: int = 0
    analyzer: int = 5
    
@dataclass
class RedisChannel:
    command = 'command'

