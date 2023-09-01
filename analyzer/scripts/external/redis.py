import time

from scripts.config.constant import RedisDB
from scripts.connection.redis_conn import set_value
from scripts.util._timezone import get_utc_datetime


def set_last_analysis_info(command: str):
    set_value('last_analysis_info', 'analysis_name', command, db=RedisDB.hardware)
    set_value('last_analysis_info', 'end_time', get_utc_datetime(time.time()), db=RedisDB.hardware)
