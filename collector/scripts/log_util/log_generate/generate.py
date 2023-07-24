import time
import logging
from multiprocessing import Event
from typing import Generator, List, Dict, Callable
import re

from scripts.log_service.stb_log.stb_connection.utils import get_connection_info, exec_command_generator


logger = logging.getLogger('connection')


# 셋탑 박스 내부 특정 command 입력하였을 때 그 output을 generate 하는 함수
def create_stb_output_channel(command: str, slot_index: int = 0, 
                              stop_events: List[Event] = [], su_prefix: bool = False) -> Generator[str, None, None]:
    connection_info = get_connection_info(slot_index)
    logger.info(f'create settop box output channel. connection info: {connection_info}')
    gen = exec_command_generator(command_script=command, 
                                 connection_info=connection_info, 
                                 stop_events=stop_events,
                                 su_prefix=su_prefix)
    return gen


def find_pattern_with_generator(gen: Generator[str, None, None], patterns: List[str], result: Dict={}, save_detail: bool = False):
    # init result
    for pat in patterns:
        result[pat] = {
            'count': 0,
            'detail': {
                'timestamps': [],
                'originals': [],
            }
        }

    logger.info(f'find pattern with generator. patterns: {patterns}')
    # check pattern
    for line in gen:
        # print(line)
        for pat in patterns:
            found = re.search(pat, line)
            if found:
                result[pat]['count'] += 1
                if save_detail:
                    result[pat]['detail']['timestamps'].append(time.time())
                    result[pat]['detail']['originals'].append(line)
                else:
                    pass
            else:
                pass

    logger.info(f'finish to find pattern with generator.')
    return result


def start_stb_output_channel_terminator(stop_event: Event, timeout: float, term_cond_func: Callable, kwargs: Dict, result: Dict, match_counts: Dict):
    start_time = time.time()

    def check_stop_condition() -> bool:
        # check stop condition
        try:
            if callable(term_cond_func) and term_cond_func(**kwargs):
                logger.info('term_cond_func is triggered')
                return True
        except Exception as err:
            logger.error(f'Error while term_cond_func. Cause: {err}')
            return True
        # check timeout
        if timeout is not None:
            duration = time.time() - start_time
            if duration >= timeout:
                logger.info('timeout is triggered')
                return True
        # check match count
        for pattern, info in result.items():
            count = info['count']  # current count
            match_count = match_counts.get(pattern, None)  # if None, ignore match count
            if match_count is not None and count >= match_count:
                logger.info(f'match count is triggered. pattern: {pattern}, count: {count}, match_count: {match_count}')
                return True
        return False

    while True:
        time.sleep(1)
        if check_stop_condition():
            logger.info('stop condition is triggered')
            stop_event.set()
            break
        if stop_event.is_set():
            logger.info('stop event is set. terminator is stopped')
            break
    logger.info('finish to start stb output channel terminator')
