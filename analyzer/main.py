import logging

from scripts.modules.color_reference import ColorReference
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB
from scripts.log_service.log_organizer import LogOrganizer


logger = logging.getLogger('main')



# TODO: module의 시작, 종료를 is_alive 기준으로 필요
def start_logcat_manager():
    global logcat_manager

    if logcat_manager is not None:
        logger.warning('LogcatManager is already alive')
    else:
        logcat_manager = ColorReference()
        logcat_manager.start()
        logger.info('Start LogcatManager')


def stop_logcat_manager():
    global logcat_manager

    if logcat_manager is not None:
        logcat_manager.stop()
        logcat_manager = None
        logger.info('Stop LogcatManager')
    else:
        logger.warning('LogcatManager is not alive')


# TODO: 포맷 정의 필요
def command_parser(command: dict):
    ''' 
    '''

    if command.get('msg') == 'stb_log':
        arg = command.get('data', {})
        logger.info(f'msg: stb_log. arg: {arg}')

        control = arg.get('control', '')
        if control == 'start':
            start_logcat_manager()
        elif control == 'stop':
            stop_logcat_manager()
        else:
            logger.warning(f'Unknown control: {control}')


def main():
    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            command_parser(command)


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
