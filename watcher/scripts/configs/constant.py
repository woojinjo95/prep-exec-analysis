import os

if os.name == 'nt':
    _platform = 'windows'
else:
    if os.uname().sysname == 'Darwin':
        _platform = 'mac'
    else:
        _platform = 'linux'


class RedisDBEnum:
    hardware: int = 0
    media: int = 3


class RedisChannel:
    command = 'command'
    loudness = 'loudness'
