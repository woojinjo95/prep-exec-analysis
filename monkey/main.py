import logging
from typing import Dict

from scripts.connection.redis_conn import get_strict_redis_connection, set_value
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB
from scripts.log_service.log_organizer import LogOrganizer
from scripts.modules.monkey_test import MonkeyTestModule
from scripts.connection.redis_pubsub import publish_msg


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
        arguments = data['arguments']
        analysis_type = arguments['type']
        set_value('monkey_test_arguments', 'analysis_type', analysis_type)
        for arg in arguments['args']:
            key = arg['key']
            value = arg['value']
            set_value('monkey_test_arguments', key, value)

    def execute(self, command: Dict):
        ''' 
        - 인텔리전트 몽키 테스트 실행 (ROKU)
            PUBLISH command '{"msg": "monkey", "data": {"arguments": {"type": "intelligent_monkey_test", "args": [{"key":"profile","value":"roku"},{"key":"duration_per_menu","value": 60},{"key":"interval","value":1000},{"key":"enable_smart_sense","value": true},{"key":"waiting_time","value":3}]}}}'
        - 몽키 테스트 실행
            PUBLISH command '{"msg": "monkey", "data": {"arguments": {"type": "monkey_test", "args": [{"key":"duration","value":60},{"key":"interval","value":1000},{"key":"enable_smart_sense","value":true},{"key":"waiting_time","value":3},{"key":"remocon_name","value":"roku"},{"key":"remote_control_type","value":"ir"}]}}}'
        - 몽키테스트 종료
            PUBLISH command '{"msg": "monkey_terminate"}'
        
        '''
        if command.get('msg', '') == 'monkey':
            data = command.get('data', {})
            self.set_arguments(data)
            self.start_mt_module()
            publish_msg({}, 'monkey_started')
            
        elif command.get('msg', '') == 'monkey_terminate':
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
