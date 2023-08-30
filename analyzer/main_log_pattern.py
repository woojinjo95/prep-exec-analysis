# FIXME 에 해당하는 부분을 수정

import logging
from typing import Dict

from scripts.config.constant import RedisChannel, RedisDB
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe, publish_msg
from scripts.format import Command
from scripts.log_service.log_organizer import LogOrganizer
from scripts.modules.log_pattern import LogPattern

logger = logging.getLogger('main')

service_name = 'log_pattern'  # FIXME: service name


class CommandExecutor:
    def __init__(self):
        self.service_module = LogPattern()  # FIXME: module

    def start_service_module(self):
        self.service_module.start()

    def stop_service_module(self):
        self.service_module.stop()

    def execute(self, command: Dict):
        if command.get('msg') == 'analysis':
            data = command.get('data', {})

            measurement = data.get('measurement', [])
            if Command.LOG_PATTERN_MATCHING.value in measurement:  # FIXME: measurement command name
                self.start_service_module()
                publish_msg({'measurement': [Command.LOG_PATTERN_MATCHING.value]}, 'analysis_started')


def main():
    command_executor = CommandExecutor()
    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            command_executor.execute(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name=service_name)
        log_organizer.set_stream_logger('main', color_index=3)
        logger.info(f'Start {service_name} container')
        
        main()

    finally:
        logger.info(f'Close {service_name} container')
        log_organizer.close()

