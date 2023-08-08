import logging

from scripts.configs.constant import RedisChannel
from scripts.connection.mongo_db.crud import load_one_from_mongodb
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection,
                                             publish)
from scripts.log_organizer import LogOrganizer
from scripts.utils._exceptions import handle_errors

logger = logging.getLogger('main')


@handle_errors
def init():
    pass


@handle_errors
def command_parser(command: dict):
    args = command.get('replay', None)
    if args == 'run':
        logger.info('run!!!!!!!')

        scenario = load_one_from_mongodb(col='scenario')
        block_list = [
            block
            for item in scenario.get('block_group', [])
            for _ in range(item['repeat_cnt'])
            for block in item['block']
        ]

        for i, block in enumerate(block_list):
            # logger.info(block)
            # TODO 타입에 맞게 publish
            with get_strict_redis_connection() as src:
                publish(src, 'command', {"network": "start"})
            # TODO 정상 동작 응답이 오면 다음 블럭 실행

    elif args == 'stop':
        logger.info('stop!!!!!!!')



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
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start replay container')

        main()

    finally:
        logger.info('Close replay container')
        log_organizer.close()
