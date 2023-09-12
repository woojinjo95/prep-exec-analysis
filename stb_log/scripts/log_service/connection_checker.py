import logging
import time

from scripts.config.constant import RedisDB
from scripts.connection.external import get_connection_info
from scripts.connection.redis_conn import set_value
from scripts.connection.redis_pubsub import publish_msg
from scripts.connection.stb_connection.utils import check_connection

logger = logging.getLogger('connection')


def connection_checker():
    prev_connected = None

    while True:
        time.sleep(1)
        connection_info = get_connection_info()
        connected = check_connection(connection_info)
        if connected:
            set_value('log_connection_status', 'is_connected', 'log_connected', RedisDB.hardware)
            logger.info('Connection Checking... log connected')
        else:
            set_value('log_connection_status', 'is_connected', 'log_disconnected', RedisDB.hardware)
            logger.info('Connection Checking... log disconnected')

        if prev_connected is not None and prev_connected != connected:
            publish_msg({'log_connection_status_changed': 'true'}, 'log_connection_status')
            logger.info(f'Connection Checking... log status changed. {prev_connected} -> {connected}')

        prev_connected = connected
