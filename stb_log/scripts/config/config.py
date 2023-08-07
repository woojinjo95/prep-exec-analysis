import os
from ast import literal_eval
from typing import Any


def get_setting_with_env(key: str, default: Any = None):
    try:
        value = os.getenv(key, default)
        if value is None:
            return None
        try:
            decoded = literal_eval(value)
        except Exception:
            decoded = value
        return decoded
    except Exception:
        return default
    