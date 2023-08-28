import logging
from typing import Dict

from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB
from scripts.log_service.log_organizer import LogOrganizer
from scripts.monkey.monkey_manager import MonkeyManager


logger = logging.getLogger('main')


monkey_manager = None


def start_monkey_manager():
    global monkey_manager

    if monkey_manager is not None:
        logger.warning('MonkeyManager is already alive')
    else:
        monkey_manager = MonkeyManager()
        monkey_manager.start()
        logger.info('Start MonkeyManager')


def stop_monkey_manager():
    global monkey_manager

    if monkey_manager is not None:
        monkey_manager.stop()
        monkey_manager = None
        logger.info('Stop MonkeyManager')
    else:
        logger.warning('MonkeyManager is not alive')



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
            start_monkey_manager()
        elif control == 'stop':
            stop_monkey_manager()
        else:
            logger.warning(f'Unknown control: {control}')


def main():
    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            execute(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='monkey')
        # DO NOT naming conflict with organizer's logger name.
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('monkey_test')
        logger.info('Start monkey container')
        
        main()

    finally:
        logger.info('Close monkey container')
        log_organizer.close()
