import logging
import os
import time
import traceback
import glob

from scripts.file_service.log_manage.db_connection import LogManagerDBConnection


logger = logging.getLogger('connection')

db_conn = LogManagerDBConnection()


def save():
    completed_log_dir = 'completed_logs'
    os.makedirs(completed_log_dir, exist_ok=True)

    while True:
        try:
            file_paths = sorted(glob.glob(os.path.join(completed_log_dir, '*.log')))
            if len(file_paths) > 0:
                save_log(file_paths[0])
        except Exception as e:
            logger.info(traceback.format_exc())
        finally:
            time.sleep(1)


def save_log(file_path: str):
    try:
        with open(file_path, 'rb') as f:
            logger.info(f'{file_path} try to save.')
            ##### Save log here
            insert_to_db(file_path)
            #####
            logger.info(f'{file_path} save complete.')
    except Exception as e:
        logger.info(traceback.format_exc())
    finally:
        os.remove(file_path)
        logger.info(f'{file_path} remove complete.')


def insert_to_db(file_path: str):
    # db_conn.save_data((time.time(), log_line))
    pass
