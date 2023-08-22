import cv2
import logging
import os
from typing import Dict, List, Tuple

from scripts.util.common import seconds_to_time
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


def get_video_info(video_path: str) -> Dict:
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cap.get(cv2.CAP_PROP_FOURCC)
    cap.release()
    return {
        'frame_count': frame_count,
        'width': width,
        'height': height,
        'fps': fps,
        'fourcc': fourcc,
    }


def find_nearest_index(timestamps: List[float], target_time: float) -> float:
    differences = [abs(ts - target_time) for ts in timestamps]
    nearest_index = differences.index(min(differences))
    return nearest_index


def crop_video(video_path: str, output_path: str, start_index: int, end_index: int, timestamps: List[float]) -> Tuple[str, List[float]]:
    logger.info(f'crop video start. output_path: {output_path}, start_index: {start_index}, end_index: {end_index}')

    video_info = get_video_info(video_path)
    # logger.info(f'video_info: {video_info}')

    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, video_info['fps'], (video_info['width'], video_info['height']))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_index)

    cropped_timestamps = []
    for frame_index in range(start_index, end_index):
        ret, frame = cap.read()
        if not ret:
            logger.warning(f"cannot read frame at {frame_index}")
            break
        out.write(frame)
        cropped_timestamps.append(timestamps[frame_index])

    cap.release()
    out.release()
    
    if len(cropped_timestamps) != end_index - start_index:
        logger.warning(f'slicing in end of the video. cropped_timestamps: {len(cropped_timestamps)}, start_index: {start_index}, end_index: {end_index}')
    logger.info(f'video crop completed. output_path: {output_path}')
    return output_path, cropped_timestamps


def crop_video_with_opencv(video_path: str, timestamps: List[float], target_times: List[float], 
                            output_dir: str, duration: float) -> List[CroppedInfo]:
    os.makedirs(output_dir, exist_ok=True)

    crop_infos = []
    for target_time in target_times:
        start_index = find_nearest_index(timestamps, target_time)
        end_index = find_nearest_index(timestamps, target_time + duration)
        cropped_video_path = os.path.join(output_dir, f'{start_index}.mp4')
        crop_infos.append({
            'cropped_video_path': cropped_video_path,
            'start_index': start_index,
            'end_index': end_index,
        })

    cropped_videos = []
    for crop_info in crop_infos:
        cropped_video_path, cropped_timestamps = crop_video(video_path, crop_info['cropped_video_path'], crop_info['start_index'], crop_info['end_index'], timestamps)
        cropped_info = CroppedInfo(video_path=cropped_video_path, timestamps=cropped_timestamps)
        cropped_videos.append(cropped_info)

        frame_count, timestamp_length = get_video_info(cropped_video_path)['frame_count'], len(cropped_timestamps)
        logger.info(f'cropped video info. frame_count: {frame_count}, timestamp_length: {timestamp_length}')
        if frame_count != timestamp_length:
            logger.error(f'cropped frame count and timestamps mismatch.')
    return cropped_videos
