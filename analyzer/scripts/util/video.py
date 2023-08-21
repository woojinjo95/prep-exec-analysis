import cv2
import logging
import os
import subprocess
from typing import Dict, List

from util.common import seconds_to_time
from scripts.format import CroppedInfo

logger = logging.getLogger('main')

class VideoCaptureContext:
    def __init__(self, *args, **kwargs):
        self.cap = cv2.VideoCapture(*args, **kwargs)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()
        cv2.destroyAllWindows()


def FrameGenerator(video_path: str, timestamps: list = None):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for frame_index in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            logger.warning(f"cannot read frame at {frame_index}")
            break

        if timestamps:
            try:
                cur_time = timestamps[frame_index]
            except IndexError:
                cur_time = 0
        else:
            cur_time = 0

        yield frame, cur_time

    cap.release()


def crop_video(video_path: str, output_path: str, start_time: float, end_time: float):
    # start_time: absolute start time
    # end_time: absolute end time
    cmd = [
        'ffmpeg', 
        '-i', video_path,
        '-ss', seconds_to_time(start_time),  # Start time, e.g., '00:00:10' for 10 seconds in
        '-to', seconds_to_time(end_time),    # End time, e.g., '00:01:00' for 1 minute in
        '-c:v', 'copy',     # Use the same codec for video
        '-c:a', 'copy',     # Use the same codec for audio
        '-y',
        output_path
    ]
    subprocess.run(cmd)


def crop_video_with_timestamps(video_path: str, timestamps: List[float], target_times: List[float], 
                               output_dir: str, duration: float) -> List[CroppedInfo]:
    os.makedirs(output_dir, exist_ok=True)
    cropped_videos = []
    for start_time in target_times:
        end_time = start_time + duration

        cropped_video_path = os.path.join(output_dir, f'{start_time}.mp4')
        crop_video(video_path=video_path,
                    output_path=cropped_video_path,
                    start_time=start_time,
                    end_time=end_time)
        cropped_timestamp = [timestamp for timestamp in timestamps if start_time <= timestamp <= end_time]
        logger.info(f'video frame count: {get_video_info(cropped_video_path)["frame_count"]}, timestamp count: {len(cropped_timestamp)}')

        cropped_info = CroppedInfo(video_path=cropped_video_path, timestamps=cropped_timestamp)
        cropped_videos.append(cropped_info)
    return cropped_videos


def get_video_info(video_path: str) -> Dict:
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return {
        'frame_count': frame_count,
        'fps': fps,
    }
