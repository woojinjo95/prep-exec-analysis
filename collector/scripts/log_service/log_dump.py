import logging
import os
import threading
import time

import config
import requests


logger = logging.getLogger('log_collector')

LOG_BACKEND_API_URL = os.environ.get('LOG_BACKEND_API_URL')
def upload(upload_queue, stop_event, is_running):
    while not stop_event.is_set():
        is_running.set()
        if upload_queue.qsize() > 0:
            threading.Thread(target=upload_file, args=(*upload_queue.get(), )).start()
        else:
            time.sleep(0.1)
    is_running.clear()

def upload_file(file_path, logging_session_id, chunk_count, is_finish, collector_chunk_start_time):
    try_count = 0
    time_out = config.UPLOAD_TIMEOUT
    while try_count < config.UPLOAD_TRY_COUNT:  # 최대 10회 try
        try:
            with open(file_path, 'rb') as f:
                logger.info(f'{file_path} try to upload.')
                upload_file = {'uploadfile': f}
                post_json = {
                    'logging_session_id': logging_session_id,
                    'chunk_count': chunk_count,
                    'is_finish': is_finish,
                    'collector_chunk_start_time': collector_chunk_start_time
                }
                # 120 seconds (2 mins) timeout
                headers = current_access_token_headers()
                response = requests.post(f'{LOG_BACKEND_API_URL}/log_chunks', files=upload_file,
                                         params=post_json, timeout=time_out, headers=headers)
            if response.status_code == 200:
                logger.info(f'{file_path} upload complete.')
                os.remove(file_path)  # upload가 잘 되었을 경우에만 local에서 파일 삭제
                break
            else:
                logger.info(f'{file_path} upload fail. Try again.')
        except Exception as e:
            logger.info(e)
            logger.info(f'{file_path} upload fail. Try again.')
        time.sleep(5)
        try_count += 1  # try count 증가
        time_out += 20  # 60초부터 20초씩 늘려나감
