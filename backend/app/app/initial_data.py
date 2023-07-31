
import logging
import json
import uuid

# from PIL import Image
from app.db.redis_session import RedisClient
from app.crud.base import insert_many_to_mongodb

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


def init_remocon_registration():
    class remocon_code_basic():
        name: str
        hotkey: list
        code: str
        location: [{
            "x1": int,
            "y1": int
            },{
            "x2": int,
            "y2": int
            }
        ]
    class remocon_basic():
        id: str
        name: str
        image_path: str
        image_resolution: {
            "width": int,
            "height": int
        }
        remocon_codes: list[remocon_code_basic]

    with open('/app/app/remocon_ir_preset.json') as f:
        remocons_data = []
        preset_json = json.load(f)
        for remocon_model, codes in preset_json.items():
            remocon = remocon_basic()
            remocon.id = str(uuid.uuid4())
            remocon.name = remocon_model
            # remocon.image_path = f'/app/app/files/image/remocon_image_{remocon_model}.jpg'
            # image_size = Image.open(remocon.image_path).size # 이미지 해상도 계산
            # remocon.image_resolution = {"width":image_size[0], "height":image_size[1]}
            remocon_codes = []
            for preset in codes:
                remocon_code = remocon_code_basic()
                remocon_code.name = preset.get('name', '')
                remocon_code.code = preset.get('pronto_code', '')
                # remocon_code.hotkey = preset.get('', [])
                # remocon_code.location = [{"x1": 1, "y1": 1}, {"x2": 2, "y2": 2}]
                remocon_codes.append(remocon_code.__dict__)
            remocon.remocon_codes = remocon_codes
            remocons_data.append(remocon.__dict__)
        insert_many_to_mongodb(col='remocon', data=remocons_data)
        
            


def init() -> None:
    init_hardware_configuration()
    init_remocon_registration()


def main() -> None:
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
