import logging
import os
import threading
import time
import traceback

import config
import requests


logger = logging.getLogger('connection')


def save(upload_queue, stop_event, is_running):
    while not stop_event.is_set():
        is_running.set()
        if upload_queue.qsize() > 0:
            threading.Thread(target=save_log, args=(*upload_queue.get(), )).start()
        else:
            time.sleep(0.1)
    is_running.clear()


def save_log(file_path, logging_session_id, chunk_count, is_finish, collector_chunk_start_time):
    try:
        with open(file_path, 'rb') as f:
            logger.info(f'{file_path} try to save.')
            # insert code here
            logger.info(f'{file_path} save complete.')
    except Exception as e:
        logger.info(traceback.format_exc())
    finally:
        os.remove(file_path)
        logger.info(f'{file_path} remove complete.')
