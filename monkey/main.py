import logging
from typing import Dict

from scripts.connection.redis_conn import get_strict_redis_connection, set_value, delete
from scripts.connection.redis_pubsub import Subscribe, publish_msg
from scripts.config.constant import RedisChannel, RedisDB
from scripts.log_service.log_organizer import LogOrganizer
from scripts.modules.monkey_test import MonkeyTestModule


logger = logging.getLogger('main')


class CommandExecutor:
    def __init__(self):
        self.mt_module = MonkeyTestModule()

    def start_mt_module(self):
        self.mt_module.start()

    def stop_mt_module(self):
        self.mt_module.stop()

    # sub의 data로 오면 파싱해서 monkey test db에 별도로 기록
    def set_arguments(self, data: Dict):
        hash_name = 'monkey_test_arguments'
        delete(hash_name)
        
        for key, value in data.items():
            set_value(hash_name, key, value)

    def execute(self, command: Dict):
        ''' 
        - 인텔리전트 몽키 테스트 실행 (ROKU)
            PUBLISH command '{"msg": "monkey", "data": {"type": "intelligent_monkey_test", "profile": "roku", "duration_per_menu": 10, "interval": 1300, "enable_smart_sense": true, "waiting_time": 3}}'
        - 인텔리전트 몽키 테스트 실행 (SKB)
            PUBLISH command '{"msg": "monkey", "data": {"type": "intelligent_monkey_test", "profile": "skb", "duration_per_menu": 10, "interval": 1300, "enable_smart_sense": true, "waiting_time": 3}}'
        - 몽키 테스트 실행 (ROKU)
            PUBLISH command '{"msg": "monkey", "data": {"type": "monkey_test", "duration": 60, "interval": 1300, "enable_smart_sense": true, "waiting_time": 3, "remocon_name": "roku", "remote_control_type": "ir"}}'
        - 몽키 테스트 실행 (SKB)
            PUBLISH command '{"msg": "monkey", "data": {"type": "monkey_test", "duration": 60, "interval": 1300, "enable_smart_sense": true, "waiting_time": 3, "remocon_name": "skb", "remote_control_type": "ir"}}'
        - 몽키테스트 종료
            PUBLISH command '{"msg": "monkey_terminate"}'
        
        '''
        msg = command.get('msg', '')

        if msg in ['monkey_test', 'intelligent_monkey_test']:
            data = command.get('data', {})
            self.set_arguments(data)
            self.start_mt_module()
            publish_msg({}, 'monkey_started')

        elif msg == 'monkey_terminate':
            self.stop_mt_module()


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
        log_organizer.set_stream_logger('monkey_agent')
        logger.info('Start monkey container')
        
        main()

    finally:
        logger.info('Close monkey container')
        log_organizer.close()
