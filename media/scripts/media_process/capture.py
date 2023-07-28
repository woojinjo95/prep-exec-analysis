import logging
import os
import shutil
import subprocess
import time
import datetime
from multiprocessing import Event, Manager, Process, Queue
from multiprocessing.managers import DictProxy

import cv2

from .rotation import get_file_creation_time, RotationFileManager, MakeVideo
from .loudness import (get_sound_values,
                       set_device_volume)

logger = logging.getLogger('main')


def construct_ffmpeg_cmd(segment_time: int = 10, output_path='real_time_videos') -> str:
    video_name = '/dev/video0'
    audio_name = 'hw:1'
    # crf is stand for constant rate factor, 0 to 51
    # if this value increase, video quality andimage size and process time is decrease
    # ffmpeg default crf is 23, 17~18 is visually noticible.
    # if crf value +6, video size is half.

    # 1920x1080 @ 60FPS from /dev/video0 by v4l2, -re option is realtime.
    video_input_settings = f'ffmpeg -re -f v4l2 -framerate 60 -video_size 1920x1080 -i {video_name}'
    # audio from hw:1, by alsa, and calculate lkfs by ebur128 filter
    audio_input_settings = f'-f alsa -i {audio_name} -af ebur128'
    # using h264 codec, ultrafast compression, minimize delay by nobuffer, crf level 23 no b-frame
    dump_video_settings = '-map 0:v -c:v libx264 -preset ultrafast -fflags nobuffer -crf 20 -bf 0'
    # using aac codec, bitrate 128 kbytes/s, and dump it segment_time interval.
    dump_audio_settings = f'-map 1:a -c:a aac -b:a 128k -f segment -segment_time {segment_time} -reset_timestamps 1 -strftime 1 {output_path}/live_%s.mp4'
    # using h264 codec, resize to half, ultrafast compression, minimize delay by nobuffer, crf level 30 no b-frame
    streaming_video_settings = '-map 0:v -c:v libx264 -s 960x540 -r 30 -preset ultrafast -fflags nobuffer -tune zerolatency -crf 30 -bf 0'
    #  using aac codec, bitrate 64 kbytes/s, stream to localhost:8544 by rtsp protocol
    streaming_audio_settings = '-map 1:a -c:a aac -b:a 64k -f rtsp -rtsp_transport tcp rtsp://localhost:8554/live'

    cmd = ' '.join([video_input_settings,
                    audio_input_settings,
                    dump_video_settings,
                    dump_audio_settings,
                    streaming_video_settings,
                    streaming_audio_settings])

    return cmd


def get_video_info(filepath):
    # Get creation time
    os.stat
    creation_time = os.path.get(filepath)
    readable_creation_time = datetime.datetime.fromtimestamp(creation_time)

    # Get video info
    video = cv2.VideoCapture(filepath)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)

    return {"creation_time": readable_creation_time, "frame_count": frame_count, "fps": fps}


def start_capture(shared_values: DictProxy, audio_values: Queue, stop_event: Event):
    audio_name = 'hw:1'
    output_path = shared_values.get('output_path', 'real_time_videos')
    set_device_volume(audio_name)
    cmd = construct_ffmpeg_cmd(output_path=output_path)
    rotation_file_manager = RotationFileManager(path=output_path)

    with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        start_time = time.time()
        while process.poll() is None and not stop_event.is_set():
            output = process.stdout.readline()
            if output != b'':
                line = output.decode().strip('\n')
                file_created_info = get_file_creation_time(line)
                if file_created_info is not None:
                    logger.warning(str(file_created_info))
                    rotation_file_manager.add_new_file(*file_created_info)

                loudness_values = get_sound_values(start_time, line)
                audio_values.put(loudness_values)

        process.stdin.write(b'q')
        process.stdin.close()

    rotation_file_manager.update_completed_file_info()


def audio_value_consumer(audio_values: Queue, stop_event: Event):
    idx = 0
    while not stop_event.is_set() or not audio_values.empty():
        idx += 1
        value = audio_values.get()
        if idx % 10 == 0:
            logger.warning(f'{value}')


def test(duration=30):
    # logger = logging.Logger('main')
    # logger.setLevel(logging.DEBUG)

    logger.info('start')

    with Manager() as manager:
        configs = manager.dict()
        video_path = 'videos'
        default_path = 'real_time_videos'
        configs['output_path'] = default_path
        os.makedirs(default_path, exist_ok=True)
        os.makedirs(video_path, exist_ok=True)
        # os.system(f'rm {default_path}/*.mp4')
        audio_values = Queue()
        stop_event = Event()
        capture_process = Process(target=start_capture, args=(configs, audio_values, stop_event), daemon=True)
        consumer_process = Process(target=audio_value_consumer, args=(audio_values, stop_event), daemon=True)

        capture_process.start()
        consumer_process.start()
        time.sleep(35)
        new_video = MakeVideo(default_path, video_path, duration=20)
        new_video.run()
        print('Xxxxxxx')
        time.sleep(5)
        stop_event.set()
        print('Xxxxxxx')