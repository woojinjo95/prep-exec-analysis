import logging
import time

from scripts.configs.default import init_configs
from scripts.configs.config import get_value, set_value
from scripts.log_organizer import LogOrganizer
from scripts.media_process.capture import streaming
from scripts.media_process.rotation import MakeVideo
from scripts.utils._exceptions import handle_errors
from scripts.media_process.loudness import test_audio_redis_update

logger = logging.getLogger('main')


@handle_errors
def main():
    time.sleep(1)

    is_streaming = False
    while True:
        if get_value('test', 'mode') == 'streaming_start':
            set_value('test', 'mode', 'streaming')
            is_streaming = True
            stop_event = streaming()
            test_audio_redis_update(stop_event)
        elif is_streaming and get_value('test', 'mode') == 'idle':
            stop_event.set()
            time.sleep(5)
        else:
            pass

        if get_value('test', 'capture') == 'yes':
            set_value('test', 'capture', 'no')
            interval = get_value('test', 'interval', 30)

            new_video = MakeVideo(interval=interval)
            new_video.run()

        time.sleep(5)


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
