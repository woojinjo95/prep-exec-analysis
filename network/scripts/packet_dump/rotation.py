import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import time
import datetime
from collections import deque
from copy import deepcopy
from glob import glob
from typing import List, Tuple

import cv2

from ..configs.config import RedisDBEnum, get_value
from ..connection.mongo_db.create import insert_to_mongodb
from ..connection.redis_pubsub import publish, get_strict_redis_connection
from ..utils._timezone import timestamp_to_datetime_with_timezone_str
from ..utils.file_manage import JsonManager, substitute_path_extension

logger = logging.getLogger('main')


class RotationFileManager:

    def __init__(self):
        network_capture_configs = get_value('network')
        self.path = network_capture_configs['real_time_packet_path']
        self.segment_interval = network_capture_configs['segment_interval']
        self.rotation_interval = network_capture_configs['rotation_interval']
        self.file_count = self.rotation_interval // self.segment_interval + 5
        self.files_deque = deque(maxlen=self.file_count)
        self.preserved_list = []
        self.index = 0
        self.remove_old_files()

    def get_exist_files(self, format='*') -> List[str]:
        return sorted(glob(os.path.join(self.path, f'*.{format}')))

    def get_file_info(self, filename):
        basename = os.path.basename(filename)
        timestamp_str = basename.split('_')[2].split('.')[0]
        dt = datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
        created_time = dt.timestamp()
        self.index = 1

        return filename, created_time

    def check_new_file(self) -> Tuple[str, float]:
        reversed_file_list = self.get_exist_files('pcap')[::-1]
        packet_name_list = [file_info['name'] for file_info in self.files_deque]
        for idx, file in enumerate(reversed_file_list):
            if file in packet_name_list:
                if idx == 0:
                    # no new file
                    return None
                else:
                    new_file = reversed_file_list[idx - 1]
                    return self.get_file_info(new_file)
        else:
            try:
                if len(self.files_deque) == 0:
                    return self.get_file_info(file)
                else:
                    return None
            except:
                return None

    def add_new_file(self, name: str, created_time: float):
        file_info = {'name': name, 'created': created_time, 'index': self.index}
        self.index += 1
        self.files_deque.append(file_info)
        self.remove_old_files()

    def remove_old_files(self):
        exists_files = self.get_exist_files('pcap')
        packet_name_list = [file_info['name'] for file_info in self.files_deque]
        if len(exists_files) > 0:
            for file_name in exists_files:
                if file_name not in self.preserved_list and file_name not in packet_name_list:
                    try:
                        os.remove(file_name)
                    except:
                        pass

        if len(exists_files) > self.file_count * 2:
            logger.critical('Rotation System malfunctioned!!! remove all pcap file')
            for file_name in exists_files:
                try:
                    os.remove(file_name)
                except:
                    pass
