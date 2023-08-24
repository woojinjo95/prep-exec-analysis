from multiprocessing import Pool
import sys
from ping3 import ping


def ping_to_dst(ip: str, timeout: float = 0.1, interface: str = None) -> float:
    try:
        timeout = ping(ip, timeout=timeout, interface=interface) or 0
    except:
        timeout = 0
    finally:
        return (ip, timeout)


# check 255 ip for 0.0.0.0/24
def brute_ping_ipv4(base_ip: str, timeout: float = 3, interface: str = None, pool_size=64) -> float:
    three_octet = base_ip.split('.')[0:3]
    ip_list = ['.'.join(three_octet + [str(fourth_octet)]) for fourth_octet in range(1, 256)]
    ip_list.pop(ip_list.index(base_ip))

    with Pool(pool_size) as pool:
        result = pool.map(ping_to_dst, ip_list)

    result.sort(key=lambda x: x[1])
    return list(filter(lambda x: x[1] != 0, result))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ip_3 = sys.argv[1]
    else:
        ip_3 = '192.168.0'

    ip_list = list()

    for i in range(2, 254):
        ip_list.append(f'{ip_3}.{i}')
    with Pool(20) as p:
        r = p.map(ping_to_dst, ip_list)

    for i in r:
        if i != '':
            print(i)
