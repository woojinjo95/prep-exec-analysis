import logging
import time
from typing import Dict, Tuple

from ..configs.config import get_value
from ..configs.constant import RedisChannel, RedisDBEnum
from ..connection.redis_connection import StrictRedis, hget_value, hset_value
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from .serial.serial_device import SerialDevice, parse_on_off_control_args

logger = logging.getLogger('serial')


HARDWARE_CONFIG = 'hardware_configuration'
DUT_POWER = 'enable_dut_power'
DUT_HDMI = 'enable_hdmi'
DUT_WAN = 'enable_dut_wan'


def init_dut_state(serial_device: SerialDevice) -> Tuple[str, str, str]:
    hardware_configuration = get_value(HARDWARE_CONFIG, db=RedisDBEnum.hardware)
    power_state = parse_on_off_control_args(hardware_configuration.get(DUT_POWER))
    hdmi_state = parse_on_off_control_args(hardware_configuration.get(DUT_HDMI))
    wan_state = parse_on_off_control_args(hardware_configuration.get(DUT_WAN))
    serial_device.set_packet(vac=power_state, hpd=hdmi_state, lan=wan_state)
    return power_state, hdmi_state, wan_state


def change_dut_state(serial_device: SerialDevice, args: Dict[str, str]):
    power_state = args.pop(DUT_POWER, None)
    hdmi_state = args.pop(DUT_HDMI, None)
    wan_state = args.pop(DUT_WAN, None)

    packet_dict = {}
    data = {}

    def assign_state(rc: StrictRedis, state: str, pin_name: str, device_name: str):
        state = parse_on_off_control_args(state)
        packet_dict[pin_name] = state
        prev_state = hget_value(rc, HARDWARE_CONFIG, device_name)
        requested_state = True if state == 'on' else False

        if prev_state == requested_state:
            transition = 'steady'
        elif prev_state is True:
            transition = 'falling'
        else:
            transition = 'rising'

        data[f'{device_name}_transition'] = transition
        hset_value(rc, HARDWARE_CONFIG, device_name, requested_state)

    with get_strict_redis_connection(db=RedisDBEnum.hardware) as rc:
        if power_state is not None:
            assign_state(rc, power_state, 'vac', DUT_POWER)

        if hdmi_state is not None:
            assign_state(rc, hdmi_state, 'hpd', DUT_HDMI)

        if wan_state is not None:
            assign_state(rc, wan_state, 'lan', DUT_WAN)

        if len(args) > 0:
            publish(rc, RedisChannel.command, {'msg': 'on_off_control_response',
                                               'level': 'error',
                                               'data': {'log': f'Devices "{args}" is not supported type'}})

    data.update(packet_dict)

    with get_strict_redis_connection() as rc:
        sensor_time = time.time()
        log = serial_device.set_packet(**packet_dict)
        sensor_time += serial_device.time_offset

        if log == 'ok':
            data.update({'sensor_time': sensor_time})
            payload = {'msg': 'on_off_control_response',
                       'data': data}
        else:
            payload = {'msg': 'on_off_control_response',
                       'level': 'error',
                       'data': {'log': f'Devices "{args}" is not supported type'}}

        publish(rc, RedisChannel.command, payload)
