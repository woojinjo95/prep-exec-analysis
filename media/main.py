import logging
import time

from scripts.utils._exceptions import handle_errors
from scripts.log_organizer import LogOrganizer

logger = logging.getLogger('main')


@handle_errors
def main():
    while True:
        logger.info(f'I\'m alive! {time.perf_counter()}')
        time.sleep(5)

if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer()
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('video')
        log_organizer.set_stream_logger('audio')
        log_organizer.set_stream_logger('connections')
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start media container')

        main()

    finally:
        logger.info('Close media container')
        log_organizer.close()
