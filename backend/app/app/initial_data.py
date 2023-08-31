import logging

from app.core.config import settings
from app.db.redis_session import RedisClient
from app.remocon_ir_preset import remocon_preset
from app.schemas.enum import RemoteControlTypeEnum

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
            'workspace_path': f'{settings.HOST_PATH}/workspace/testruns',
            'id': 'null',
            'scenario_id': 'null',
        }
    }

    for key, fields in configs.items():
        for field, value in fields.items():
            RedisClient.hsetnx(key, field, value)


def main() -> None:
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
