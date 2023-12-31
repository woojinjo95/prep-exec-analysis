import logging
import time
from multiprocessing import Event, Process

from .analysis.packet_analyzer import (init_archived_stream_dict,
                                       read_pcap_and_update_dict)
from .capture.dumper import start_capture_thread, stop_capture
from .capture.parser import (get_completed_pcap_chunck_files,
                             init_read_path_list)
from .configs.config import get_value
from .mongo_db_update import PacketMongoSession

logger = logging.getLogger('main')


def start_capture(mongo_session: PacketMongoSession, stop_event: Event):
    interval = 3600 * 24 * 2  # 2 days
    segmnet_interval = get_value('network', 'segment_interval', 10)
    rotation_interval = get_value('network', 'rotation_interval', 1800)
    rotating_file_count = rotation_interval // segmnet_interval + 5
    stb_nic = get_value('network', 'stb_nic', 'enx00e09900866a')
    stream_dict = {}

    logger.info(f'Start Packet capture, maximum interval: {interval} second, {segmnet_interval} segment time')

    archived_stream_dict = init_archived_stream_dict()
    read_path_list = init_read_path_list(rotating_file_count)
    history = {}

    dump_state = {}  # dump state

    thread_info = start_capture_thread(stb_nic, interval, dump_interval=segmnet_interval, state=dump_state, rotating_file_count=rotating_file_count, stop_event=stop_event)
    start_time = thread_info['start_time']
    capture_thread = thread_info['thread']
    path = None

    def read_process(stream_dict: dict, archived_stream_dict: dict, read_path_list: list, path: str):
        if path not in read_path_list:
            read_pcap_and_update_dict(mongo_session, stream_dict, path, archived_stream_dict, history)
            read_path_list.append(path)

    time.sleep(segmnet_interval + 1)  # wait for first dump end.
    while capture_thread.is_alive():
        for path in get_completed_pcap_chunck_files(start_time, segmnet_interval):
            read_process(stream_dict, archived_stream_dict, read_path_list, path)
    time.sleep(1)                  # wait for last dump end.
    if path is not None:
        read_process(stream_dict, archived_stream_dict, read_path_list, path)


def real_time_packet_capture(stop_event: Event = Event()) -> Event:
    mongo_session = PacketMongoSession()
    packet_capture_process = Process(target=start_capture, args=(mongo_session, stop_event, ), daemon=True)
    packet_capture_process.start()
    pass
