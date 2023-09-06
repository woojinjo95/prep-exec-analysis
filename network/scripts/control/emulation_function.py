import logging
from typing import Dict
from uuid import uuid4

from ..configs.config import RedisChannel, RedisDBEnum, get_value, set_value
from ..connection.redis_connection import hget_value, hset_value, StrictRedis
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from .network_control.network_functions import (change_packet_block,
                                                change_traffic_control,
                                                reset_network, ebtables_clear, ebtables_init)
from .network_control.value_rules import DefaultValues

HARDWARE_CONFIG = 'hardware_configuration'
ENABLE = 'enable_network_emulation'
BANDWIDTH = 'packet_bandwidth'
DELAY = 'packet_delay'
LOSS = 'packet_loss'
PACKET_BLOCK = 'packet_block'

logger = logging.getLogger('network_control')


def get_requested_state() -> Dict:
    with get_strict_redis_connection(db=RedisDBEnum.hardware) as src:
        bandwidth = hget_value(src, HARDWARE_CONFIG, BANDWIDTH, None)
        delay = hget_value(src, HARDWARE_CONFIG, DELAY, None)
        loss = hget_value(src, HARDWARE_CONFIG, LOSS, None)
        corrupt = None
        duplicate = None
        packet_blocks = hget_value(src, HARDWARE_CONFIG, PACKET_BLOCK, [])

        return {'bandwidth': bandwidth,
                'delay': delay,
                'loss': loss,
                'duplicate': duplicate,
                'corrupt': corrupt,
                'packet_blocks': packet_blocks}


def apply_network_emulation():
    nic = get_value('network', 'stb_nic')
    requested_state = get_requested_state()
    packet_blocks = requested_state.pop('packet_blocks', [])
    state = {}
    state.update(change_traffic_control(nic, **requested_state))
    state.update({'packet_blocks': change_packet_block(nic, packet_blocks)})

    set_value('state', 'network_control', state)
    set_value(HARDWARE_CONFIG, ENABLE, True, db=RedisDBEnum.hardware)


def change_network_emulation():
    # 위 apply와 달리 traffic_clear를 적용하지 않음
    nic = get_value('network', 'stb_nic')
    prev_settings = get_value('state', 'network_control')
    requested_state = get_requested_state()

    state = {}
    for element, value in requested_state.items():
        if element != 'packet_blocks':
            if value is not None and value != prev_settings.get(element):
                state.update(change_traffic_control(nic, **{element: value}))
            else:
                pass
                # do nothing
        else:
            # 원래는 requested_state와 prev_settings 비교 후 변경/삭제/추가 된 항목 확인, 개별로 규칙 삭제 구문을 command_executor에 추가해야 함
            # 다만 너무 복잡한 작업이라 판단, 무조건 삭제 후 재적용
            # 전체 개수가 수백~수천 개가 아닌 이상 문제 없다고 판단
            # 순간적으로 인터넷 연결이 생길 수 있음
            packet_blocks = value or []
            packet_blocks = [{k: v for k, v in el.items() if k != 'id'} for el in packet_blocks]
            prev_packet_blocks = prev_settings.get('packet_blocks')

            if prev_packet_blocks == packet_blocks:
                state.update({'packet_blocks': prev_packet_blocks})
            else:
                ebtables_clear()
                ebtables_init(nic)
                state.update({'packet_blocks': change_packet_block(nic, packet_blocks)})

    set_value('state', 'network_control', state)


def reset_network_emulation():
    with get_strict_redis_connection() as src:
        nic = hget_value(src, 'network', 'stb_nic')
        reset_network(nic)
        hset_value(src, 'state', 'network_control', {})
    
    set_value(HARDWARE_CONFIG, ENABLE, False, db=RedisDBEnum.hardware)


def add_packet_block(block_args: dict):
    with get_strict_redis_connection(db=RedisDBEnum.hardware) as src:
        packet_block_list = hget_value(src, HARDWARE_CONFIG, PACKET_BLOCK)

        if not isinstance(packet_block_list, list):
            packet_block_list = []

        if {k: v for k, v in block_args.items() if k != 'id'} not in [{k: v for k, v in item.items() if k != 'id'} for item in packet_block_list]:
            logger.info(f'{block_args} is added to packet block list')
            block_args['id'] = str(uuid4())
            updated_packet_block_list = packet_block_list + [{k: v for k, v in block_args.items() if v != ''}]
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
                    packet_block_item.update({k: v for k, v in block_args.items() if v != ''})
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
        '''
        action
            start: 규칙 적용
            stop:  규칙 해제

            create: 규칙 추가
            delete: 규칙 삭제
            update: 규칙 수정
            reset:  모든 규칙 기본값으로 초기화 
        '''
        if action == 'start':
            apply_network_emulation()

        elif action == 'stop':
            reset_network_emulation()

        else:
            if action == 'reset':
                hset_value(src, HARDWARE_CONFIG, BANDWIDTH, DefaultValues.bandwidth)
                hset_value(src, HARDWARE_CONFIG, DELAY, DefaultValues.delay)
                hset_value(src, HARDWARE_CONFIG, LOSS, DefaultValues.loss)
                hset_value(src, HARDWARE_CONFIG, PACKET_BLOCK, [])

                updated.update({BANDWIDTH: DefaultValues.bandwidth,
                                DELAY: DefaultValues.delay,
                                LOSS: DefaultValues.loss,
                                PACKET_BLOCK: []})

            elif action in ('create', 'delete', 'update'):
                bandwidth_args = args.get(BANDWIDTH)
                delay_args = args.get(DELAY)
                loss_args = args.get(LOSS)
                block_args = args.get(PACKET_BLOCK)

                if action == 'update':
                    # 아래 3개 값은 추가/삭제되지 않고 수정만 된다.
                    if bandwidth_args is not None:
                        hset_value(src, HARDWARE_CONFIG, BANDWIDTH, bandwidth_args)
                        updated[BANDWIDTH] = bandwidth_args

                    if delay_args is not None:
                        hset_value(src, HARDWARE_CONFIG, DELAY, delay_args)
                        updated[DELAY] = delay_args

                    if loss_args is not None:
                        hset_value(src, HARDWARE_CONFIG, LOSS, loss_args)
                        updated[LOSS] = loss_args

                if block_args is not None:
                    # packet_block은 추가/삭제/변경이 가능하며 각각마다 다른 함수를 적용해야한다.
                    # 다만 모든 action에서 packet block이 포함되지 않고, 위 3개 값과 구조가 다르니 따로 처리
                    if action == 'create':
                        add_packet_block(block_args)
                        updated['create'] = block_args
                    elif action == 'delete':
                        delete_packet_block(block_args)
                        updated['delete'] = block_args
                    elif action == 'update':
                        update_packet_block(block_args)
                        updated['update'] = block_args
            else:
                log_level = 'warning'
                log = f'{action} is not valid'

            if log_level == 'info' and hget_value(src, HARDWARE_CONFIG, ENABLE):
                change_network_emulation()

        publish(src, RedisChannel.command, {'msg': 'network_emulation_response',
                                            'level': log_level,
                                            'data': {'action': action, 'updated': updated, 'log': log}})
