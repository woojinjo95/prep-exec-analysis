import logging

from app.core.config import settings
from app.crud.base import (insert_many_to_mongodb, insert_one_to_mongodb,
                           load_one_from_mongodb)
from app.db.redis_session import RedisClient
from app.remocon_ir_preset import remocon_preset
from app.schemas.enum import RemoteControlTypeEnum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_hardware_configuration():
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
            'stb_connection': 'null'
        },
        'common': {'timezone': 'Asia/Seoul'}
    }

    for key, fields in configs.items():
        for field, value in fields.items():
            if RedisClient.hget(key, field) is None:
                RedisClient.hset(key, field, value)


def init_remocon_registration():
    remocon_preset(settings.REMOCON_COMPANY.split(','))
    logger.info('Remote control preset process completed')


def init() -> None:
    init_hardware_configuration()
    init_remocon_registration()


def main() -> None:
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
