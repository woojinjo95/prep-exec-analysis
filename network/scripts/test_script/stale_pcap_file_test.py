import sys

sys.path.append('../')

from scripts.capture.parser import get_stale_pcap_chunck_files
from scripts.analysis.packet_analyzer import pprint_stream_dict, pprint_archived_stream_dict, read_pcap_and_update_dict, init_archived_stream_dict
from simple_logger import simple_logger

logger = simple_logger('analysis')
simple_logger('capture')


def main() -> tuple:
    stream_dict = {}
    archived_stream_dict = init_archived_stream_dict()
    # archived_stream_dict = None
    for path in get_stale_pcap_chunck_files():
        read_pcap_and_update_dict(stream_dict, path, archived_stream_dict)
    return stream_dict, archived_stream_dict


if __name__ == '__main__':
    import sys
    import time
    from glob import glob
    s = time.time()

    # path = 'iptv_normal.pcap' if len(sys.argv) < 2 else sys.argv[1]
    stream_dict, archived_stream_dict = main()
    # stream_dict = main('iptv_permill_loss.pcap')
    # stream_dict = main('iptv_half_bandwidth.pcap')
    pprint_stream_dict(stream_dict)
    # print(stream_dict)
    logger.info(f'elased: {time.time() - s}')

    print('\n\n===== same channel archived =====\n\n')
    pprint_archived_stream_dict(archived_stream_dict)