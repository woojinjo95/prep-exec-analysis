import uuid
from dataclasses import dataclass
import multiprocessing
import threading


@dataclass
class PatternFinder:
    id: uuid.UUID
    result: dict
    start_time: float
    end_time: float
    command: str
    patterns: list
    stop_event: threading.Event
    global_stop_event: multiprocessing.Event
    thread: threading.Thread
    terminator: threading.Thread
    