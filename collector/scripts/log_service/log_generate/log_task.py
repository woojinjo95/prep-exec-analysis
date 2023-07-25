import multiprocessing
import threading
import time
import uuid
from typing import List, Dict, Callable

from .generate import (create_stb_output_channel, find_pattern_with_generator, start_stb_output_channel_terminator)
from .template import PatternFinder


def start_log_pattern_finder(connection_info: dict, command: str, patterns: List[str], term_cond_func: Callable = None, kwargs: Dict = {}, match_counts: List[int] = [],
                             duration: float = None, save_detail: bool = False, global_stop_event: multiprocessing.Event = None) -> PatternFinder:
    if term_cond_func is not None and not callable(term_cond_func):
        raise ValueError('term_cond_func must be callable')
    
    stop_event = threading.Event()
    gen = create_stb_output_channel(command=command, 
                                    connection_info=connection_info,
                                    stop_events=[stop_event, global_stop_event])
    
    result = {}
    gen_thrd = threading.Thread(target=find_pattern_with_generator,
                                daemon=True,
                                kwargs={'gen': gen, 
                                        'patterns': patterns, 
                                        'result': result, 
                                        'save_detail': save_detail})
    gen_thrd.start()

    match_counts = {pat: count for pat, count in zip(patterns, match_counts)}
    terminator = threading.Thread(target=start_stb_output_channel_terminator,
                                  daemon=True,
                                  kwargs={'stop_event': stop_event,
                                          'timeout': duration,
                                          'term_cond_func': term_cond_func,
                                          'kwargs': kwargs,
                                          'result': result,
                                          'match_counts': match_counts})
    terminator.start()

    return PatternFinder(
        id=uuid.uuid4(),
        result=result,
        start_time=time.time(),
        end_time=None,
        command=command,
        patterns=patterns,
        stop_event=stop_event,
        global_stop_event=global_stop_event,
        thread=gen_thrd,
        terminator=terminator,
    )


def stop_log_pattern_finder(finder: PatternFinder) -> Dict:
    if finder.stop_event is not None:
        finder.stop_event.set()  # generator and thread will be stopped
    finder.end_time = time.time()
    return finder.result


def wait_log_pattern_finder(finder: PatternFinder) -> Dict:
    finder.thread.join()
    finder.end_time = time.time()
    return finder.result
