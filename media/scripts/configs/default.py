from ..connection.redis_connection import (get_strict_redis_connection,
                                           hget_value, hset_value)
from .constant import RedisDBEnum

settings = {'capture': {'video_device': '/dev/video0',
                        'audio_device': 'hw:1',
                        'width': 1920,
                        'height': 1080,
                        'fps': 60,
                        'audio_gain': 90, },
            'streaming': {'rtsp_publish_url': 'localhost',
                          'rtsp_publish_port': 8554,
                          'streaming_url': 'localhost',
                          'webrtc_port': 8889,
                          'hls_port': 8888,
                          'streaming_name': 'live',
                          'width': 960,
                          'height': 540,
                          'fps': 30,
                          'crf': 30, },
            'recording': {'crf': 23,
                          'rotation_interval': 1800,
                          'segment_interval': 10,
                          'real_time_video_path': 'real_time_videos'},
            'state': {'streaming': 'idle'},
            'common': {'root_file_path': './data'},
            'test': {'description': '''publish command '{"msg": "streaming", "data": {"action": "start"}}'
publish command '{"msg": "recording", "data": {"interval": 1800}}' ''', },
            }

hardware_settings = {'hardware_configuration': {'ssh_port': 2345}}


def initialize_keys(db: int, settings: dict):
    with get_strict_redis_connection(db) as con:
        for key, fields in settings.items():
            for field, value in fields.items():
                if hget_value(con, key, field) is None:
                    hset_value(con, key, field, value)


def init_configs():
    initialize_keys(RedisDBEnum.hardware, hardware_settings)
    initialize_keys(RedisDBEnum.media, settings)
