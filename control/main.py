import logging
import time
from multiprocessing import Event

from scripts.configs.config import get_value, set_value
from scripts.configs.constant import RedisChannel
from scripts.configs.default import init_configs
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection)
from scripts.log_organizer import LogOrganizer
from scripts.utils._exceptions import handle_errors

logger = logging.getLogger('main')


def init():
    set_value('state', 'streaming', 'idle')
    time.sleep(1)


def command_parser(command: dict, streaming_stop_event: Event):
    pass


@handle_errors
def main():
    streaming_stop_event = Event()
    init()
    with get_strict_redis_connection() as src:
        for command in Subscribe(src, RedisChannel.command):
            command_parser(command, streaming_stop_event)


if __name__ == '__main__':
    try:
        init_configs()
        log_organizer = LogOrganizer()
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('serial')
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start control container')

        main()

    finally:
        logger.info('Close control container')
        log_organizer.close()
