def check_valid_multicast_ip(ip_bytes: bytes) -> bool:
    if len(ip_bytes) < 3:
        # not regular packet
        return False

    if not (224 <= ip_bytes[0] <= 239):
        # The multicast addresses are in the range 224.0.0.0 through 239.255.255.255.
        return False

    elif ip_bytes[0] == 224 and ip_bytes[1] == 0 and ip_bytes[2] == 0:
        # The range of addresses between 224.0.0.0 and 224.0.0.255, inclusive,
        # is reserved for the use of routing protocols and other low-level
        # topology discovery or maintenance protocols, such as gateway discovery
        # and group membership reporting.
        return False

    elif ip_bytes[0] == 232:
        # Reserved for use with the SSM datagram delivery model where data 
        # is forwarded only to receivers that have explicitly joined the group.
        return False

    elif ip_bytes[0] == 239 and ip_bytes[1] == 255 and ip_bytes[2] == 255 and ip_bytes[3] == 250:
        # 239.255.255.250
        # This address is used for UPnP (Universal Plug and Play)/SSDP (Simple Service Discovery Protocol)
        # by various vendors to advertise the capabilities of (or discover) devices on a VLAN. MAC OS,
        # Microsoft Windows, IOS and other operating systems and applications use this protocol.
        return False

    return True
