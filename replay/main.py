import logging

from scripts.configs.constant import RedisChannel
from scripts.connection.mongo_db.crud import load_one_from_mongodb
from scripts.connection.redis_pubsub import (Subscribe,
                                             get_strict_redis_connection,
                                             publish)
from scripts.log_organizer import LogOrganizer
from scripts.utils._exceptions import handle_errors

logger = logging.getLogger('main')


class BlockListManager:
    def __init__(self):
        self.block_list = []

    def init(self):
        scenario = load_one_from_mongodb(col='scenario')
        self.block_list = [
            {**block, 'network': 'start', 'idx': block_idx + len(item['block']) * item_idx}
            for item in scenario.get('block_group', [])
            for item_idx in range(item['repeat_cnt'])
            for block_idx, block in enumerate(item['block'])
        ]

    def get_block(self, idx: int):
        # TODO 타입에 맞게 변경
        return None if len(self.block_list) <= idx else self.block_list[idx]

    def reset_block_list(self):
        self.block_list = []


@handle_errors
def command_parser(block_list_manager, command: dict):
    args = command.get('replay', None)

    if args == 'run':
        with get_strict_redis_connection() as src:
            block_list_manager.init()
            publish(src, 'command', block_list_manager.get_block(0))

    elif args == 'stop':
        logger.info('stop!!!!')
        block_list_manager.reset_block_list()
        # TODO 이어서 실행

    elif args == 'next':
        with get_strict_redis_connection() as src:
            next_block = block_list_manager.get_block(command.get('idx')+1)
            if next_block:
                publish(src, 'command', next_block)


@handle_errors
def main():
    block_list_manager = BlockListManager()

    with get_strict_redis_connection() as src:
        for command in Subscribe(src, RedisChannel.command):
            command_parser(block_list_manager, command)


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
