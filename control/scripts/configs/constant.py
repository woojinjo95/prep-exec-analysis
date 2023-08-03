import os

if os.name == 'nt':
    _platform = 'windows'
else:
    if os.uname().sysname == 'Darwin':
        _platform = 'mac'
    else:
        _platform = 'linux'


class VideoFormat:
    extension = 'mp4'
    encoding = 'avc1' if _platform == 'windows' else 'mp4v'
    default_max_frame = 216000  # 60 fps for 1 hour
    background_max_frame = 10800  # 60 fps for 3 minutes
    default_max_time = 7200


class AudioDevice:
    gain = 67 if _platform == 'nt' else 90
    silence = -90


class RedisDBEnum:
    hardware: int = 0
    media: int = 3


class RedisChannel:
    command = 'command'
    loudness = 'loudness'
