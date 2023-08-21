from connection.redis_pubsub import unit_publish
from simple_logger import simple_logger


def main():
    unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'stop'}})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'del', 'packet_block': {'ip': '239.192.53.9'}}})


if __name__ == '__main__':
    logger = simple_logger('test')
    main()
