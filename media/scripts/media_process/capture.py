import logging
import os
import subprocess
import time
from multiprocessing import Event, Process, Queue

from ..configs.config import get_value, set_value
from ..configs.constant import RedisChannel
from ..utils._subprocess import kill_pid_grep
from ..utils.docker import convert_if_docker_localhost
from .loudness import get_sound_values, set_device_volume
from .rotation import RotationFileManager, get_file_creation_time
from ..connection.redis_pubsub import publish, get_strict_redis_connection

logger = logging.getLogger('main')
file_logger = logging.getLogger('file')


def get_rtsp_public_url() -> str:
    streaming_url = get_value('capture', '')
    return convert_if_docker_localhost(streaming_url)


def construct_ffmpeg_cmd() -> str:
    capture_configs = get_value('capture')
    streaming_configs = get_value('streaming')
    recording_configs = get_value('recording')

    # capture config
    video_name = capture_configs['video_device']
    audio_name = capture_configs['audio_device']
    capture_dimension = f'{capture_configs["width"]}x{capture_configs["height"]}'
    capture_framerate = capture_configs['fps']

    # stremaing config
    rtsp_public_url = convert_if_docker_localhost(streaming_configs['rtsp_publish_url'])
    rtsp_publish_port = streaming_configs['rtsp_publish_port']
    streaming_name = streaming_configs['streaming_name']
    rtsp_url = f'rtsp://{rtsp_public_url}:{rtsp_publish_port}/{streaming_name}'
    streaming_dimension = f'{streaming_configs["width"]}x{streaming_configs["height"]}'
    streaming_framerate = streaming_configs['fps']
    streaming_crf = streaming_configs['crf']

    # recording config
    segment_time = recording_configs['segment_interval']
    output_path = recording_configs['real_time_video_path']
    recording_crf = recording_configs['crf']
    os.makedirs(output_path, exist_ok=True)

    # crf is stand for constant rate factor, 0 to 51
    # if this value increase, video quality andimage size and process time is decrease
    # ffmpeg default crf is 23, 17~18 is visually noticible.
    # if crf value +6, video size is half.

    # 1920x1080 @ 60FPS from /dev/video0 by v4l2, -re option is realtime.
    video_input_settings = f'ffmpeg -re -f v4l2 -framerate {capture_framerate} -video_size {capture_dimension} -i {video_name}'
    # audio from hw:1, by alsa, and calculate lkfs by ebur128 filter
    audio_input_settings = f'-f alsa -i {audio_name} -af ebur128'
    # using h264 codec, ultrafast compression, minimize delay by nobuffer, crf level 23 no b-frame
    dump_video_settings = f'-map 0:v -c:v libx264 -preset ultrafast -fflags nobuffer -crf {recording_crf} -bf 0'
    # using aac codec, bitrate 128 kbytes/s, and dump it segment_time interval.
    dump_audio_settings = f'-map 1:a -c:a aac -b:a 128k -f segment -segment_time {segment_time} -reset_timestamps 1 -strftime 1 {output_path}/live_%s.mp4'
    # using h264 codec, resize to half, ultrafast compression, minimize delay by nobuffer, crf level 30 no b-frame
    streaming_video_settings = f'-map 0:v -c:v libx264 -s {streaming_dimension} -r {streaming_framerate} -preset ultrafast -fflags nobuffer -tune zerolatency -crf {streaming_crf} -bf 0'
    #  using aac codec, bitrate 64 kbytes/s, stream to localhost:8544 by rtsp protocol
    streaming_audio_settings = f'-map 1:a -c:a aac -b:a 64k -f rtsp -rtsp_transport tcp {rtsp_url}'

    cmd = ' '.join([video_input_settings,
                    audio_input_settings,
                    dump_video_settings,
                    dump_audio_settings,
                    streaming_video_settings,
                    streaming_audio_settings])

    logger.info(f'Streaming and recording and sound level ffmpeg command: {cmd}')

    return cmd


def start_capture(audio_values: Queue, stop_event: Event):
    capture_configs = get_value('capture')
    set_device_volume(capture_configs['audio_device'], capture_configs['audio_gain'])
    cmd = construct_ffmpeg_cmd()
    rotation_file_manager = RotationFileManager()

    try:
        set_value('state', 'streaming_state', 'streaming')
        # ffmpeg use stderr that stderr = stderr=subprocess.STDOUT
        with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            start_time = time.time()
            while process.poll() is None and not stop_event.is_set():
                output = process.stdout.readline()
                if output != b'':
                    line = output.decode().strip('\n')
                    file_created_info = get_file_creation_time(line)
                    if file_created_info is not None:
                        file_logger.info(f'Video: {file_created_info[0]} / {file_created_info[1]}')
                        rotation_file_manager.add_new_file(*file_created_info)

                    loudness_values = get_sound_values(start_time, line)
                    audio_values.put(loudness_values)

            process.stdin.write(b'q')
            process.stdin.close()

        rotation_file_manager.update_completed_file_info()
    finally:
        # kill process
        time.sleep(0.5)
        kill_pid_grep(capture_configs['video_device'])
        set_value('state', 'streaming_state', 'idle')


def audio_value_consumer(audio_values: Queue, stop_event: Event):
    # value format: {'t': 1690940538.72, 'M': -27.5, 'I': -29.1, 'inactive': False}
    idx = 0
    with get_strict_redis_connection() as src:
        while not stop_event.is_set() or not audio_values.empty():
            idx += 1
            value = audio_values.get()
            # TODO add data save function if this value is needed.
            publish(src, RedisChannel.loudness, value)


def streaming() -> Event:
    logger.info('Streaming Start')
    audio_values = Queue()
    stop_event = Event()
    capture_process = Process(target=start_capture, args=(audio_values, stop_event), daemon=True)
    consumer_process = Process(target=audio_value_consumer, args=(audio_values, stop_event), daemon=True)

    capture_process.start()
    consumer_process.start()

    return stop_event
