import logging
import time
from multiprocessing import Event

from ..configs.config import RedisDBEnum, RedisDBField, get_value, set_value
from ..control.network_control.command_executor import traffic_change
from ..info.network_info import (EthernetState, get_ethernet_state,
                                 get_mac_address, get_private_ip)
from ..utils._multi_process import ProcessMaintainer
from .brute_ping import brute_ping_ipv4, ping_to_dst

logger = logging.getLogger('info')
TIMEOUT = 0.02    # in second
STABLE_DELAY = 5  # in second
UNIT_DELAY = 0.01  # in second


def get_dut_ip() -> str:
    return get_value(RedisDBField.hardware_config, 'dut_ip', '', db=RedisDBEnum.hardware)


def get_dut_mac() -> str:
    return get_value(RedisDBField.hardware_config, 'dut_mac', '', db=RedisDBEnum.hardware)


def get_dut_power_state():
    return get_value(RedisDBField.hardware_config, 'enable_dut_power', '', db=RedisDBEnum.hardware)


def set_dut_ip(dut_ip: str):
    set_value(RedisDBField.hardware_config, 'dut_ip', dut_ip, db=RedisDBEnum.hardware)


def set_dut_mac(dut_mac: str):
    set_value(RedisDBField.hardware_config, 'dut_mac', dut_mac, db=RedisDBEnum.hardware)


def set_dut_net_state(state: bool):
    set_value(RedisDBField.hardware_config, 'dut_net_state', state, db=RedisDBEnum.hardware)


def stb_ip_finder(stop_event: Event, run_state_event: Event):
    logger.info('stb ip finder start')
    stb_nic = get_value('network', 'stb_nic')
    prev_state = EthernetState.down
    index = 0

    while not stop_event.is_set():
        # 현재 상태 및 저장된 상태
        # dut ip는 외부에서 ''로 만들면 강제로 업데이트하는 이벤트로 사용하기 위함, 즉 dut_ip를 공백으로 만들면 확인 과정을 수행
        current_state = get_ethernet_state(stb_nic)
        dut_ip = get_dut_ip()

        if current_state == EthernetState.up:
            # 물리적 연결 상태가 되면 표시
            set_dut_net_state(True)
            if dut_ip == '' or prev_state == EthernetState.down:
                # 현재 ip가 없거나 rising edge일 경우 ip 확인 과정 시작
                private_ip = get_private_ip()
                logger.info(f'New stb nic conection detected! wait {STABLE_DELAY} seconds for stable connection')
                # 물리적인 연결이 생기더라도 실제 IP를 받는 데에 시간이 소요되므로, 약간의 대기작업
                time.sleep(STABLE_DELAY)

                original_delay = get_value('hardware_configuration', 'packet_delay', db=RedisDBEnum.hardware)
                bridge = get_value('network', 'br_nic', 'br0')

                # emulation을 적용하여 해당 영향을 받는 유일한 ip 가 바로 dut에 연결된 ip
                original_ip_values = brute_ping_ipv4(private_ip, timeout=TIMEOUT, interface=bridge)
                traffic_change(nic=stb_nic, delay=original_delay + UNIT_DELAY * 1000)
                augmented_ip_values = brute_ping_ipv4(private_ip, timeout=TIMEOUT, interface=bridge)
                traffic_change(nic=stb_nic, delay=original_delay)

                for ip, ping_value in list(augmented_ip_values.items())[::-1]:
                    if ping_value - original_ip_values.get(ip, TIMEOUT) > UNIT_DELAY * 0.9:
                        dut_ip = ip
                        dut_mac = get_mac_address(dut_ip)
                        set_dut_ip(dut_ip)
                        set_dut_mac(dut_mac)
                        logger.info(f'STB: {dut_ip} / {dut_mac}')
                        break
                else:
                    logger.error('Failed to find STB. maybe STB is not reachable')

                logger.debug(f'Result: {original_ip_values} / {augmented_ip_values}')
            else:
                # 보조 로직: 100회 주기로 ip와 mac 비교로 잘못된 값을 가져왔는지 체크
                # 0.5초 안에 물리적 up/down 상태가 변경되거나, 물리적 변경 없이 mac, ip가 변경될 경우에 동작함
                # 일반적인 경우가 아니므로 대략 1분 정도의 주기로만 체크
                if index > 100:
                    index = 0
                    if get_mac_address(get_dut_ip()) != get_dut_mac():
                        logger.warning('Mac address unmatched and get ip stb mac again')
                        set_dut_ip('')

                    if ping_to_dst(get_dut_ip()) == 0:
                        logger.warning('IP not respond even physical connection is live')
                        set_dut_ip('')

        else:
            set_dut_net_state(False)
            if get_dut_power_state():
                # 만약 사용자가 의도적으로 power_off를 했을 때 값이 날아가지 않도록 하는 설정
                dut_ip = ''
                set_dut_ip(dut_ip)

        prev_state = current_state
        index += 1
        time.sleep(0.5)


def stb_ip_finder_process() -> ProcessMaintainer:
    process = ProcessMaintainer(func=stb_ip_finder, daemon=False, revive_interval=1)
    process.start()
    return process
