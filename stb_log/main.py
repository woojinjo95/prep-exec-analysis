import logging
import time

from scripts.config.constant import RedisChannel, RedisDB
from scripts.connection.external import (get_connection_info,
                                         set_connection_info)
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.log_service.connection_checker import connection_checker
from scripts.log_service.dumpsys.manager import DumpsysManager
from scripts.log_service.log_organizer import LogOrganizer
from scripts.log_service.logcat.log_manager import LogcatManager
from scripts.util.process_maintainer import ProcessMaintainer

logger = logging.getLogger('main')


logcat_manager = None
dumpsys_manager = None


def start_logcat_manager(connection_info: dict):
    global logcat_manager

    if logcat_manager is not None:
        logger.warning('LogcatManager is already alive')
    else:
        logcat_manager = LogcatManager(connection_info=connection_info)
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


def start_dumpsys_manager(connection_info: dict):
    global dumpsys_manager

    if dumpsys_manager is not None:
        logger.warning('DumpsysManager is already alive')
    else:
        dumpsys_manager = DumpsysManager(connection_info=connection_info)
        dumpsys_manager.start()
        logger.info('Start DumpsysManager')


def stop_dumpsys_manager():
    global dumpsys_manager

    if dumpsys_manager is not None:
        dumpsys_manager.stop()
        dumpsys_manager = None
        logger.info('Stop DumpsysManager')
    else:
        logger.warning('DumpsysManager is not alive')


def start():
    connection_info = get_connection_info()
    start_logcat_manager(connection_info)
    start_dumpsys_manager(connection_info)


def stop():
    stop_logcat_manager()
    stop_dumpsys_manager()
    time.sleep(0.1)


def command_parser(command: dict):
    ''' 
    start: PUBLISH command '{"msg": "stb_log", "data": {"control": "start"}}'
    stop: PUBLISH command '{"msg": "stb_log", "data": {"control": "stop"}}'
    connection info: PUBLISH command '{"msg": "config", "data": {"mode": "adb", "host": "192.168.30.30", "port": "5555", "username": "root", "password": ""}}'
    '''

    if command.get('msg') == 'stb_log':
        arg = command.get('data', {})
        logger.info(f'msg: stb_log. arg: {arg}')

        control = arg.get('control', '')
        if control == 'start':
            start()
        elif control == 'stop':
            stop()
        else:
            logger.warning(f'Unknown control: {control}')

    if command.get('msg') == 'config':
        data = command.get('data')
        data['connection_mode'] = data['mode']
        del data['mode']
        connection_info = data
        logger.info(f'connection_info: {connection_info}')
        set_connection_info(**connection_info)

        # restart
        stop()
        start()


def main():
    connection_checker_proc = ProcessMaintainer(target=connection_checker, 
                                                name='connection_checker',
                                                revive_interval=1)
    connection_checker_proc.start()

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
