from multiprocessing import Pool
import sys
from ping3 import ping


def ping_to_dst(ip: str, timeout: float = 3, interface: str = None) -> float:
    try:
        result = ping(ip, timeout=timeout, interface=interface)
    except:
        result = timeout
    finally:
        if not result:  # if for ''
            result = 0
        return result


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
