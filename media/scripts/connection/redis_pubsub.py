import json
import logging
import time
import traceback
from multiprocessing import Event
from typing import Generator

from redis.exceptions import ConnectionError as RedisConnectionError

from .redis_connection import StrictRedis

logger = logging.getLogger('connection')

process_pubsub_error_dict = {'stack_count': 0, 'last_occured_time': time.time()}


def publish(redis_client: StrictRedis, channel: str, payload: dict):
    data = json.dumps(payload)
    return redis_client.publish(channel, data)


def Subscribe(redis_client: StrictRedis, channel: str, stop_event: Event = Event()) -> Generator:
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    logger.info(f'Redis subscriber start in {channel}')

    while not stop_event.is_set():
        try:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                logger.debug(f'sub: {message}')
                # message : {'type': 'message', 'pattern': None, 'channel': b'test', 'data': b'{"test": 1}'}
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
