import logging
from typing import Dict

from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB
from scripts.log_service.log_organizer import LogOrganizer
from .monkey import start_monkey, stop_monkey


logger = logging.getLogger('main')


def execute(command: Dict):
    ''' 
    start: PUBLISH command '{"msg": "monkey", "data": {"control": "start"}}'
    stop: PUBLISH command '{"msg": "monkey", "data": {"control": "stop"}}'
    '''
    if command.get('msg', '') == 'monkey':
        arg = command.get('data', {})
        logger.info(f'msg: monkey. arg: {arg}')

        control = arg.get('control', '')
        if control == 'start':
            start_monkey()
        elif control == 'stop':
            stop_monkey()
        else:
            logger.warning(f'Unknown control: {control}')


def main():
    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            execute(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='monkey')
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('monkey')
        logger.info('Start monkey container')
        
        main()

    finally:
        logger.info('Close monkey container')
        log_organizer.close()
