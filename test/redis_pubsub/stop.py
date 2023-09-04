from connection.redis_pubsub import unit_publish, Subscribe, get_strict_redis_connection
from connection.redis_connection import hget_value
from connection.apis import new_scenario
from simple_logger import simple_logger
import time


def main():
    with get_strict_redis_connection() as src:
        if hget_value(src, 'state', 'streaming') != 'idle':
            unit_publish(payload={"msg": "recording",
                                  "data": {"interval": 180}})
            for command in Subscribe(src, 'command'):
                if command.get('msg') == 'recording_response':
                    break
    time.sleep(1)

    unit_publish(payload={'msg': 'streaming', 'data': {'action': 'stop'}})
    unit_publish(payload={'msg': 'stb_log', 'data': {'control': 'stop'}})


if __name__ == '__main__':
    logger = simple_logger('test')
    # unit_publish(payload={'msg': 'streaming', 'data': {'action': 'stop'}})
    main()
