from typing import List
from scripts.monkey.util import exec_keys


class Monkey:
    def __init__(self, key_interval: float, key_candidates: List[str], root_keyset: List[str],
                 profile: str):
        self.key_interval = key_interval
        self.key_candidates = key_candidates
        self.root_keyset = root_keyset
        self.profile = profile

    def run(self):
        pass

    def exec_keys(self, keys: List[str]):
        exec_keys(keys, self.key_interval, self.profile)
