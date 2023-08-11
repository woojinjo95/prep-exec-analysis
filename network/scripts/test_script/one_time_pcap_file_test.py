import sys
sys.path.append('../')

from scripts.analysis.packet_analyzer import (init_archived_stream_dict,
                                              pprint_archived_stream_dict,
                                              pprint_stream_dict,
                                              read_pcap_and_update_dict)
from scripts.capture.dumper import start_capture_thread, stop_capture
from scripts.capture.parser import (TCPDUMP, get_completed_pcap_chunck_files,
                                    init_read_path_list)
from simple_logger import simple_logger


logger = simple_logger('analysis')
simple_logger('capture')


def main(interval: int = 30, dump_interval: int = 5) -> tuple:
    stream_dict = {}
    archived_stream_dict = init_archived_stream_dict()
    # archived_stream_dict = None
    read_path_list = init_read_path_list()
    
    dump_state = {} # dump state

    thread_info = start_capture_thread('enx00e09900866a', interval, dump_interval=dump_interval, state=dump_state)
    start_time = thread_info['start_time']
    capture_thread = thread_info['thread']

    def read_process(stream_dict: dict, archived_stream_dict: dict, read_path_list: list, path: str):
        if path not in read_path_list:
            read_pcap_and_update_dict(stream_dict, path, archived_stream_dict)
            read_path_list.append(path)

    time.sleep(dump_interval + 1)  # wait for first dump end.
    while capture_thread.is_alive():
        for path in get_completed_pcap_chunck_files(start_time, dump_interval):
            read_process(stream_dict, archived_stream_dict, read_path_list, path)
    time.sleep(1)                  # wait for last dump end.
    read_process(stream_dict, archived_stream_dict, read_path_list, path)

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
