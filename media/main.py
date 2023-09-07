import logging
import time
from multiprocessing import Event
from operator import attrgetter

from scripts.configs.config import get_value, set_value
from scripts.configs.constant import RedisChannel
from scripts.configs.default import init_configs
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection,
                                             publish)
from scripts.log_organizer import LogOrganizer
from scripts.media_process.capture import refresh_capture_board, streaming
from scripts.media_process.loudness import update_loudness_to_mongodb
from scripts.media_process.rotation import MakeVideo
from scripts.media_process.utils import kill_active_capture_process
from scripts.media_process.video_snapshot import save_video_frame_snapshot
from scripts.utils._exceptions import handle_errors

logger = logging.getLogger('main')


def init():
    set_value('state', 'streaming', 'idle')
    time.sleep(1)


def command_parser(command: dict, streaming_stop_event: Event):
    ''' 
    publish command '{"msg": "streaming", "data": {"action": "start"}}'
    publish command '{"msg": "recording", "data": {"interval": 1800}}'
    '''

    if command.get('msg') == 'streaming':
        streaming_arg = command.get('data', {})
        action = streaming_arg.get('action', 'stop')

        log_level = 'info'
        state = 'idle'
        log = ''

        if action == 'start':
            state = 'streaming'
            if get_value('state', 'streaming') == 'idle':
                streaming_stop_event.clear()
                streaming(streaming_stop_event)
                log = 'Start streaming service'
                time.sleep(1)   # prevent multiple process by waiting state update time
            else:
                log_level = 'warning'
                log = 'Already streaming service Started'

        elif action == 'stop':
            state = 'idle'
            if get_value('state', 'streaming') == 'idle':
                log_level = 'warning'
                log = 'Already streaming service stopped'
            else:
                streaming_stop_event.set()
                log = 'Stop streaming service'
                # kill_active_capture_process(signal=2)
                # time.sleep(10)

        elif action == 'restart':
            log = 'Restart streaming service'
            streaming_stop_event.set()
            time.sleep(2)
            kill_active_capture_process()
            time.sleep(1)
            streaming_stop_event.clear()
            streaming(streaming_stop_event)
        else:
            log_level = 'warning'
            log = f'Unknown streaming action args: {streaming_arg}'

        attrgetter(log_level)(logger)(log)
        with get_strict_redis_connection() as redis_connection:
            publish(redis_connection, RedisChannel.command, {'msg': 'streaming_response',
                                                             'level': log_level,
                                                             'data': {'log': log, 'state': state}})

    if command.get('msg') == 'recording':
        recording_args = command.get('data')
        interval = recording_args.get('interval', 30)
        start_time = recording_args.get('start_time', None)
        end_time = recording_args.get('end_time', None)
        new_video = MakeVideo(start_time, end_time, interval)
        new_video.run()

    if command.get('msg') == 'capture_board':
        capture_board_args = command.get('data')
        if capture_board_args.get('action') == 'refresh':
            refresh_capture_board()

    if command.get('msg') == 'video_frame_snapshot':
        video_snapshot_args = command.get('data')
        save_video_frame_snapshot(**video_snapshot_args)


@handle_errors
def main():
    global_stop_event = Event()
    streaming_stop_event = Event()
    init()
    update_loudness_to_mongodb(global_stop_event)
    with get_strict_redis_connection() as src:
        for command in Subscribe(src, RedisChannel.command):
            command_parser(command, streaming_stop_event)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='media')
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('video')
        log_organizer.set_stream_logger('audio')
        log_organizer.set_stream_logger('snapshot')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('mongodb')
        log_organizer.set_stream_logger('file', 5)
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start media container')

        init_configs()
        main()

    finally:
        logger.info('Close media container')
        log_organizer.close()
