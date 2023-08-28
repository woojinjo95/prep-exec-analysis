from scripts.connection.redis_pubsub import publish_msg


def publish_remocon_msg(key: str, company: str):
    # PUBLISH command  '{"msg": "remocon_transmit", "data": {"key": "right", "type": "ir", "press_time": 0, "name": "roku"}}'
    publish_msg({
        'key': key,
        'type': 'ir',
        'press_time': 0,
        'name': company,
    }, 'remocon_transmit')
