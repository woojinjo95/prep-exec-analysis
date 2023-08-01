import time
import logging
from functools import wraps
import dataclasses

from dotenv import dotenv_values


logger = logging.getLogger('main')


def get_dotenvs_value(path: str, name: str, default: str = '') -> str:
    if name in dotenv_values(path):
        value = dotenv_values(path)[name]
    else:
        value = default
    return value


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


def convert_to_dict(data):
    if dataclasses.is_dataclass(data):
        return dataclasses.asdict(data)
    elif hasattr(data, "__dict__"):
        return vars(data)
    else:
        raise TypeError("Data is neither a dataclass instance nor an object")