import logging

from analysis_manager import AnalysisManager
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB
from scripts.config.config import get_setting_with_env
from scripts.log_service.log_organizer import LogOrganizer
from scripts.


logger = logging.getLogger('main')


freeze_manager = None


def start_logcat_manager(connection_info: dict):
    global freeze_manager

    if freeze_manager is not None:
        logger.warning('LogcatManager is already alive')
    else:
        freeze_manager = LogcatManager(connection_info=connection_info)
        freeze_manager.start()
        logger.info('Start LogcatManager')


def stop_logcat_manager():
    global freeze_manager

    if freeze_manager is not None:
        freeze_manager.stop()
        freeze_manager = None
        logger.info('Stop LogcatManager')
    else:
        logger.warning('LogcatManager is not alive')


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
    analysis_manager = AnalysisManager(mode=get_setting_with_env('ANALYSIS_EXEC_MODE', 'async'))

    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            analysis_manager.register(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='analyzer')
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('connection')
        logger.info('Start analyzer container')
        
        main()

    finally:
        logger.info('Close analyzer container')
        log_organizer.close()
