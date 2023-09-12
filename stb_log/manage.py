import time
import logging

from scripts.connection.external import get_connection_info
from scripts.log_service.dumpsys.manager import DumpsysManager
from scripts.log_service.logcat.log_manager import LogcatManager

logger = logging.getLogger('main')


logcat_manager = None
dumpsys_manager = None


def start_logcat_manager(connection_info: dict):
    global logcat_manager

    if logcat_manager is not None:
        logger.warning('LogcatManager is already alive')
    else:
        logcat_manager = LogcatManager(connection_info=connection_info)
        logcat_manager.start()
        logger.info('Start LogcatManager')


def stop_logcat_manager():
    global logcat_manager

    if logcat_manager is not None:
        logcat_manager.stop()
        logcat_manager = None
        logger.info('Stop LogcatManager')
    else:
        logger.warning('LogcatManager is not alive')


def start_dumpsys_manager(connection_info: dict):
    global dumpsys_manager

    if dumpsys_manager is not None:
        logger.warning('DumpsysManager is already alive')
    else:
        dumpsys_manager = DumpsysManager(connection_info=connection_info)
        dumpsys_manager.start()
        logger.info('Start DumpsysManager')


def stop_dumpsys_manager():
    global dumpsys_manager

    if dumpsys_manager is not None:
        dumpsys_manager.stop()
        dumpsys_manager = None
        logger.info('Stop DumpsysManager')
    else:
        logger.warning('DumpsysManager is not alive')


def log_start():
    connection_info = get_connection_info()
    start_logcat_manager(connection_info)
    start_dumpsys_manager(connection_info)


def log_stop():
    stop_logcat_manager()
    stop_dumpsys_manager()
    time.sleep(0.1)
