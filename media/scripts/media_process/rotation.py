import os
import re
import shutil
import time
from copy import deepcopy
from collections import deque
from glob import glob
from typing import List, Tuple
import cv2
import json
import logging
from multiprocessing import Event
import tempfile
import subprocess

from ..utils.file_manage import substitute_path_extension

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

    calculated_fps = (last_modified - created_time) / frame_count

    video_info = {'frame_count': frame_count,
                  'fps': fps,
                  'width': width,
                  'height': height,
                  'fourcc': fourcc,
                  'index': index,
                  'created_time': created_time,
                  'last_modified': last_modified,
                  'calculated_fps': calculated_fps}

    json_file_name = substitute_path_extension(name, 'json')

    with open(json_file_name, 'w', encoding='utf-8') as metadata:
        metadata.write(json.dumps(video_info, ensure_ascii=False, indent=4))

    return video_info


class RotationFileManager:

    def __init__(self, path: str, segment_time: int = 10, duration: int = 60):
        self.path = path
        self.segment_time = segment_time
        self.duration = duration

        self.file_count = duration//segment_time + 5
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
            json_file_name = substitute_path_extension(video_name, 'json')
            if not os.path.exists(json_file_name):
                process_video_info(file_info)

    def remove_old_files(self):
        exists_files = self.get_exist_files('mp4')
        video_name_list = [file_info['name'] for file_info in self.files_deque]
        if len(exists_files) > self.file_count:
            for file_name in exists_files:
                if file_name not in self.preserved_list and file_name not in video_name_list:
                    os.remove(file_name)
                    json_file_name = substitute_path_extension(file_name, 'json')
                    if os.path.exists(json_file_name):
                        os.remove(json_file_name)


class MakeVideo:

    def __init__(self, path: str, output_path: str, start_time: float = None, end_time: float = None, duration: float = 30):
        self.path = path
        self.output_path = output_path
        self.now = time.time()
        self.start_time = self.now - duration if start_time is None else start_time
        self.end_time = self.start_time + duration if end_time is None else end_time is None

        self.video_name = f'video_{self.start_time}_{duration}.mp4'
        self.open = True

        logger.warning(self.video_name)
        self.video_name_list = []

    def copy_files(self):
        json_list = sorted(glob(os.path.join(self.path, f'*.json')))
        if json_list:
            for json_file in json_list:
                with open(json_file) as f:
                    video_info = json.loads(f.read())

                if video_info['created_time'] < self.start_time < video_info['last_modified'] or self.start_time < video_info['created_time']:
                    if not os.path.exists(os.path.join(self.output_path, json_file)):
                        shutil.copy(json_file, os.path.join(self.output_path, os.path.basename(json_file)))
                        video_file = substitute_path_extension(json_file, 'mp4')
                        new_video_name = os.path.join(self.output_path, os.path.basename(video_file))
                        shutil.copy(video_file, new_video_name)
                        self.video_name_list.append(new_video_name)

                    if video_info['last_modified'] > self.end_time:
                        self.open = False

    def concat_file(self):
        video_name_list = sorted(list(set(self.video_name_list)))
        logger.warning(video_name_list)
        with tempfile.NamedTemporaryFile(delete=False, mode='w+t') as f:
            for video in video_name_list:
                f.write(f"file '{os.path.abspath(video)}'\n")
            temp_filename = f.name

        # construct the command to concatenate videos
        ffmpeg_command = f"ffmpeg -f concat -safe 0 -i {temp_filename} -c copy {self.video_name}"

        # execute the command
        subprocess.call(ffmpeg_command, shell=True)
        for video in video_name_list:
            try:
                os.remove(video)
                os.remove(substitute_path_extension(video, 'json'))
            except:
                pass

        # remove the temporary file
        os.unlink(temp_filename)

    def run(self):
        while self.open:
            self.copy_files()
            time.sleep(1)
        self.concat_file()
