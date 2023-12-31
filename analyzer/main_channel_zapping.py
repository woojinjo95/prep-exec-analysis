# FIXME 에 해당하는 부분을 수정

import logging
from typing import Dict

from scripts.config.constant import RedisChannel, RedisDB
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe, publish_msg
from scripts.format import Command
from scripts.log_service.log_organizer import LogOrganizer
from scripts.modules.channel_zapping import ChannelZapping

logger = logging.getLogger('main')

service_name = 'channel_zapping'  # FIXME: service name
command_name = Command.CHANNEL_ZAPPING.value  # FIXME: command name


class CommandExecutor:
    def __init__(self):
        self.service_module = ChannelZapping()  # FIXME: module

    def start_service_module(self):
        self.service_module.start()

    def stop_service_module(self):
        self.service_module.stop()

    def execute(self, command: Dict):
        if command.get('msg') == 'analysis':
            data = command.get('data', {})
            measurement = data.get('measurement', [])
            if command_name in measurement:
                self.start_service_module()
                publish_msg({'measurement': command_name}, 'analysis_started')

        elif command.get('msg') == 'service_state':
            data = command.get('data', {})
            state = data.get('state', '')
            if state == 'streaming':
                self.stop_service_module()
                publish_msg({'measurement': command_name}, 'analysis_terminate')


def main():
    command_executor = CommandExecutor()
    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            command_executor.execute(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name=service_name)
        log_organizer.set_stream_logger('main', color_index=6)
        logger.info(f'Start {service_name} container')
        
        main()

    finally:
        logger.info(f'Close {service_name} container')
        log_organizer.close()

