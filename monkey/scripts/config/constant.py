from dataclasses import dataclass


@dataclass
class RedisDB:
    hardware: int = 0
    monkey: int = 6
    
@dataclass
class RedisChannel:
    command = 'command'


BASE_TESTRUN_RAW_DIR = "/app/workspace/testruns/{}/raw/monkey/section/images"
BASE_DEV_TEST_RAW_DIR = "/app/workspace/testruns/{}/raw/monkey/test/images"
BANNED_IMAGE_DIR = '/app/static/banned_images'
SKIPPED_IMAGE_DIR = '/app/static/skipped_images'
