from dataclasses import dataclass


@dataclass
class RedisDB:
    hardware: int = 0
    stb_log: int = 4
    
    