import logging

from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB
from scripts.log_service.log_organizer import LogOrganizer
from command import CommandExecutor


logger = logging.getLogger('main')


def main():
    cmd_exec = CommandExecutor()

    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            cmd_exec.execute(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='analyzer')
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('color_reference')
        logger.info('Start analyzer container')
        
        main()

    finally:
        logger.info('Close analyzer container')
        log_organizer.close()
