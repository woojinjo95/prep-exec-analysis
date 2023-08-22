from connection.redis_pubsub import unit_publish
from simple_logger import simple_logger


def main():
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'start'}})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'stop'}})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'del', 'packet_block': {'ip': '239.192.41.2'}}})
    unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'add', 'packet_block': {'ip': '239.192.41.3', 'port': 3000}}})
    unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'add', 'packet_block': {'ip': '192.168.100.100', 'port': 3000, 'protocol': 'tcp'}}})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'add', 'packet_block': {'ip': '239.192.41.5', 'port': 3000}}})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'add', 'delay': 20}})

if __name__ == '__main__':
    logger = simple_logger('test')
    main()
