import logging

from scripts.configs.constant import RedisChannel, ServiceType
from scripts.connection.mongo_db.crud import load_one_from_mongodb
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

    def init_scenario(self):
        scenario = load_one_from_mongodb(col='scenario')
        self.block_list = [
            {**block, getattr(ServiceType, block['type']): 'start'}
            for item in scenario.get('block_group', [])
            for _ in range(item['repeat_cnt'])
            for block in item['block']
        ]

    def get_block(self, idx: int):
        if len(self.block_list) <= idx:
            res = None
            # ------ 이어서 진행하려면
            if len(self.block_list) != 0:  # ------
                self.progress_index = 0
        else:
            res = self.block_list[idx]
        return res

    def reset_block_list(self):
        self.block_list = []

    def update_progress_index(self):
        self.progress_index += 1


@handle_errors
def command_parser(block_manager, command: dict):
    args = command.get('replay', None)

    if args == 'run':
        block_manager.init_scenario()
        logger.info(f'start!!!!')

        with get_strict_redis_connection() as src:
            publish(src, 'command', block_manager.get_block(block_manager.progress_index))

    elif args == 'stop':
        logger.info('stop!!!!')
        block_manager.reset_block_list()

    elif args == 'next':
        block_manager.update_progress_index()
        next_block = block_manager.get_block(block_manager.progress_index)
        if next_block:
            with get_strict_redis_connection() as src:
                publish(src, 'command', next_block)
        elif next_block is None and block_manager.progress_index == 0:
            logger.info('end!!!!')


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