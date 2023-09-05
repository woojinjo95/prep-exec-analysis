import threading
import time
import logging
from scripts.connection.stb_connection.utils import check_connection
from scripts.connection.external import get_connection_info
from scripts.connection.redis_conn import set_value 
from scripts.config.constant import RedisDB
from scripts.connection.redis_pubsub import publish_msg


logger = logging.getLogger('connection')

class ConnectionChecker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
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
