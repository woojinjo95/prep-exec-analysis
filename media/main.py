import logging
import time
from multiprocessing import Event, Manager, Process, Queue
from multiprocessing.managers import DictProxy

from scripts.configs.default import init_configs
from scripts.configs.redis_connection import hget_single, hset_single
from scripts.log_organizer import LogOrganizer
from scripts.media_process.capture import test, start_capture, audio_value_consumer
from scripts.media_process.rotation import MakeVideo

from scripts.utils._exceptions import handle_errors

logger = logging.getLogger('main')


def streaming() -> Event:
    with Manager() as manager:
        configs = manager.dict()
        audio_values = Queue()
        stop_event = Event()
        capture_process = Process(target=start_capture, args=(configs, audio_values, stop_event), daemon=True)
        consumer_process = Process(target=audio_value_consumer, args=(audio_values, stop_event), daemon=True)

        capture_process.start()
        consumer_process.start()

        return stop_event


@handle_errors
def main():
    time.sleep(1)

    is_streaming = False
    while True:
        if hget_single('test', 'mode') == 'streaming_start':
            hset_single('test', 'mode', 'streaming')
            is_streaming = True
            stop_event = streaming()
        elif is_streaming and hget_single('test', 'mode', 'idle'):
            stop_event.set()
            time.sleep(5)
        else:
            pass

        if hget_single('test', 'capture') == 'yes':
            hset_single('test', 'capture', 'no')
            duration = hget_single('test', 'interval', 30)

            new_video = MakeVideo(duration=duration)
            new_video.run()
            logger.info(f'New video! : {new_video}')

        time.sleep(5)


if __name__ == '__main__':
    try:
        init_configs()
        log_organizer = LogOrganizer()
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('video')
        log_organizer.set_stream_logger('audio')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start media container')

        main()

    finally:
        logger.info('Close media container')
        log_organizer.close()
