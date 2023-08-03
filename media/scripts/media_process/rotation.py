import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import time
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


def get_file_creation_time(line: str) -> Tuple[str, float]:
    if re.search(r'\[segment.+\] Opening ', line):
        result = re.search(r"'.+\.mp4'", line)
        if result:
            return result.group().strip("'"), time.time()
        else:
            pass
    else:
        return None


def process_video_info(file_info: dict) -> dict:
    name = file_info['name']
    created_time = file_info['created']
    index = file_info['index']

    # Get video info
    cap = cv2.VideoCapture(name)
    last_modified = os.path.getmtime(name)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    calculated_fps = round(frame_count / (last_modified - created_time), 4)

    video_info = {'frame_count': frame_count,
                  'fps': fps,
                  'width': width,
                  'height': height,
                  'fourcc': fourcc,
                  'index': index,
                  'created_time': created_time,
                  'last_modified': last_modified,
                  'calculated_fps': calculated_fps}

    json_file_name = substitute_path_extension(name, 'mp4_stat')

    with open(json_file_name, 'w', encoding='utf-8') as metadata:
        metadata.write(json.dumps(video_info, ensure_ascii=False, indent=4))

    return video_info


class RotationFileManager:

    def __init__(self):
        recording_config = get_value('recording')
        self.path = recording_config['real_time_video_path']
        self.segment_interval = recording_config['segment_interval']
        self.rotation_interval = recording_config['rotation_interval']
        self.file_count = self.segment_interval // self.segment_interval + 5
        self.files_deque = deque(maxlen=self.file_count)
        self.preserved_list = []
        self.index = 0

    def get_exist_files(self, format='*') -> List[str]:
        return sorted(glob(os.path.join(self.path, f'*.{format}')))

    def add_new_file(self, name: str, created_time: float):
        self.update_completed_file_info()
        file_info = {'name': name, 'created': created_time, 'index': self.index}
        self.index += 1
        self.files_deque.append(file_info)
        self.remove_old_files()

    def update_completed_file_info(self):
        file_info_list = list(deepcopy(self.files_deque))
        for file_info in file_info_list:
            video_name = file_info['name']
            json_file_name = substitute_path_extension(video_name, 'mp4_stat')
            if not os.path.exists(json_file_name):
                process_video_info(file_info)

    def remove_old_files(self):
        exists_files = self.get_exist_files('mp4')
        video_name_list = [file_info['name'] for file_info in self.files_deque]
        if len(exists_files) > 0:
            for file_name in exists_files:
                if file_name not in self.preserved_list and file_name not in video_name_list:
                    os.remove(file_name)
                    json_file_name = substitute_path_extension(file_name, 'mp4_stat')
                    if os.path.exists(json_file_name):
                        os.remove(json_file_name)


class MakeVideo:

    def __init__(self, start_time: float = None, end_time: float = None, interval: float = 30):

        self.root_file_path = get_value('common', 'root_file_path', './data')
        recording_config = get_value('recording')
        self.path = recording_config['real_time_video_path']
        self.output_path = recording_config['output_video_path']
        self.temp_path = 'temp_videos'
        self.now = time.time()
        self.start_time = self.now - interval if start_time is None else start_time
        self.end_time = self.start_time + interval if end_time is None else end_time is None

        os.makedirs(self.temp_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)
        time_info = timestamp_to_datetime_with_timezone_str(self.start_time, format="%Y-%m-%dT%H%M%SF%f%z", timezone=get_value('common', 'timezone', db=RedisDBEnum.hardware))
        self.output_video_name = os.path.join(self.output_path, f'video_{time_info}_{interval}.mp4')
        self.video_name_list = []
        self.json_name_list = []

        logger.info(f'Make new video: {self.output_video_name}, {self.start_time} to {self.end_time}')
        self.state = 'writing'

    def copy_files(self):
        json_list = sorted(glob(os.path.join(self.path, f'*.mp4_stat')))
        if json_list:
            for json_file in json_list:
                with open(json_file) as f:
                    video_info = json.loads(f.read())

                if video_info['created_time'] < self.start_time < video_info['last_modified'] or self.start_time < video_info['created_time']:
                    if not os.path.exists(os.path.join(self.temp_path, json_file)):
                        shutil.copy(json_file, os.path.join(self.temp_path, os.path.basename(json_file)))
                        video_file = substitute_path_extension(json_file, 'mp4')
                        new_video_name = os.path.join(self.temp_path, os.path.basename(video_file))
                        shutil.copy(video_file, new_video_name)
                        self.video_name_list.append(new_video_name)
                        self.json_name_list.append(json_file)

                    if video_info['last_modified'] > self.end_time:
                        self.state = 'merging'

    def concat_file(self):
        video_name_list = sorted(list(set(self.video_name_list)))

        if len(video_name_list) == 0:
            logger.error(f'Failed to make {self.output_video_name}, no available live video for that time')
        else:
            with tempfile.NamedTemporaryFile(delete=False, mode='w+t') as f:
                for video in video_name_list:
                    f.write(f"file '{os.path.abspath(video)}'\n")
                temp_filename = f.name

            ffmpeg_command = f"ffmpeg -f concat -safe 0 -i {temp_filename} -c copy {self.output_video_name} -loglevel panic -hide_banner"
            logger.info(f'Concat ffmpeg command: {ffmpeg_command}')
            subprocess.call(ffmpeg_command, shell=True)

            json_name_list = sorted(list(set(self.json_name_list)))

            with JsonManager(substitute_path_extension(self.output_video_name, 'mp4_stat')) as jf:
                video_infos = []
                for json_file in json_name_list:
                    with open(json_file, 'r') as f:
                        video_infos.append(json.loads(f.read()))
                jf.change('data', video_infos)

            for video in video_name_list:
                try:
                    os.remove(video)
                    os.remove(substitute_path_extension(video, 'mp4_stat'))
                except:
                    pass

            # remove the temporary file
            os.unlink(temp_filename)
            logger.info(f'New video save completed: {self.output_video_name}')

        self.state = 'end'

    def run(self):
        while self.state == 'writing':
            self.copy_files()
            time.sleep(1)
        self.concat_file()
        video_info = {'created': timestamp_to_datetime_with_timezone_str(),
                      'path': os.path.join(self.root_file_path, self.output_video_name),
                      'name': os.path.basename(self.output_video_name),
                      # length.. or something
                      }
        with get_strict_redis_connection() as src:
            subscribe_count = publish(src, 'videos', video_info)
        _, id = insert_to_mongodb('videos', video_info)

        logger.info(f'Video info created, {subscribe_count} listener get data, saved mongodb document "videos", {id}, with info: {video_info}')
