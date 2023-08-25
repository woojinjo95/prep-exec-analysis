import logging
import re
import requests

from ..control.command import get_stdout
from ..configs.config import get_value
from ..utils._exceptions import handle_errors
from ..utils.network import check_ipv4, check_ipv6

logger = logging.getLogger('info')


class EthernetState:
    up: str = 'up'
    down: str = 'down'


@handle_errors
def ping_google() -> bool:
    try:
        result = get_stdout('ping 8.8.8.8 -c 1 -w 1')
        connected = '1 received' in result
    except:
        connected = False
    return connected


@handle_errors
def get_ethernet_state(nic: str):
    return get_stdout(f'cat /sys/class/net/{nic}/operstate', log=False).strip()


@handle_errors
def get_private_ip() -> str:
    bridge = get_value('network', 'br_nic', 'br0')

    bridge_ipv4_info = get_stdout(f'ip -4 addr show {bridge}')

    bridge_ipv4 = re.search(r'(?<=inet\s)\d+(\.\d+){3}', bridge_ipv4_info)

    if bridge_ipv4:
        private_ip = bridge_ipv4.group()
    else:
        pass  # use 0.0.0.0

    return private_ip


@handle_errors
def get_public_ip() -> str:
    public_ip = '0.0.0.0'

    # ipv4 시도 -> 모두 실패 시 ipv6 한번 시도 -> 모두 실패 시 공백 처리
    # 고객사 요청으로 public ip를 ipv4로 하는 것임.
    timeout = 3
    default_urls = ['ip.dev-nextlab.com']
    third_party_urls = ['icanhazip.com', 'ifconfig.co', 'checkip.amazonaws.com']
    ip_getter_urls = default_urls + third_party_urls
    for address in ip_getter_urls:
        ip = get_stdout(f'curl -4 -s {address} -m {timeout}').strip()
        if check_ipv4(ip):
            public_ip = ip
            break
    else:
        ip = get_stdout(f'curl -s {ip_getter_urls[0]} -m {timeout}').strip()
        if check_ipv6(ip):
            public_ip = ip
        else:
            pass  # use 0.0.0.0

    return public_ip


@handle_errors
def get_gateway_ips(nic: str):
    return get_stdout(f'ip route show | grep {nic} | awk \'/default/ {{print $3}}\'').strip()


@handle_errors
def get_gateway_mac_address() -> str:
    arp_info = get_stdout('arp _gateway')
    upper_mac_re = re.search(r'ether\s+(?P<mac>.{2}:.{2}:.{2}:.{2}:.{2}:.{2})', arp_info)
    upper_mac = upper_mac_re['mac'] if upper_mac_re else '00:00:00:00:00:00'

    return upper_mac


@handle_errors
def get_detail_ip_info(dump_file_name: str = 'ipinfo.json') -> dict:
    info = JsonManager(dump_file_name)
    info.load()
    result = info.data
    ip = get_public_ip()
    if ip != result.get('ip'):
        # 1k per month requests for free.
        result = {'ip': None, 'city': 'Seoul', 'loc': "37.5602,127.0401", 'country': 'KR', 'line': 'KT'}

        logger.info('Get ip info from 3rd party program')
        res = requests.post('http://ipinfo.io', timeout=5)
        res_result = res.json()
        isp = res_result['org'].lower()
        if 'korea telecom' in isp:
            res_result['line'] = 'KT'
        elif 'sk broadband' in isp:
            res_result['line'] = 'SK'
        elif 'lg powercomm' in isp:
            res_result['line'] = 'LG'
        else:
            if 'kt' in isp:
                res_result['line'] = 'KT'
            elif 'sk' in isp:
                res_result['line'] = 'SK'
            elif 'lg' in isp:
                res_result['line'] = 'LG'
            else:
                res_result['line'] = 'etc'
        result.update(res_result)
        for key, value in result.items():
            info.change(key, value)
        info.save()
    else:
        return result
