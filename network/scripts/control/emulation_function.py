import logging
from typing import Dict
from uuid import uuid4

from ..configs.config import RedisChannel, RedisDBEnum, get_value, set_value
from ..connection.redis_connection import hget_value, hset_value
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from .network_control.network_functions import (change_packet_block,
                                                change_traffic_control,
                                                reset_network)

HARDWARE_CONFIG = 'hardware_configuration'
ENABLE = 'enable_network_emulation'
BANDWIDTH = 'packet_bandwidth'
DELAY = 'packet_delay'
LOSS = 'packet_loss'
PACKET_BLOCK = 'packet_block'

logger = logging.getLogger('network_control')


def apply_network_emulation():
    nic = get_value('network', 'stb_nic')
    with get_strict_redis_connection(db=RedisDBEnum.hardware) as src:
        bandwidth = hget_value(src, HARDWARE_CONFIG, BANDWIDTH)
        delay = hget_value(src, HARDWARE_CONFIG, DELAY)
        loss = hget_value(src, HARDWARE_CONFIG, LOSS)
        corrupt = None
        duplicate = None
        packet_blocks = hget_value(src, HARDWARE_CONFIG, PACKET_BLOCK, {})

        state = {}

        state.update(change_traffic_control(nic, bandwidth, delay, loss, duplicate, corrupt))
        values = change_packet_block(nic, packet_blocks)
        state.update({'packet_blocks': values})

        set_value('state', 'network_control', state)


def reset_network_emulation():
    with get_strict_redis_connection() as src:
        nic = hget_value(src, 'network', 'stb_nic')
        reset_network(nic)
        hset_value(src, 'state', 'network_control', {})


def add_packet_block(block_args: dict):
    with get_strict_redis_connection(db=RedisDBEnum.hardware) as src:
        packet_block_list = hget_value(src, HARDWARE_CONFIG, PACKET_BLOCK)

        if not isinstance(packet_block_list, list):
            packet_block_list = []

        if {k: v for k, v in block_args.items() if k != 'id'} not in [{k: v for k, v in item.items() if k != 'id'} for item in packet_block_list]:
            logger.info(f'{block_args} is added to packet block list')
            block_args['id'] = str(uuid4())
            updated_packet_block_list = packet_block_list + [block_args]
            hset_value(src, HARDWARE_CONFIG, PACKET_BLOCK, updated_packet_block_list)
        else:
            logger.warning(f'{block_args} is already added')


def update_packet_block(block_args: dict):
    with get_strict_redis_connection(db=RedisDBEnum.hardware) as src:
        packet_block_list = hget_value(src, HARDWARE_CONFIG, PACKET_BLOCK)

        if not isinstance(packet_block_list, list):
            packet_block_list = []

        uuid = block_args.pop('id', None)
        if uuid is not None:
            for packet_block_item in packet_block_list:
                if packet_block_item.get('id') == uuid:
                    packet_block_item.clear()
                    packet_block_item.update(block_args)
                    packet_block_item['id'] = uuid
                    logger.warning(f'{uuid}: {block_args} is updated')

                    hset_value(src, HARDWARE_CONFIG, PACKET_BLOCK, packet_block_list)
                    break
            else:
                logger.warning(f'{block_args} is not valid to remove')
        else:
            logger.warning(f'No uuid is specified: {block_args}')


def delete_packet_block(query: dict):
    with get_strict_redis_connection(db=RedisDBEnum.hardware) as src:
        deleted_item = None
        packet_block_list = hget_value(src, HARDWARE_CONFIG, PACKET_BLOCK)

        if not isinstance(packet_block_list, list):
            packet_block_list = []

        uuid = query.get('id', None)
        if uuid is not None:
            for item in packet_block_list:
                if item.get('id') == uuid:
                    deleted_item = item
                    break

            if deleted_item is not None:
                logger.info(f'{deleted_item} is deleted')
                packet_block_list.remove(deleted_item)
                hset_value(src, HARDWARE_CONFIG, PACKET_BLOCK, packet_block_list)
                return

        logger.warning(f'{query} is not valid to remove')


def apply_network_emulation_args(args: Dict):

    action = args.get('action')
    log_level = 'info'
    log = ''
    updated = {}

    with get_strict_redis_connection(db=RedisDBEnum.hardware) as src:
        if action in ('create', 'delete', 'update'):
            bandwidth_args = args.get(BANDWIDTH)
            delay_args = args.get(DELAY)
            loss_args = args.get(LOSS)
            block_args = args.get(PACKET_BLOCK)

            if bandwidth_args is not None:
                hset_value(src, HARDWARE_CONFIG, BANDWIDTH, bandwidth_args)
                updated['bandwidth'] = bandwidth_args

            if delay_args is not None:
                hset_value(src, HARDWARE_CONFIG, DELAY, delay_args)
                updated['delay'] = delay_args

            if loss_args is not None:
                hset_value(src, HARDWARE_CONFIG, LOSS, loss_args)
                updated['loss'] = loss_args

            if block_args is not None:
                if action == 'create':
                    add_packet_block(block_args)
                    updated['create'] = block_args
                elif action == 'delete':
                    delete_packet_block(block_args)
                    updated['delete'] = block_args
                elif action == 'update':
                    update_packet_block(block_args)
                    updated['update'] = block_args

        elif action == 'start':
            apply_network_emulation()
            hset_value(src, HARDWARE_CONFIG, ENABLE, True)

        elif action == 'stop':
            reset_network_emulation()
            hset_value(src, HARDWARE_CONFIG, ENABLE, False)
        else:
            log_level = 'warning'
            log = f'{action} is not valid'

        publish(src, RedisChannel.command, {'msg': 'network_emulation_response',
                                            'level': log_level,
                                            'data': {'action': action, 'updated': updated, 'log': log}})
