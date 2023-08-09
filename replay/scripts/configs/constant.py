import os

if os.name == 'nt':
    _platform = 'windows'
else:
    if os.uname().sysname == 'Darwin':
        _platform = 'mac'
    else:
        _platform = 'linux'


class RemoconSetting:
    max_qsize = 100
    default_remocon_id = 1


class SerialRemoconSetting(RemoconSetting):
    key_interval = 0.1


class BTRemoconSetting(RemoconSetting):
    key_interval = 0.1


class RedisDBEnum:
    hardware: int = 0
    media: int = 3


class RedisChannel:
    command = 'command'
    loudness = 'loudness'


class ServiceType:
    rcu = 'remocon'
    config = 'on_off_control'
    shell = 'network'
