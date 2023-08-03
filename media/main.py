import logging
import time
from multiprocessing import Event

from scripts.configs.config import get_value, set_value
from scripts.configs.constant import RedisChannel
from scripts.configs.default import init_configs
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection)
from scripts.log_organizer import LogOrganizer
from scripts.media_process.capture import streaming
from scripts.media_process.loudness import test_audio_redis_update
from scripts.media_process.rotation import MakeVideo
from scripts.utils._exceptions import handle_errors

logger = logging.getLogger('main')


def init():
    set_value('state', 'streaming', 'idle')
    time.sleep(1)


def command_parser(command: dict, streaming_stop_event: Event):
    ''' 
    PUBLISH command '{"streaming": "start"}'
    PUBLISH command '{"streaming": "stop"}'
    PUBLISH command '{"streaming": "restart"}
    PUBLISH command '{"recording": {"interval": 20}}'
    PUBLISH command '{"recording": {"start_time": 1691046399.10611, "end_time":  1691046399.10611}}'

    '''

    if command.get('streaming'):
        streaming_arg = command.get('streaming')
        if streaming_arg == 'start':
            if get_value('state', 'streaming') == 'idle':
                streaming_stop_event.clear()
                streaming(streaming_stop_event)
            else:
                logger.warning('Already Streaming Service Started')

        elif streaming_arg == 'stop':
            if get_value('state', 'streaming') == 'idle':
                logger.warning('Already Streaming Service stopped')
            else:
                streaming_stop_event.set()
                time.sleep(2)

        elif streaming_arg == 'restart':
            streaming_stop_event.set()
            time.sleep(2)
            streaming_stop_event.clear()
            streaming(streaming_stop_event)
        else:
            logger.warning(f'Unknown streaming args: {streaming_arg}')

    if command.get('recording'):
        interval = command.get('record', {}).get('interval', 30)
        start_time = command.get('record', {}).get('start_time', None)
        end_time = command.get('record', {}).get('end_time', None)
        new_video = MakeVideo(start_time, end_time, interval)
        new_video.run()


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
        log_organizer.set_stream_logger('video')
        log_organizer.set_stream_logger('audio')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('file', 5)
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start media container')

        main()

    finally:
        logger.info('Close media container')
        log_organizer.close()
