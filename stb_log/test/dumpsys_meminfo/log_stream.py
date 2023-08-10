from datetime import datetime, timedelta
from collections import defaultdict


def split_log_stream(log_stream, split_patterns):
    lines = []
    current_split_pattern_key = list(split_patterns.keys())[0]
    for line in log_stream:
        striped_line = line.strip()
        added = False
        for k, r in split_patterns.items():
            if r.match(striped_line):
                if lines:
                    yield current_split_pattern_key, lines
                lines = [striped_line]
                current_split_pattern_key = k
                added = True
                break
        if striped_line and added is False:
            lines.append(striped_line)
    yield current_split_pattern_key, lines


def quantize_time(dt=None, roundTo=10):
    """Round a datetime object to any time lapse in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt is None:
        dt = datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + timedelta(0, rounding - seconds, -dt.microsecond)


def get_quantize_times(min_t, max_t, delta):
    dt = timedelta(seconds=delta)
    current_time = min_t
    quantized_times = []
    while(True):
        if current_time < max_t + dt:
            quantized_times.append(current_time)
            current_time += dt
        else:
            break
    return quantized_times


def convert_memory_string(size_str):
    size_str = size_str.upper()
    if 'K' in size_str:
        size_str = size_str.replace("K", "")
        product = 1024
    elif "M" in size_str:
        size_str = size_str.replace("M", "")
        product = 1024 * 1024
    elif "G" in size_str:
        size_str = size_str.replace("G", "")
        product = 1024 * 1024 * 1024
    elif "T" in size_str:
        size_str = size_str.replace("T", "")
        product = 1024 * 1024 * 1024 * 1024
    elif "E" in size_str:
        size_str = size_str.replace("E", "")
        product = 1
    else:
        product = 1
    return int(product * float(size_str))


def check_overlap(range1, range2):
    start1, end1 = range1
    start2, end2 = range2
    if (
        (start1 < start2 and end1 < start2) and (start1 < end2 and end1 < end2) or
        (start1 > start2 and end1 > start2) and (start1 > end2 and end1 > end2)
    ):
        return False
    else:
        return True


def convert_timestamp(timestamp):
    try:
        current_time_stamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        try:
            current_time_stamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            current_time_stamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%f")
    return current_time_stamp
