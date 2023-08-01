
import logging
import uuid

from app.crud.base import insert_to_mongodb, load_one_from_mongodb
from app.db.redis_session import RedisClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_hardware_configuration():
    config = RedisClient.hget(name=f'hardware_configuration',
                              key='remote_control_type')
    if not config:
        configs = {'remote_control_type': 'ir',
                   'enable_dut_power': 'True',
                   'enable_hdmi': 'True',
                   'enable_dut_wan': 'True',
                   'enable_network_emulation': 'True',
                   'packet_bandwidth': 1000,
                   'packet_delay': 0.0,
                   'packet_loss': 0.0}
        for k, v in configs.items():
            RedisClient.hset(f'hardware_configuration', k, v)


def init_scenario():
    scenario = load_one_from_mongodb('scenario', {"_id": 1})
    if scenario is None:
        insert_to_mongodb(col='scenario', data={"block_group": []})


def init() -> None:
    init_hardware_configuration()
    init_scenario()


def main() -> None:
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
