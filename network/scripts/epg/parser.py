from collections import namedtuple
from typing import Tuple, Generator, List

from pypacker import ppcap

from .utils import check_base_info, check_ipv4, convert_ip_bytes_string, parse_pcap_file


ChannelInfo = namedtuple("ChannelInfo", ["channel_id",
                                         "channel_name",
                                         "channel_number",
                                         "ip_port",
                                         "provider",
                                         "region_id"])


def FilterEPGPacket(reader: ppcap.Reader, epg_server_ip: str = '') -> Generator:
    """
    패킷 바이트 Reader에서 패킷을 하나씩 읽어, ipv4 체크, udp 체크, payload 1316 bytes length 체크 후 yield
    만약 epg_server_ip 를 특정한다면 해당 ip만 yield
    """
    for _, buffer in reader:
        iptype, protocol, ip_total_legnth = check_base_info(buffer)
        if iptype == b'\x08\x00' and protocol == 0x11 and ip_total_legnth == 1344 or ip_total_legnth == 1356:
            # ipv4 = 2048 / udp = 0x11 = 17 / 42 + 1316 length
            # ethernet layer : 14 bytes
            # ipv4 layer: 20 bytes
            # udp layer: 8 bytes
            # payload: 188 * 7 = 1316 bytes
            # total: 14 + 20 + 8 + 1316 = 1358, ip_total -> 20 + 8 + 1316 = 1344
            if epg_server_ip and check_ipv4(epg_server_ip) and not convert_ip_bytes_string(buffer[30:34]) == epg_server_ip:
                # ip is epg_server_ip. if epg_server_ip is None or not valid ipv4 format, all 1358 bytes ipv4 udp packet is parsed.
                pass
            else:
                yield buffer
        else:
            pass


def FormatEGPPacket(packet_stream: Generator) -> Generator:
    """
    한 패킷 내의 7개의 188 bytes 데이터를 데이터 헤더로 분리해서 아래와 같이 yield
    여기서 header continuous count 를 체크할 수 있지만, 불필요하다 판단하여 하지 않음.
    """
    # iso_iec_13818_1_bytes = 188 bytes
    for buffer in packet_stream:
        buffer = buffer[12:] if len(buffer) == 1356 else buffer
        for i in range(7):
            yield buffer[42 + 188 * i: 42 + 188 * (i+1)]


def MergeEPGPacket(iso_iec_13818_1_bytes_stream: Generator):
    """
    EPG 데이터는 iso_iec_13818_1 188 bytes 데이터 안에 여러 패킷에 걸쳐서 저장되어 있음
    0x47 로 헤더로 시작하는 데이터에 길이가 정의되어 있으므로, 해당 길이만큼 다음 패킷 까지 읽은 뒤에
    channel_info_bytes 만들어서 yield
    """
    length_remainder = -1
    valid_block = False
    for packet_sub_block in iso_iec_13818_1_bytes_stream:
        # 0x47: packet epg 정보                                # 0x11: TV 관련
        if packet_sub_block[0] != 0x47 or packet_sub_block[2] != 0x11:
            continue
        # 0x42 group start
        if packet_sub_block[5] == 0x42 and length_remainder < 0:
            valid_block = True
            repacked_packets = packet_sub_block[5:]
            length_remainder = (packet_sub_block[6] * 256 + packet_sub_block[7] & 0xfff) - len(packet_sub_block[5:])
        else:
            repacked_packets += packet_sub_block[4:]
            length_remainder -= len(packet_sub_block[4:])

        if valid_block and length_remainder < 0:
            channel_info_bytes = repacked_packets[11:]
            yield channel_info_bytes
            repacked_packets = b''
            length_remainder = -1
            valid_block = False
        else:
            pass


def parse_descriptor_tag(packet: bytes) -> Tuple[bytes, bytes, bytes]:
    """
    tag, length 는 2bytes로 저장되어 있고, length 만큼 payload가 순차적으로 쌓여 있는 구조임.
    """
    tag = packet[0]
    length = packet[1]
    payload = packet[2: 2 + length]
    remained_packet = packet[2 + length:]
    return tag, payload, remained_packet


def process_descriptor_tag(dt: dict, channel_info_packet: bytes, descriptors_lop_length: int) -> bytes:
    """
    이 함수는 단순히 channel_info_packet 을 파싱하는게 아니라, 다음 가공을 위해 이미 읽은 데이터를 잘라서 되돌려주는 역할 또한 진행
    """
    start_len = len(channel_info_packet)
    while len(channel_info_packet) > start_len - descriptors_lop_length + 3:
        tag, payload, channel_info_packet = parse_descriptor_tag(channel_info_packet)
        dt[tag] = payload
    return channel_info_packet


def decode_name_bytes(name_bytes: bytes) -> str:
    """
    한국 특성상 cp949 포맷일 수 있음, utf-8 인코딩이 더 일반적이고, cp949 먼저 시도 시 이상한 문자열로 디코딩 될 수도 있음.
    """
    try:
        decoded_name = name_bytes.decode('utf-8')
    except UnicodeDecodeError:
        try:
            decoded_name = name_bytes.decode('cp949')
        except UnicodeDecodeError:
            decoded_name = name_bytes.hex()
    return decoded_name


def ParseEPGPacket(channel_info_packet: bytes) -> Generator:
    """
    머지된 channel_info_packet 에서 채널 정보를 가져옴. 한 channel_info_packet 에는 3~6개의 채널 정보가 들어있으며,
    패킷, 통신사마다 다를 수 있음. 실제 데이터는 여러 패킷에 걸쳐져 있는 형태임.add()
    일부 descriptor_tag는 통신사마다 존재하지 않을 수 있음.
    """
    while len(channel_info_packet) > 10:
        try:
            s_id = channel_info_packet[0] * 256 + channel_info_packet[1]
            descriptors_lop_length = channel_info_packet[3] * 256 + channel_info_packet[4] & 0xfff
            channel_info_packet = channel_info_packet[5:]
            end_packet_check = channel_info_packet[0]
            if end_packet_check != 0x48:
                break

            dt = {}
            channel_info_packet = process_descriptor_tag(dt, channel_info_packet, descriptors_lop_length)
            _, provider, name_data = parse_descriptor_tag(dt[0x48])
            name = name_data[2:]

            s_name = decode_name_bytes(name)
            s_provider = provider[1:].decode('utf-8')
            s_ip = convert_ip_bytes_string(dt[0x80][:4])
            s_port = int.from_bytes(dt[0x80][4:], 'big')
            s_channel = int.from_bytes(dt[0x83], 'big')
            s_area = int.from_bytes(dt[0x85], 'big')

            # s_genre = int(dt84, 16)
            # s_extended_service_descriptor = int(dt90, 16)
            # s_element_stream_descriptor =  int(dt86, 16)

            yield s_id, s_channel, s_provider, s_ip, s_port, s_name, s_area
        except Exception as e:
            print(e)
            pass


def parse_epg_pcapfile(epg_file_name: str, epg_server_ip: str) -> List[ChannelInfo]:
    """
    pcap 파일내 반복적으로 정보가 들어오므로, set으로 중복 체크 후 service_id로 정렬하여 반환.
    """
    raw_channel_list = []
    with parse_pcap_file(epg_file_name) as reader:
        for channel_info_packet in MergeEPGPacket(FormatEGPPacket(FilterEPGPacket(reader, epg_server_ip))):
            raw_channel_list += list(ParseEPGPacket(channel_info_packet))
        channel_list = list(set(raw_channel_list))

    return sorted(channel_list, key=lambda x: x[0])
