import logging
from pathlib import Path


def get_parents_path(path: str, level: int = 0):
    path_object = Path(path)
    return path_object.parents[level]
