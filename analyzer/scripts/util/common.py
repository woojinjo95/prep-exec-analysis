import logging
from pathlib import Path


logger = logging.getLogger('main')


def get_parents_path(path: str, level: int = 0):
    path_object = Path(path)
    return path_object.parents[level]


def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
