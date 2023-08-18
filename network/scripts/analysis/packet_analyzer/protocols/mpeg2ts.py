# TS_ERROR_BIN = 0b1 << 3
# PAYLOAD_START_BIN = 0b1 << 2
# TS_PRIORITY_BIN = 0b1 << 1
PID_BIN = 0b1111111111111
TS_SCRAMBLE_BIN = 0b11 << 6
ADAPDATION_BIN = 0b11 << 4
CC_BIN = 0b1111


def iso_iec_13818_1_format(iso_iec_13818_1_bytes: bytes):
    '''
    Header bytes example: b"G\x03\xe9\x14"
    0x47 <= b"\x47" = b"G" (ord('G') = 71) 
    0x03 <= b"\x03" = 3
    0xe9 <= b"\xe9" = 233
    0x14 <= b"\x14" = 20

    Header: 0x4703e914
     0x4  0x7  0x0  0x3  0xe  0x9  0x1  0x4
    0100 0111 .... .... .... .... .... .... = Sync Byte: 0x47 == mpeg2ts header
    .... .... 0... .... .... .... .... .... = Transport Error Indicator: 0
    .... .... .0.. .... .... .... .... .... = Payload Unit Start Indicator: 0
    .... .... ..0. .... .... .... .... .... = Transport Priority: 0
    .... .... ...0 0011 1110 1001 .... .... = PID: Unknown (0x03e9)
    .... .... .... .... .... .... 00.. .... = Transport Scrambling Control: Not scrambled (0b00)
    .... .... .... .... .... .... ..01 .... = Adaptation Field Control: Payload only (0b01)
    .... .... .... .... .... .... .... 0100 = Continuity Counter: 4 (0b0100)
    '''
    header_bytes = iso_iec_13818_1_bytes[:4]
    sync_byte = header_bytes[0]
    # ts_error = (indicators & TS_ERROR_BIN) >> 23
    # payload_start = (indicators & PAYLOAD_START_BIN) >> 22
    # ts_priority = (indicators & TS_PRIORITY_BIN) >> 21
    pid = (header_bytes[1] * 256 + header_bytes[2]) & PID_BIN
    ts_scramble = (header_bytes[3] & TS_SCRAMBLE_BIN) >> 6
    adaptation = (header_bytes[3] & ADAPDATION_BIN) >> 4
    cc = (header_bytes[3] & CC_BIN)

    return (sync_byte, pid, ts_scramble, adaptation, cc, iso_iec_13818_1_bytes)


def mpeg2_ts_parser(packet_bytes: bytes):
    rtp_sequence_num = -1
    try:
        ip = packet_bytes[30:34]
        payload = packet_bytes[42:]
        len_payload = len(payload)

        if len_payload < 1316:
            return ip, (-1, None)
        elif len_payload == 1328:  # 12 + 7 * 188:
            rtp_diagram = payload[:12]
            rtp_sequence_num = rtp_diagram[2] * 0x100 + rtp_diagram[3] if rtp_diagram[1] == 0x21 else -1
            mpeg_ts_7 = payload[12:]
        elif len_payload == 1316:  # 7 * 188
            mpeg_ts_7 = payload
        else:
            return ip, (-1, None)

        pid_values = (iso_iec_13818_1_format(mpeg_ts_7[0:188]),
                      iso_iec_13818_1_format(mpeg_ts_7[188:376]),
                      iso_iec_13818_1_format(mpeg_ts_7[376:564]),
                      iso_iec_13818_1_format(mpeg_ts_7[564:752]),
                      iso_iec_13818_1_format(mpeg_ts_7[752:940]),
                      iso_iec_13818_1_format(mpeg_ts_7[940:1128]),
                      iso_iec_13818_1_format(mpeg_ts_7[1128:1316]))
        return ip, (rtp_sequence_num, pid_values)

    except:
        return ip, (rtp_sequence_num, None)  # not ts file
