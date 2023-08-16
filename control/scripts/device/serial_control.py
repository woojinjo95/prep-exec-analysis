import logging
from typing import Dict, Tuple

from ..configs.config import get_value, set_value
from ..configs.constant import RedisChannel, RedisDBEnum
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from .serial.serial_device import SerialDevice, parse_on_off_control_args

logger = logging.getLogger('serial')


def init_dut_state(serial_device: SerialDevice) -> Tuple[str, str, str]:
    hardware_configuration = get_value('hardware_configuration', db=RedisDBEnum.hardware)
    power_state = parse_on_off_control_args(hardware_configuration.get('enable_dut_power'))
    hdmi_state = parse_on_off_control_args(hardware_configuration.get('enable_hdmi'))
    wan_state = parse_on_off_control_args(hardware_configuration.get('enable_dut_wan'))
    serial_device.set_packet(vac=power_state, hpd=hdmi_state, lan=wan_state)
    return power_state, hdmi_state, wan_state


def change_dut_state(serial_device: SerialDevice, args: Dict[str, str]):
    power_state = args.pop('enable_dut_power', None)
    hdmi_state = args.pop('enable_hdmi', None)
    wan_state = args.pop('enable_dut_wan', None)

    packet_dict = {}

    if power_state is not None:
        power_state = parse_on_off_control_args(power_state)
        packet_dict['vac'] = power_state
        set_value('hardware_configuration', 'enable_dut_power',
                  'True' if power_state == 'on' else 'False', db=RedisDBEnum.hardware)

    if hdmi_state is not None:
        hdmi_state = parse_on_off_control_args(hdmi_state)
        packet_dict['hpd'] = hdmi_state
        set_value('hardware_configuration', 'enable_hdmi',
                  'True' if hdmi_state == 'on' else 'False', db=RedisDBEnum.hardware)

    if wan_state is not None:
        wan_state = parse_on_off_control_args(wan_state)
        packet_dict['lan'] = wan_state
        set_value('hardware_configuration', 'enable_dut_wan',
                  'True' if wan_state == 'on' else 'False', db=RedisDBEnum.hardware)

    if len(args) > 0:
        with get_strict_redis_connection() as redis_connection:
            publish(redis_connection, RedisChannel.command, {'msg': 'on_off_control_response',
                                                             'level': 'error',
                                                             'data': {'log': f'Devices "{args}" is not supported type'}})

    with get_strict_redis_connection() as redis_connection:
        log = serial_device.set_packet(**packet_dict)

        if log == 'ok':
            payload = {'msg': 'on_off_control_response',
                       'data': packet_dict}
        else:
            payload = {'msg': 'on_off_control_response',
                       'level': 'error',
                       'data': {'log': f'Devices "{args}" is not supported type'}}


        publish(redis_connection, RedisChannel.command, payload)
