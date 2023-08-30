import logging
from typing import Dict

from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB
from scripts.log_service.log_organizer import LogOrganizer
from scripts.modules.intelligent_monkey_test import IntelligentMonkeyTestModule


logger = logging.getLogger('main')


class CommandExecutor:
    def __init__(self):
        self.imt_module = IntelligentMonkeyTestModule()

    def start_imt_module(self):
        self.imt_module.start()

    def stop_imt_module(self):
        self.imt_module.stop()

    def execute(self, command: Dict):
        ''' 
        start: PUBLISH command '{"msg": "monkey", "data": {"analysis_type": "intelligent_monkey_test"}}'
        '''
        if command.get('msg', '') == 'monkey':
            data = command.get('data', {})
            analysis_type = data.get('analysis_type', '')
            if analysis_type == 'intelligent_monkey_test':
                self.start_imt_module()


def main():
    command_executor = CommandExecutor()
    with get_strict_redis_connection(RedisDB.hardware) as src:
        for command in Subscribe(src, RedisChannel.command):
            command_executor.execute(command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer(name='monkey')
        # DO NOT naming conflict with organizer's logger name.
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('monkey_test')
        logger.info('Start monkey container')
        
        main()

    finally:
        logger.info('Close monkey container')
        log_organizer.close()
