from typing import Dict
from scripts.connection.redis_conn import get_all


def get_monkey_test_arguments() -> Dict:
    return get_all('monkey_test_arguments')
