import threading
import time
from scripts.connection.stb_connection.utils import check_connection
from scripts.connection.external import get_connection_info
from scripts.connection.redis_conn import set_value 


class ConnectionChecker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(1)
            connection_info = get_connection_info()
            connected = check_connection(connection_info)
            if connected:
                set_value('connection_status', 'connected', True)
            else:
                set_value('connection_status', 'connected', False)
