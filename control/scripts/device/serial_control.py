import logging
from typing import Dict, Tuple

from .serial.serial_device import parse_on_off_control_args, SerialDevice
from ..configs.config import RedisDBEnum, get_value, set_value


logger = logging.getLogger('serial')


def init_dut_state(serial_device: SerialDevice) -> Tuple[str, str, str]:
    hardware_configuration = get_value('hardware_configuration', db=RedisDBEnum.hardware)
    power_state = parse_on_off_control_args(hardware_configuration.get('enable_dut_power'))
    hdmi_state = parse_on_off_control_args(hardware_configuration.get('enable_hdmi'))
    wan_state = parse_on_off_control_args(hardware_configuration.get('enable_dut_wan'))
    serial_device.set_packet(vac=power_state, hpd=hdmi_state, lan=wan_state)
    return power_state, hdmi_state, wan_state


def change_dut_state(serial_device: SerialDevice, args: Dict[str, str]):
    power_state = args.get('enable_dut_power')
    hdmi_state = args.get('enable_hdmi')
    wan_state = args.get('enable_dut_wan')

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

    serial_device.set_packet(**packet_dict)
