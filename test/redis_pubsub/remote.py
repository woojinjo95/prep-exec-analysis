from connection.redis_pubsub import unit_publish, Subscribe, get_strict_redis_connection
from connection.redis_connection import hget_value
from simple_logger import simple_logger
import time


def main():
    time.sleep(10)
    for _ in range(3):
        unit_publish(payload={'msg': 'remocon_transmit', 'data': {'key': 'channelup', 'type': 'ir'}})
    time.sleep(10)
    for _ in range(3):
        unit_publish(payload={'msg': 'remocon_transmit', 'data': {'key': 'channeldown', 'type': 'ir'}})
        time.sleep(5)

    unit_publish(payload={'msg': 'remocon_transmit', 'data': {'key': 'exit', 'type': 'ir'}})
    time.sleep(5)

    for key in '*7899#':
        unit_publish(payload={'msg': 'remocon_transmit', 'data': {'key': key, 'type': 'ir'}})

    unit_publish(payload={'msg': 'remocon_transmit', 'data': {'key': 'exit', 'type': 'ir'}})
    time.sleep(15)

    unit_publish(payload={"msg": "on_off_control",
                          "data": {"enable_dut_power": "off"}})
    time.sleep(5)

    unit_publish(payload={"msg": "on_off_control",
                          "data": {"enable_dut_power": "on"}})

    time.sleep(90)

    unit_publish(payload={'msg': 'remocon_transmit', 'data': {'key': 'exit', 'type': 'ir'}})
    time.sleep(5)

if __name__ == '__main__':
    logger = simple_logger('test')
    main()
    # unit_publish(payload={'msg': 'remocon_transmit', 'data': {'key': 'exit', 'type': 'ir'}})
