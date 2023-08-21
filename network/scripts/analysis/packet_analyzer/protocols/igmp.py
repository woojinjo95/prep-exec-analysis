MEMBERSHIP_REPORT = 0x16
LEAVE_GROUP = 0x17


class IGMPConst:
    join = 1
    leave = 0
    none = -1


def igmp_parser(packet_bytes: bytes):
    _type = packet_bytes[38]
    ip = packet_bytes[42:46]
    if _type == MEMBERSHIP_REPORT:
        return ip, IGMPConst.join
    elif _type == LEAVE_GROUP:
        return ip, IGMPConst.leave
    else:
        return ip, IGMPConst.none
