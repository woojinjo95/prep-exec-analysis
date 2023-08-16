import logging

from scripts.log_service.logcat.log_manager import LogcatManager
from scripts.log_service.dumpsys.manager import DumpsysManager
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB
from scripts.log_service.log_organizer import LogOrganizer


logger = logging.getLogger('main')


logcat_manager = None
dumpsys_manager = None
connection_info = {}


def start_logcat_manager(connection_info: dict):
    global logcat_manager

    if logcat_manager and logcat_manager.is_alive():
        logger.warning('LogcatManager is already alive')
    else:
        logcat_manager = LogcatManager(connection_info=connection_info)
        logcat_manager.start()
        logger.info('Start LogcatManager')


def stop_logcat_manager():
    global logcat_manager

    if logcat_manager and logcat_manager.is_alive():
        logcat_manager.stop()
        logger.info('Stop LogcatManager')
    else:
        logger.warning('LogcatManager is not alive')


def start_dumpsys_manager(connection_info: dict):
    global dumpsys_manager

    if dumpsys_manager and dumpsys_manager.is_alive():
        logger.warning('DumpsysManager is already alive')
    else:
        dumpsys_manager = DumpsysManager(connection_info=connection_info)
        dumpsys_manager.start()
        logger.info('Start DumpsysManager')


def stop_dumpsys_manager():
    global dumpsys_manager

    if dumpsys_manager and dumpsys_manager.is_alive():
        dumpsys_manager.stop()
        logger.info('Stop DumpsysManager')
    else:
        logger.warning('DumpsysManager is not alive')


def command_parser(command: dict):
    ''' 
    start: PUBLISH command '{"streaming": "start"}'
    stop: PUBLISH command '{"streaming": "stop"}'
    connection info: PUBLISH command '{"msg": "config", "data": {"mode": "adb", "host": "192.168.30.30", "port": "5555", "username": "root", "password": ""}}'
    '''
    global connection_info

    if command.get('streaming'):
        streaming_arg = command.get('streaming')
        logger.info(f'command_parser: {streaming_arg}')

        if streaming_arg == 'start':
            start_logcat_manager(connection_info)
            start_dumpsys_manager(connection_info)
        elif streaming_arg == 'stop':
            stop_logcat_manager()
            stop_dumpsys_manager()
        else:
            logger.warning(f'Unknown streaming args: {streaming_arg}')

    if command.get('msg'):
        if command.get('msg') == 'config':
            data = command.get('data')
            data['connection_mode'] = data['mode']
            del data['mode']
            connection_info = data
            logger.info(f'connection_info: {connection_info}')


def main():
    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            command_parser(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='stb_log')
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('collector')
        log_organizer.set_stream_logger('logcat')
        log_organizer.set_stream_logger('dumpsys')
        logger.info('Start stb_log container')

        main()

    finally:
        logger.info('Close stb_log container')
        log_organizer.close()
