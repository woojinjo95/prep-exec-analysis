import logging
import os
import time
import traceback
import glob

from scripts.util.common import check_stop_events


logger = logging.getLogger('connection')


def save(stop_events):
    completed_log_dir = 'completed_logs'
    os.makedirs(completed_log_dir, exist_ok=True)

    while not check_stop_events(stop_events):
        try:
            file_path = sorted(glob.glob(os.path.join(completed_log_dir, '*.log')))[0]
            save_log(file_path)
        except Exception as e:
            logger.info(traceback.format_exc())
        finally:
            time.sleep(1)


def save_log(file_path):
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
