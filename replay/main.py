import logging
import time

from scripts.configs.constant import RedisChannel
from scripts.connection.mongo_db.crud import load_by_id_from_mongodb
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection,
                                             publish)
from scripts.log_organizer import LogOrganizer
from scripts.utils._exceptions import handle_errors

logger = logging.getLogger('main')


class BlockManager:
    def __init__(self):
        self.block_list = []
        self.progress_index = 0

    def init_scenario(self, id=str):
        scenario = load_by_id_from_mongodb(col='scenario', id=id)
        if scenario:
            self.block_list = [
                block
                for item in scenario.get('block_group', [])
                for _ in range(item['repeat_cnt'])
                for block in item['block']
            ]
        else:
            self.block_list = []

    def get_block(self, idx: int):
        if len(self.block_list) <= idx:
            res = None
            # if len(self.block_list) != 0:  # 이어서 진행하려면
            self.progress_index = 0
        else:
            res = self.block_list[idx]
        return res

    def reset_block_list(self):
        self.block_list = []

    def update_progress_index(self):
        self.progress_index += 1

    def set_pub_data(self, block_type, block):
        data = {}
        if block_type == 'remocon_transmit':
            data = {item['key']: item['value'] for item in block.get('args', [])}

        return data


@handle_errors
def command_parser(block_manager, command: dict):
    msg = command.get('msg', None)

    if msg == 'run_scenario':
        # 시나리오 조회
        block_manager.init_scenario(id=command.get('data', {}).get('scenario_id', ''))

        # 첫번째 블럭 조회
        block = block_manager.get_block(block_manager.progress_index)
        if block:
            logger.info(f'start!!!!')
            with get_strict_redis_connection() as src:
                publish(src, 'command', {
                    "service": "replay",
                    "level": "info",
                    "msg": block['type'],
                    "data": block_manager.set_pub_data(block['type'], block),
                    "time": time.time()
                })
                
            # TODO 레디스 진행상태 업데이트
        elif block is None:
            logger.info('scenario does not exist')

    elif msg == 'next_block':
        # 진행 인덱스 업데이트
        block_manager.update_progress_index()

        # 다음 블럭 조회
        next_block = block_manager.get_block(block_manager.progress_index)
        if next_block:
            logger.info(f'next!!!! {block_manager.progress_index}')
            with get_strict_redis_connection() as src:
                publish(src, 'command', {
                    "service": "replay",
                    "level": "info",
                    "msg": next_block['type'],
                    "data": block_manager.set_pub_data(next_block['type'], next_block),
                    "time": time.time()
                })

            # TODO 레디스 진행상태 업데이트
        elif next_block is None and block_manager.progress_index == 0:
            logger.info('end!!!!')

    elif msg == 'scenario_stop':
        logger.info('stop!!!!')
        # 시나리오 초기화
        block_manager.reset_block_list()

        # TODO 레디스 진행상태 업데이트


@handle_errors
def main():
    block_manager = BlockManager()

    with get_strict_redis_connection() as src:
        for command in Subscribe(src, RedisChannel.command):
            command_parser(block_manager, command)


if __name__ == '__main__':
    try:
        log_organizer = LogOrganizer()
        log_organizer.set_stream_logger('main')
        log_organizer.set_stream_logger('connection')
        log_organizer.set_stream_logger('error', 10)
        logger.info('Start replay container')

        main()

    finally:
        logger.info('Close replay container')
        log_organizer.close()
