import logging

from app.core.config import settings
from app.db.redis_session import RedisClient
from app.remocon_ir_preset import remocon_preset
from app.schemas.enum import (BootTypeEnum, ChannelChangeTimeTargetEnum,
                              RemoteControlTypeEnum,
                              ResumeRecognizingKeyEventEnum, ResumeTypeEnum)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    remocon_preset(settings.REMOCON_COMPANY.split(','))
    configs = {
        'hardware_configuration': {
            'remote_control_type': RemoteControlTypeEnum.ir.value,
            'enable_dut_power': 'True',
            'enable_hdmi': 'True',
            'enable_dut_wan': 'True',
            'enable_network_emulation': 'True',
            'packet_bandwidth': 0,
            'packet_delay': 0.0,
            'packet_loss': 0.0,
        },
        'common': {
            'timezone': 'Asia/Seoul',
        },
        'testrun': {
            'workspace_path': './data/workspace/testruns',
            'dir': 'null',
            'scenario_id': 'null',
        },
        'analysis_config': {
            "freeze": {
                "duration": 0
            },
            "macroblock": {
                "frame_sampling_interval": 0,
                "threshold_score": 0
            },
            "loudness": {},
            "resume": {
                "recognizing_key_event": ResumeRecognizingKeyEventEnum.power.value,
                "type": ResumeTypeEnum.image_matching.value,
            },
            "boot": {
                "type": BootTypeEnum.image_matching.value,
            },
            "channel_change_time": {
                "targets": f'["{ChannelChangeTimeTargetEnum.adjoint_channel.value}"]'
            },
            "log_level_finder": {},
            "log_pattern_matching": {},
            "process_lifecycle_analysis": {},
            "network_filter": {}
        }
    }

    for key, fields in configs.items():
        for field, value in fields.items():
            if key == 'analysis_config':
                _key = f'analysis_config:{field}'
                RedisClient.hsetnx(_key, 'is_active', 'false')
                RedisClient.hsetnx(_key, 'color', '#000000')
                for f, v in value.items():
                    RedisClient.hsetnx(_key, f, v)
            else:
                RedisClient.hsetnx(key, field, value)


def main() -> None:
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
