import re
import ipaddress
from collections import defaultdict

import psutil

from ..configs.config import RedisDBEnum, get_value
from ..utils._exceptions import handle_errors, handle_none_return
from ..utils._subprocess import get_output

HARDWARE_CONFIG = 'hardware_configuration'
COMMON = 'common'
TESTRUN_CONFIG = 'testrun'


def percent_round(value: float, ndigits: int = 1) -> float:
    return round(value, ndigits=ndigits)


@handle_none_return(float)
@handle_errors
def get_representive_temperature() -> float:
    milidegreecelcius = get_output('cat /sys/class/thermal/thermal_zone*/temp')
    types = get_output('cat /sys/class/thermal/thermal_zone*/type')

    for _type, milidegree in zip(types.split(), milidegreecelcius.split()):
        if _type == 'x86_pkg_temp':
            x86_pkg_temp_milidegreecelcius = milidegree
            break
    else:
        x86_pkg_temp_milidegreecelcius = max(milidegreecelcius.split())

    '''
    /sys/class/thermal/thermal_zone0/type = x86_pkg_temp
    x86_pkg_temp_milidegreecelcius = '87000'
    '''
    x86_pkg_temp = int(x86_pkg_temp_milidegreecelcius) / 1000
    return x86_pkg_temp


@handle_none_return(dict)
@handle_errors
def get_sensors_temperture() -> dict:
    sensors_output = get_output('sensors | grep :')
    '''
    위 x86_pkg_temp 와 아래 Package id 0 는 같은 값으로 볼 수 있으므로,
    이 함수는 정의는 하나 사용하지 않음.

    sensors_output = 
    Adapter: ISA adapter
    Package id 0:  +31.0°C  (high = +100.0°C, crit = +100.0°C)
    Core 0:        +30.0°C  (high = +100.0°C, crit = +100.0°C)
    Core 1:        +29.0°C  (high = +100.0°C, crit = +100.0°C)
    Adapter: ISA adapter
    cpu_fan:     6553500 RPM
    temp1:       +6280.4°C  
    Adapter: ACPI interface
    temp1:        +27.8°C  (crit = +119.0°C)
    Adapter: ISA adapter
    VCORE_Voltage:  67.00 mV 
    VMEM_Voltage:    1.19 V  
    +12_Voltage:    12.22 V  
    5VSB_Voltage:    5.00 V  
    SYS1_FAN:      6341 RPM
    CPU_Temp:       +32.0°C  
    SYS1_Temp:      +29.0°C  
    SYS2_Temp:      +28.0°C  
    Adapter: Virtual device
    temp1:        +31.0°C  
    '''
    lines = sensors_output.strip().split("\n")
    current_adapter = None
    sensor_values = defaultdict(dict)

    for line in lines:
        if "Adapter:" in line:
            current_adapter = line.split(":")[1].strip().lower().replace(" ", "_")
        else:
            match = re.search(r"(.+):\s+\+(\d+\.?\d*)", line)
            if match:
                sensor, temperature = match.groups()
                sensor = sensor.strip().lower().replace(" ", "_")
                temperature = float(temperature)
                sensor_values[current_adapter][sensor] = temperature

    return sensor_values


@handle_none_return(str)
@handle_errors
def get_machine_private_ip() -> str:
    private_ip = get_value(HARDWARE_CONFIG, 'private_ip', '0.0.0.0', db=RedisDBEnum.hardware)
    return private_ip


@handle_none_return(str)
@handle_errors
def get_machine_dut_lan_ip() -> str:
    dut_ip = get_value(HARDWARE_CONFIG, 'dut_ip', '0.0.0.0', db=RedisDBEnum.hardware)
    return dut_ip


@handle_none_return(float)
@handle_errors
def get_cpu_usage_average_in_percent() -> float:
    cpu_usage_in_percent = psutil.cpu_percent()
    return percent_round(cpu_usage_in_percent)


@handle_none_return(float)
@handle_errors
def get_memory_usage_in_percent() -> float:
    memory_usage_in_percent = psutil.virtual_memory().percent
    return percent_round(memory_usage_in_percent)


@handle_none_return(float)
@handle_errors
def get_disk_usage_in_percent() -> float:
    workspace_path = get_value(TESTRUN_CONFIG, 'workspace_path', db=RedisDBEnum.hardware)
    disk_usage_in_percent = psutil.disk_usage(workspace_path).percent
    return percent_round(disk_usage_in_percent)


@handle_none_return(str)
@handle_errors
def get_current_running_state() -> str:
    try:
        ipaddress.ip_address(get_machine_private_ip())  # machine itself
        ipaddress.ip_address(get_machine_dut_lan_ip())  # stb connection
        state = get_value(COMMON, 'service_state', '0.0.0.0', db=RedisDBEnum.hardware)

        if state.lower() in ('streaming', 'playblock'):
            return 'Collecting'

        elif state.lower() in ('analyzing', 'recording'):
            return 'Analyzing'

        else:
            # state in ('idle')
            return 'Ready'

    except ValueError:
        return 'Check Connection'
