import socket
import struct
import time
from typing import Tuple

from pypacker import ppcap
from pypacker.layer12 import ethernet
from pypacker.layer3 import ip as ipv4
from pypacker.layer4 import udp

from .utils import GIGA, MTU, get_default_gateway_address, get_nic_mac_dict, get_nic_connected_to_gateway, get_hw_address, convert_mac_to_bytes

"""
실제로 패킷을 캡쳐하는 것이 아니라, payload 및 하위 네트워크 환경을 적절히 확인 후 만들어낸 패킷이므로, 실제 캡쳐된 정보와 다를 수 있음
layer 3 이상은 높은 확률로 일치하지만, 12 단계는 멀티 게이트웨이 환경에서 보장할 수 없음
layer 3, layer4 는 socket 라이브러리 및 대상 값이므로 올바른 경로라면 맞음
payload는 실제 캡쳐보다 더 확실함
"""


def get_src_dst_mac() -> Tuple[str, str]:
    """
    통신 시 가장 가능성이 높은 src, dst mac을 반환하는 함수로, 실패 시 아래와 같이 임의의 mac을 반환.
    """
    try:
        default_gateway_address = get_default_gateway_address()
        src_mac = convert_mac_to_bytes(get_hw_address(default_gateway_address))
        dst_mac = convert_mac_to_bytes(get_nic_mac_dict()[get_nic_connected_to_gateway(default_gateway_address)])
    except:
        src_mac, dst_mac = b'\x00\x11\x22\x33\x44\x55', b'\x66\x77\x88\x99\xaa\xbb'

    return src_mac, dst_mac


def join_multicast_and_dump_pcap(ip: str, port: int, duration: float = 0.5, name: str = ''):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(duration)

        sock.bind((ip, port))
        mreq = struct.pack("4sl", socket.inet_aton(ip), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        start_time = time.time()
        with ppcap.Writer(filename=name, linktype=ppcap.DLT_EN10MB, timestamp=time.time()) as pwriter:
            while time.time() < start_time + duration:
                ts = time.time() * GIGA
                buffer, address = sock.recvfrom(MTU)
                buffer_ip, buffer_port = address

                src, dst = get_src_dst_mac()

                eth_header = ethernet.Ethernet(src=src, dst=dst, type=ethernet.ETH_TYPE_IP)
                ipv4_header = ipv4.IP(src_s=buffer_ip, dst_s=ip)
                udp_header = udp.UDP(sport=port, dport=buffer_port)
                packet = eth_header + ipv4_header + udp_header + buffer
                pwriter._timestamp = ts 
                pwriter.write(packet.bin())


if __name__ == '__main__':
    join_multicast_and_dump_pcap('239.192.60.43', 49200, 2, 'test.pcap')
