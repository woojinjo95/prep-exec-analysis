import logging

from app.core.config import settings
from app.crud.base import (insert_many_to_mongodb, insert_one_to_mongodb,
                           load_one_from_mongodb)
from app.db.redis_session import RedisClient
from app.remocon_ir_preset import remocon_preset
from app.schemas.enum import (RemoteControlTypeEnum,
                              ResumeMeasurementRecognizingKeyEventEnum)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_hardware_configuration():
    config = RedisClient.hget(name=f'hardware_configuration',
                              key='remote_control_type')
    if not config:
        configs = {'remote_control_type': RemoteControlTypeEnum.ir.value,
                   'enable_dut_power': 'True',
                   'enable_hdmi': 'True',
                   'enable_dut_wan': 'True',
                   'enable_network_emulation': 'True',
                   'packet_bandwidth': 0,
                   'packet_delay': 0.0,
                   'packet_loss': 0.0}
        for k, v in configs.items():
            RedisClient.hset(f'hardware_configuration', k, v)


def init_scenario():
    scenario = load_one_from_mongodb('scenario', {"_id": 1})
    if scenario is None:
        insert_one_to_mongodb(col='scenario', data={"block_group": []})


def init_remocon_registration():
    remocons_data = remocon_preset(settings.REMOCON_COMPANY.split(','))
    if remocons_data != []:
        insert_many_to_mongodb(col='remocon', data=remocons_data)


def init_analysis_config():
    config = {
        "freeze": {
            "duration": 0,
            "save_video": True,
            "before_occurrence": 0,
            "after_occurrence": 0
        },
        "macroblock": {
            "save_video": True,
            "before_occurrence": 0,
            "after_occurrence": 0
        },
        "resume": {
            "recognizing_key_event": ResumeMeasurementRecognizingKeyEventEnum.power.value,
            "save_video": True,
            "before_occurrence": 0,
            "after_occurrence": 0,
            "frames": []
        },
        "boot": {
            "save_video": True,
            "before_occurrence": 0,
            "after_occurrence": 0,
            "frames": []
        },
        "channel_change_time": {
            "targets": [],
            "save_video": True,
            "before_occurrence": 0,
            "after_occurrence": 0
        },
        "log_level_finder": {
            "targets": []
        }
    }
    analysis_config = load_one_from_mongodb('analysis_config', {"_id": 1})
    if analysis_config is None:
        insert_one_to_mongodb(col='analysis_config', data=config)


def init() -> None:
    init_hardware_configuration()
    init_scenario()
    init_remocon_registration()
    init_analysis_config()


def main() -> None:
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
