from connection.redis_pubsub import unit_publish
from simple_logger import simple_logger


def main():
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'start'}})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'stop'}})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'del', 'packet_block': {'ip': '239.192.41.2'}}})
    unit_publish(payload={
    "msg": "video_frame_snapshot",
    "data": {
				"testrun_id": "",
        "video_path": "/app/workspace/testruns/2023-09-01T065554F133036/raw/videos/video_2023-09-01T155359F255942+0900_240.mp4",
        "relative_time": 3
    }
})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'add', 'packet_block': {'ip': '192.168.100.100', 'port': 3000, 'protocol': 'tcp'}}})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'add', 'packet_block': {'ip': '239.192.41.5', 'port': 3000}}})
    # unit_publish(payload={'msg': 'network_emulation', 'data': {'action': 'add', 'delay': 20}})

if __name__ == '__main__':
    logger = simple_logger('test')
    main()
