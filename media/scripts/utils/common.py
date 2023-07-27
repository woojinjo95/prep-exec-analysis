import re
import time
import logging
from collections import defaultdict
from typing import Iterable, List
import inspect
import datetime
from functools import wraps
import requests

import cv2
import numpy as np
from dotenv import dotenv_values


logger = logging.getLogger('main')


def get_dotenvs_value(path: str, name: str, default: str = '') -> str:
    if name in dotenv_values(path):
        value = dotenv_values(path)[name]
    else:
        value = default
    return value


def camel_to_snake(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def calc_list_adjacent_diffence_average(data: Iterable[float]) -> float:
    diff_list = [j - i for i, j in zip(data, data[1:])]
    return sum(diff_list) / max(1, len(diff_list))


def character_remover(string: str, chars: Iterable[str] = ', /<>?|:\t\n\\') -> str:
    for char in chars:
        string = string.replace(char, '')
    return string


def is_iterable(obj: any) -> bool:
    return hasattr(obj, '__iter__')


def figure_to_array(fig: any) -> np.ndarray:
    fig.canvas.draw()
    f_arr = np.array(fig.canvas.renderer._renderer)
    return cv2.cvtColor(f_arr, cv2.COLOR_RGBA2BGR)


def group_duplicated_value_in_dict(target_dict: dict) -> List[list]:
    reversed_dict = defaultdict(list)
    for key, value in target_dict.items():
        reversed_dict[value].append(key)
    return list(reversed_dict.values())


# TODO: 둘 데가 없어서 여기다 둠
def construct_recovery_history(history_log: str) -> dict:
    logger.info(f'history log | {history_log}')
    return {
        "created_at": time.time(),  # 현재 시간
        "history": history_log
    }


def join_list_value(target_list: Iterable[any], join_chr: str = ',') -> str:
    return join_chr.join([str(element) for element in target_list])


def convert_variable_to_name(var: any) -> str:
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]


def bytes2np_array(image_bytes: bytes, dtype=np.uint8, decoder=cv2.IMREAD_COLOR) -> bytes:
    if type(image_bytes) != np.ndarray:
        numpy_bytes = np.fromstring(image_bytes, dtype)
        return cv2.imdecode(numpy_bytes, decoder)
    return image_bytes


def datetime_str_to_datetime(datetime_str: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(datetime_str)


def datetime_str_to_timestamp(datetime_str: str) -> str:
    datetime_object = datetime_str_to_datetime(datetime_str)
    return datetime_object.timestamp()


def timestamp2ms(timestamp: float) -> int:
    return max(0, int(timestamp * 1000))


# [(0,1) -> (1,2) -> (2,3) -> ... -> (-2, -1)]
def single_adjacent_zip(iterable: Iterable):
    prev = None
    for item in iterable:
        if prev is None:
            prev = item
        else:
            current = item
            yield prev, current
            prev = current


def ClusterGenerator(cluster_margin: int, min_cluster_point_num: int, max_cluster_point_num=None):
    TIMER_DEACTIVATION = -1
    TIMER_TRIGGER = 0
    timer = TIMER_DEACTIVATION
    index = -1
    now_cluster_indices = []
    yield_flag = False
    result = None
    while True:
        index += 1
        yield_flag = False
        estimated = yield result
        if timer > TIMER_TRIGGER:
            timer -= 1
            if estimated:
                now_cluster_indices.append(index)
                timer = cluster_margin
        elif timer == TIMER_TRIGGER:
            timer = TIMER_DEACTIVATION
            if len(now_cluster_indices) >= min_cluster_point_num:
                yield_flag = True
        elif timer == TIMER_DEACTIVATION:
            if estimated:
                timer = cluster_margin
                now_cluster_indices = [index]
        if max_cluster_point_num and len(now_cluster_indices) >= max_cluster_point_num:
            yield_flag = True
        result = now_cluster_indices if yield_flag else None


def get_boolean_cluster(boolean_list: List[bool], margin: int, min_count: int):
    clusters = []
    cluster_gen = ClusterGenerator(margin, min_count)
    next(cluster_gen)
    for value in list(boolean_list) + [False] * (margin + 1):
        cluster = cluster_gen.send(value)
        if cluster:
            clusters.append(cluster)
    return clusters


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


def get_image_by_url(url: str) -> np.ndarray:
    try:
        res = requests.get(url)
        array = bytes2np_array(res.content)
    except Exception as err:
        logger.error(f'get_image_by_url error. Cause: {err}')
        array = None
    return array


def split_list_into_chunks(li: List, n: int) -> List[List]:
    return [li[i * n:(i + 1) * n] for i in range((len(li) + n - 1) // n)]


def get_nested_key(data: dict, *keys, default: any = None) -> any:
    current = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def ordinal_suffix(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix
