import time
import logging
from functools import wraps
import json
from pathlib import Path


logger = logging.getLogger('main')


def timeit(func: callable):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.info(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def get_parents_path(path: str, level: int = 0):
    path_object = Path(path)
    return path_object.parents[level]


def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
