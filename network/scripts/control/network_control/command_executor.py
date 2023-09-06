import logging


from typing import Dict

from ...configs.config import get_value
from ..command import get_stdout
from ...utils.network import check_ipv4
from .value_rules import check_bandwidth, check_delay, check_percent, check_port, DefaultValues

logger = logging.getLogger('network_control')


def traffic_clear(nic: str):
    get_stdout(f'tc qdisc del dev {nic} root')


def traffic_init(nic: str):
    max_bandwidth = DefaultValues.bandwidth    # Mbps
    target_bandwidth = max_bandwidth  # Mpbs

    '''
    htb 구조로 인해, 1과 1:1이 두번 정의됨.
    먼저 root 아래 class 한개가 정의되고, 해당 클래서에서 leaf 2개가 각각 정의
    하나는 QoS, 하나는 delay, loss, corrupt, duplicate 항.
    '''

    handle = f'tc qdisc add dev {nic} handle 1: root htb default 11'
    class1 = f'tc class add dev {nic} parent 1: classid 1:1 htb rate {max_bandwidth}Mbit'
    class1_1 = f'tc class add dev {nic} parent 1:1 classid 1:11 htb rate {target_bandwidth}Mbit'
    class2 = f'tc qdisc add dev {nic} parent 1:11 handle 2: netem delay 0ms'

    command_lines = [handle, class1, class1_1, class2]  # , mirror_qdisc, mirror_tcp, mirror_udp, mirror_icmp]
    for command in command_lines:
        get_stdout(command)


def traffic_change(nic: str, bandwidth: float = None, delay: any = None,
                   loss: float = None, duplicate: float = None, corrupt: float = None) -> Dict:
    '''
    reorder는 delay option이 필수라서 일단 제외, 추가 가능
    각각의 corelation 등을 설정할 수 있으나 일단 생략.
    '''
    logger.info(f'{nic} -> {bandwidth} / {delay} / {loss}')

    result = {}

    class1_1 = None
    if bandwidth is not None and check_bandwidth(bandwidth):
        bandwidth = bandwidth
        class1_1 = f'tc class change dev {nic} parent 1:1 classid 1:11 htb rate {bandwidth}Mbit'
        result['bandwidth'] = bandwidth

    if class1_1 is not None:
        get_stdout(class1_1)

    class2 = f'tc qdisc change dev {nic} parent 1:11 handle 2: netem '
    class2_args = []

    if delay is not None and check_delay(delay):
        if type(delay) == float or type(delay) == int:
            class2_args.append(f'delay {delay}ms')
        else:
            # mutliple args for delay
            class2_args.append(f'delay {delay}')
        result['delay'] = delay

    if loss is not None and check_percent(loss):
        class2_args.append(f'loss {loss}%')
        result['loss'] = loss

    if corrupt is not None and check_percent(corrupt):
        class2_args.append(f'corrupt {corrupt}%')
        result['corrupt'] = corrupt

    if duplicate is not None and check_percent(duplicate):
        class2_args.append(f'loss {duplicate}%')
        result['duplicate'] = duplicate

    if len(class2_args) > 0:
        get_stdout(class2 + ' '.join(class2_args))

    return result


def ebtables_clear():
    get_stdout('ebtables -F')


def ebtables_init(nic: str):
    wan = get_value('network', 'wan_nic')
    get_stdout(f'ebtables -A FORWARD -i {wan} -o {nic} -j ACCEPT')
    get_stdout(f'ebtables -A FORWARD -i {nic} -o {wan} -j ACCEPT')


def ebtables_block(nic: str, ip: str = None, port: int = None, protocol: str = None, filter_type: str = 'dst', command: str = 'set') -> dict:
    result = {'protocol': protocol}
    wan = get_value('network', 'wan_nic')

    if command in ('add', 'set', 1):
        command = 'I'
        priority = '1'
    else:
        command = 'D'
        priority = ''

    if filter_type in ('dst', 'destination'):
        filter_type = 'destination'
    else:
        filter_type = 'source'

    command_line = f'ebtables -{command} FORWARD {priority} -i {wan} -o {nic} -p ip'

    if ip is not None:
        if check_ipv4(ip):
            result['ip'] = ip
            command_line += f' --ip-{filter_type} {ip}'
        else:
            logger.warning(f'{ip} is not valid for ip')

    if port is not None:
        if check_port(port):
            result['port'] = port
            command_line += f' --ip-{filter_type}-port {port}'
        else:
            logger.warning(f'{port} is not valid for port')

    protocol = protocol.lower()
    if protocol == 'udp':
        command_lines = [command_line + f' --ip-protocol udp -j DROP']
    elif protocol == 'tcp':
        command_lines = [command_line + f' --ip-protocol tcp -j DROP']
    else:
        command_lines = [command_line + f' --ip-protocol udp -j DROP',
                         command_line + f' --ip-protocol tcp -j DROP']

    for command in command_lines:
        get_stdout(command)

    return result
