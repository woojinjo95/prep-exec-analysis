import time
from scripts.connection.redis_pubsub import publish_msg


def publish_remocon_msg(company: str, key: str, sleep: float=0, type: str='ir'):
    # PUBLISH command  '{"msg": "remocon_transmit", "data": {"key": "right", "type": "ir", "press_time": 0, "name": "roku"}}'
    publish_msg({
        'key': key,
        'type': type,
        'press_time': 0,
        'name': company,
    }, 'remocon_transmit')
    time.sleep(sleep)
