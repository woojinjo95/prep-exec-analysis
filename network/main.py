import logging
import time
from multiprocessing import Event
from operator import attrgetter

from scripts.configs.config import RedisDBEnum, get_value, set_value
from scripts.configs.constant import RedisChannel
from scripts.configs.default import init_configs
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection,
                                             publish)
from scripts.log_organizer import LogOrganizer
from scripts.packet_capture import real_time_packet_capture, stop_capture
from scripts.utils._exceptions import handle_errors
from scripts.epg.epg import get_epg_data_with_provider
from scripts.control.emulation_function import apply_network_emulation_args


logger = logging.getLogger('main')


@handle_errors
def init():
    set_value('state', 'packet_capture', 'idle')
    pass


@handle_errors
def command_parser(command: dict, packet_capture_stop_event: Event):
    ''' 
    publish command '{"msg": "packet_capture", "data": {"action": "start"}}'
    publish command '{"msg": "epg_update", "data": {"provider": "sk", "ip": "239.192.60.43", "port": 49200}}'
    publish command '{"msg": "network_emulation", "data": {"action": "start"}}'
    publish command '{"msg": "network_emulation", "data": {"args": {}}}'
    '''

    if command.get('msg') == 'packet_capture':
        packet_capture_args = command.get('data', {})
        action = packet_capture_args.get('action', 'stop')

        log_level = 'info'
        state = 'idle'
        log = ''

        if action == 'start':
            state = 'capturing'
            if get_value('state', 'packet_capture') == 'idle':
                set_value('state', 'packet_capture', 'capturing')
                packet_capture_stop_event.clear()
                real_time_packet_capture(packet_capture_stop_event)
                log = 'Start packet capture service'
            else:
                log_level = 'warning'
                log = 'Already packet capture service Started'

        elif action == 'stop':
            state = 'idle'
            if get_value('state', 'packet_capture') == 'idle':
                log_level = 'warning'
                log = 'Already packet capture service stopped'
            else:
                set_value('state', 'packet_capture', 'idle')
                stop_capture()
                packet_capture_stop_event.set()
                log = 'Stop packet capture service'
                time.sleep(2)
        else:
            log_level = 'warning'
            log = f'Unknown capturing action args: {packet_capture_args}'

        attrgetter(log_level)(logger)(log)
        with get_strict_redis_connection() as redis_connection:
            publish(redis_connection, RedisChannel.command, {'msg': 'packet_capture_response',
                                                             'level': log_level,
                                                             'data': {'log': log, 'state': state}})

    if command.get('msg') == 'epg_update':
        epg_args = command.get('data', {})
        provider = epg_args.get('provider', 'Unknown')
        ip = epg_args.get('ip')
        port = epg_args.get('port')
        logger.info()

        get_epg_data_with_provider(provider, ip, port)

    if command.get('msg') == 'network_emulation':
        network_emulation_args = command.get('data', {})
        apply_network_emulation_args(network_emulation_args)


@handle_errors
def main():
    packet_capture_stop_event = Event()
    init()
    with get_strict_redis_connection() as src:
        for command in Subscribe(src, RedisChannel.command):
            command_parser(command, packet_capture_stop_event)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='network')
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('capture')
        log_organizer.set_stream_logger('analysis')
        log_organizer.set_stream_logger('network_control')
        log_organizer.set_stream_logger('epg')
        log_organizer.set_stream_logger('file')
        log_organizer.set_stream_logger('shell')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start network container')

        init_configs()
        main()

    finally:
        logger.info('Close network container')
        log_organizer.close()
