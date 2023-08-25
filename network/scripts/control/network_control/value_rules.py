import socket


def check_bandwidth(value: float) -> bool:
    # 0 Mbps ~ 1000 Mbps
    if 0 <= value <= 1000:
        return True
    else:
        False


def check_delay(value: float) -> bool:
    # 0 ms ~ 100,000 ms (0s ~ 100 s)
    if 0 <= value < 100 * 1000:
        return True
    else:
        False


def check_percent(value: float) -> bool:
    # 0 to 100 %
    if 0 <= value <= 100:
        return True
    else:
        return False


def check_port(port_value: any) -> bool:
    if isinstance(port_value, str):
        port_value = port_value.strip("'\"")

    # If it's a port range
    if ":" in str(port_value):
        start_port, end_port = map(int, str(port_value).split(":"))
        return 1 <= start_port < end_port <= 65535

    # If it's a single port
    else:
        port_value = int(port_value)
        return 1 <= port_value <= 65535
