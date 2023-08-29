import logging

from analysis_manager import AnalysisManager
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB
from scripts.config.config import get_setting_with_env
from scripts.log_service.log_organizer import LogOrganizer
from scripts.format import LogName


logger = logging.getLogger('main')


def main():
    analysis_manager = AnalysisManager(mode=get_setting_with_env('ANALYSIS_EXEC_MODE', 'sync'))

    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            analysis_manager.register(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='analyzer')
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger(LogName.COLOR_REFERENCE.value)
        log_organizer.set_stream_logger(LogName.FREEZE_DETECT.value)
        log_organizer.set_stream_logger(LogName.BOOT_TEST.value)
        log_organizer.set_stream_logger(LogName.LOG_PATTERN.value)
        logger.info('Start analyzer container')
        
        main()

    finally:
        logger.info('Close analyzer container')
        log_organizer.close()
