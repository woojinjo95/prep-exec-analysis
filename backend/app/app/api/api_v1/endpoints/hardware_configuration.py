import logging

from app import schemas
from app.db.redis_session import RedisClient
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


def converted_data(data_str):
    try:
        converted_data = float(data_str)
        if converted_data.is_integer():
            return int(converted_data)
        return converted_data
    except ValueError:
        try:
            converted_data = str(data_str)
            return converted_data
        except ValueError:
            try:
                converted_data = bool(data_str)
                return converted_data
            except ValueError:
                return data_str


@router.put("", response_model=schemas.Msg)
def update_hardware_configuration(
    *,
    hardware_configuration_in: schemas.HardwareConfigurationUpdate,
) -> schemas.Msg:
    """
    Update a hardware_configuration.
    """
    for key, val in jsonable_encoder(hardware_configuration_in).items():
        if val is not None:
            RedisClient.hset('hardware_configuration', key, str(val))
    return {'msg': 'Update a hardware_configuration'}


@router.get("", response_model=schemas.HardwareConfigurationBase)
def read_hardware_configuration():
    """
    Retrieve hardware_configuration.
    """
    hardware_configuration = RedisClient.hgetall(f'hardware_configuration')
    config = {field: converted_data(value)
              for field, value in hardware_configuration.items()}

    ip_limit_list = []
    matching_keys = RedisClient.scan_iter(
        match="hardware_configuration_ip_limit:*")
    for key in matching_keys:
        res = RedisClient.hgetall(key)
        ip_limit_list.append({
            'id': key.split(':')[1],
            'ip': res.get('ip', ''),
            'port': res.get('port', ''),
            'type': res.get('type', ''),
            'created_at': float(res.get('created_at', '')),
        })
    config['ip_limit'] = ip_limit_list
    return {'items': config}


#  등록로직
configs = {'remote_control_type': 'IR',
           'enable_dut_power': 'True',
           'enable_hdmi': 'True',
           'enable_dut_wan': 'True',
           'enable_network_emulation': 'True',
           'packet_bandwidth': 1000,
           'packet_delay': 0.0,
           'packet_loss': 0.0}
for k, v in configs.items():
    RedisClient.hset(f'hardware_configuration', k, v)

result = []
matching_keys = RedisClient.scan_iter(
    match="hardware_configuration_ip_limit:*")
for key in matching_keys:
    res = RedisClient.hgetall(key)
    result.append({
        'id': key.split(':')[1],
        'ip': res.get('ip', ''),
        'port': res.get('port', ''),
        'type': res.get('type', ''),
    })
