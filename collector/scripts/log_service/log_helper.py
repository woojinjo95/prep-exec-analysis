import logging
import logging.handlers
import multiprocessing
from threading import Thread
import os
import traceback


logger = logging.getLogger('main')


class LogHelper():
    def __init__(self):
        self.listener = None

        # define log colors
        string_effect = '\033[2m'
        colors = {
            'GREEN': '\033[32m',
            'YELLOW': '\033[33m',
            'BLUE': '\033[34m',
            'MAGENTA': '\033[35m',
            'CYAN': '\033[36m',
            'BRIGHT_MAGENTA': f'{string_effect}\033[95m',
            'BRIGHT_CYAN': f'{string_effect}\033[96m',
            'BRIGHT_GREEN': f'{string_effect}\033[92m',
            'BRIGHT_BLUE': f'{string_effect}\033[94m',
            'BRIGHT_YELLOW': f'{string_effect}\033[93m',
            'RED': '\033[31m',
            'RESET_ALL': '\033[0m',
        }
        self.colors_list = list(colors.values())
        self.default_format = colors['RESET_ALL']

        # make log directory
        if os.path.exists('/app'):
            self.base_log_dir = os.path.join('/app', 'logs')
        else:
            self.base_log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(self.base_log_dir, exist_ok=True)

    def start_listening(self, name: str, queue: multiprocessing.Queue):
        self.listener = Thread(target=self.consume_log_queue, args=(name, queue))
        self.listener.start()

    def end_listening(self, queue: multiprocessing.Queue):
        queue.put(None)
        self.listener.join()
        logger.info('log listener end...')

    def consume_log_queue(self, name: str, queue: multiprocessing.Queue):
        logger = self.set_time_rotating_file_logger(name)
        while True:
            try:
                record = queue.get()
                if record is None:
                    break
                logger.handle(record)
            except Exception:
                logger.error('logger helper listener problem')
                logger.info(traceback.format_exc())

    def set_stream_logger(self, name: str, color_index: int = 0) -> logging.Logger:
        logger = logging.getLogger(name)
        color = self.colors_list[color_index % len(self.colors_list)]
        colored_log_format = f"{color}{name:<12} | [%(asctime)s] %(levelname)8s | %(message)s {self.default_format}"
        colered_formatter = logging.Formatter(colored_log_format)

        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.INFO)
        streamhandler.setFormatter(colered_formatter)
        logger.addHandler(streamhandler)
        return logger

    def set_file_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        log_format = f"{name:<12} | [%(asctime)s] %(levelname)8s | %(message)s"
        formatter = logging.Formatter(log_format)

        filehandler = logging.FileHandler(filename=os.path.join(self.base_log_dir, f'{name}.log'), encoding='utf-8-sig')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger

    # 1000000000 byte = 1 GB 이므로 최대 10 GB 백업
    def set_rotating_file_logger(self, name: str, maxBytes: int = 1000000000, backupCount: int = 10) -> logging.Logger:
        logger = logging.getLogger(name)
        log_format = f"%(name)-12s | [%(asctime)s] %(levelname)8s | %(message)s"
        formatter = logging.Formatter(log_format)

        filehandler = logging.handlers.RotatingFileHandler(os.path.join(self.base_log_dir, f'{name}.log'),
                                                           mode='a', maxBytes=maxBytes, backupCount=backupCount, encoding='utf-8-sig')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger

    # 자정마다 롤오버하고 최대 100일치 저장
    def set_time_rotating_file_logger(self, name: str, backupCount: int = 100) -> logging.Logger:
        logger = logging.getLogger(name)
        log_format = f"%(name)-12s | [%(asctime)s] %(levelname)8s | %(message)s"
        formatter = logging.Formatter(log_format)

        filehandler = logging.handlers.TimedRotatingFileHandler(os.path.join(self.base_log_dir, f'{name}.log'),
                                                                when='midnight', backupCount=backupCount, encoding='utf-8-sig')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger

    def set_queue_logger(self, queue: multiprocessing.Queue, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        qh = logging.handlers.QueueHandler(queue)
        logger.addHandler(qh)
        return logger


def init_log_helper(log_helper: LogHelper, log_queue: multiprocessing.Queue):
    log_helper.start_listening('total', log_queue)

    log_helper.set_queue_logger(log_queue, 'main')
    log_helper.set_queue_logger(log_queue, 'user')
    log_helper.set_queue_logger(log_queue, 'connection')
    log_helper.set_queue_logger(log_queue, 'scheduler')
    log_helper.set_queue_logger(log_queue, 'analysis')
    log_helper.set_queue_logger(log_queue, 'licence')
    log_helper.set_queue_logger(log_queue, 'media')
    log_helper.set_queue_logger(log_queue, 'report')
    log_helper.set_queue_logger(log_queue, 'event_log')
    log_helper.set_queue_logger(log_queue, 'remocon')
    log_helper.set_queue_logger(log_queue, 'serial')
    log_helper.set_queue_logger(log_queue, 'daq')
    log_helper.set_queue_logger(log_queue, 'error')

    log_helper.set_stream_logger('main', 1)         # yellow
    log_helper.set_stream_logger('user', 2)         # blue
    log_helper.set_stream_logger('connection', 3)   # magenta
    log_helper.set_stream_logger('scheduler', 4)    # cyan
    log_helper.set_stream_logger('analysis', 5)     # bright magenta
    log_helper.set_stream_logger('licence', 5)     # bright magenta
    log_helper.set_stream_logger('media', 6)        # bright cyan
    log_helper.set_stream_logger('report', 0)       # green
    log_helper.set_stream_logger('event_log', 7)    # bright green
    log_helper.set_stream_logger('remocon', 8)      # bright blue
    log_helper.set_stream_logger('serial', 8)       # bright blue
    log_helper.set_stream_logger('daq', 8)          # bright blue
    log_helper.set_stream_logger('error', 10)          # RED
    # 9, bright yellow

    # log_helper.set_file_logger('main')
    # log_helper.set_file_logger('user')
    # log_helper.set_file_logger('connection')
    # log_helper.set_file_logger('scheduler')
    # log_helper.set_file_logger('analysis')
    # log_helper.set_file_logger('media')
    # log_helper.set_file_logger('report')
    # log_helper.set_file_logger('remocon')
    # log_helper.set_file_logger('serial')
    # log_helper.set_file_logger('daq')

    return log_helper


def terminate_log_helper(log_helper: LogHelper, log_queue: multiprocessing.Queue):
    log_helper.end_listening(log_queue)
