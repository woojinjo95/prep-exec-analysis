import logging

from scripts.config.constant import RedisChannel, RedisDB
from scripts.connection.external import set_connection_info
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.log_service.connection_checker import connection_checker
from scripts.log_service.log_organizer import LogOrganizer
from scripts.util.process_maintainer import ProcessMaintainer
from manage import log_start, log_stop

logger = logging.getLogger('main')


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
            log_start()
        elif control == 'stop':
            log_stop()
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
        log_stop()
        log_start()


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
