from connection.redis_pubsub import unit_publish
from connection.apis import new_scenario
from simple_logger import simple_logger


def main():
    log_config_95 = {
        "msg": "config",
        "data": {
            "mode": "adb",
            # "host": "192.168.10.35",
            "host": "192.168.30.30",
            "port": "5555",
            "username": "",
            "password": "",
        }
    }

    # new_scenario()

    # unit_publish(payload=log_config_95)
    unit_publish(payload={'msg': 'streaming', 'data': {'action': 'start'}})
    unit_publish(payload={'msg': 'stb_log', 'data': {'control': 'start'}})


if __name__ == '__main__':
    logger = simple_logger('test')

    main()
