from dataclasses import dataclass


@dataclass
class RedisDB:
    hardware: int = 0
    monkey: int = 6
    
@dataclass
class RedisChannel:
    command = 'command'


BASE_TESTRUN_RAW_DIR = "/app/workspace/testruns/{}/raw/monkey/section/images"

BANNED_IMAGE_DIR = '/app/static/banned_images'
