import json
import logging
import time
import traceback
from multiprocessing import Event
from typing import Generator

from redis.exceptions import ConnectionError as RedisConnectionError

# get_strict_redis_connection is not used in this code, but it used when import with publish
from .redis_connection import StrictRedis, get_strict_redis_connection

logger = logging.getLogger('connection')

process_pubsub_error_dict = {'stack_count': 0, 'last_occured_time': time.time()}


def Subscribe(redis_client: StrictRedis, channel: str, stop_event: Event = Event()) -> Generator[dict, None, None]:
    """_summary_
    redis_client 상 channel에서 JSON 값을 가져옴
    Args:
        redis_client (StrictRedis): 레디스 클라이언트 
        channel (str): 채널명
        stop_event: Mutliprocesse event, 재시작 등을 위한 플래그
    Yields:
        payload: JSON serialize가 가능한 dictionary
    """
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    logger.info(f'Redis subscriber start, subscribing this channel: {channel}')

    while not stop_event.is_set():
        try:
            message = pubsub.get_message(ignore_subscribe_messages=True, timeout=None)
            # logger.debug(f'sub: {message}')
            # message : {'type': 'message', 'pattern': None, 'channel': b'test', 'data': b'{"test": 1}'}
            if isinstance(message, dict):
                payload = json.loads(message['data'])
                yield payload

            if process_pubsub_error_dict['stack_count'] > 0:
                logger.info(f'Successfully reconnected after {process_pubsub_error_dict["stack_count"]} consecutive errors.')
                process_pubsub_error_dict['stack_count'] = 0

        except RedisConnectionError:
            current_occured_time = time.time()
            if current_occured_time - 1 < process_pubsub_error_dict['last_occured_time']:
                process_pubsub_error_dict['stack_count'] += 1
            else:
                logger.error(f'ConnectionError, total consecutive errors: {process_pubsub_error_dict["stack_count"]} in 1 seconds')
                logger.info(traceback.format_exc())
                process_pubsub_error_dict['stack_count'] = 0

            process_pubsub_error_dict['last_occured_time'] = current_occured_time

        except Exception as e:
            logger.error(f'Error in consume function: {e}')
            logger.info(traceback.format_exc())
            time.sleep(1)  # to avoid too many log
