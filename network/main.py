import logging
import time

from scripts.configs.config import RedisDBEnum, get_value
from scripts.configs.constant import RedisChannel, RemoconSetting
from scripts.configs.default import init_configs
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection)

from scripts.log_organizer import LogOrganizer
from scripts.utils._exceptions import handle_errors

logger = logging.getLogger('main')


@handle_errors
def init():
    pass


@handle_errors
def command_parser(command: dict):
    if command.get('network'):
        logger.info("I'm alive!")


@handle_errors
def main():
    init()

    with get_strict_redis_connection() as src:
        for command in Subscribe(src, RedisChannel.command):
            command_parser(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer()
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('packet')
        log_organizer.set_stream_logger('file')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start network container')

        init_configs()
        main()

    finally:
        logger.info('Close network container')
        log_organizer.close()
