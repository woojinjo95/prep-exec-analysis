import logging
from operator import attrgetter
from multiprocessing import Event

from scripts.configs.constant import RedisChannel
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection)

from scripts.log_organizer import LogOrganizer
from scripts.utils._exceptions import handle_errors
from scripts.utils._multi_process import ProcessMaintainer


logger = logging.getLogger('main')
error_logger = logging.getLogger('error')

log_level_values = {'debug': 0,
                    'info': 10,
                    'warning': 20,
                    'error': 30,
                    'critical': 40,
                    'fatal': 50}

@handle_errors
def commander_watcher(channel: str) -> ProcessMaintainer:
    logger = logging.getLogger(channel)
    def log_process(channel: str, stop_event: Event, run_state_event: Event):
        with get_strict_redis_connection() as src:
            for command in Subscribe(src, channel):
                try:
                    log_level = command.pop('level')
                    value = log_level_values[log_level]
                except KeyError:
                    log_level = 'info'
                    value = log_level_values[log_level]

                if value < log_level_values['error']:
                    attrgetter(log_level)(logger)(f'{command}')
                else:
                    attrgetter(log_level)(error_logger)(f'{command}')

    proc = ProcessMaintainer(func=log_process, args=(channel, ), daemon=True, revive_interval=1)
    proc.start()
    return proc


def main(log_organizer: LogOrganizer):
    channels = [RedisChannel.command, ]
    process_list = []

    for channel in channels:
        log_organizer.set_stream_logger(channel)
        proc = commander_watcher(channel)
        process_list.append(proc)


    while not proc.stop_event.is_set():
        for proc in process_list:
            proc.process.join()


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='watcher')
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start watcher container')

        main(log_organizer)

    finally:
        logger.info('Close watcher container')
        log_organizer.close()
