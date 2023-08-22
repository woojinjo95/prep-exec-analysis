from typing import Dict
import json
import cv2
import logging

from scripts.format import InputData

logger = logging.getLogger('connection')


def load_data() -> Dict:
    return {
        "video_path": "/app/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-22T113901F361442+0900_1800.mp4",
        "stat_path": "/app/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-22T113901F361442+0900_1800.mp4_stat",   
    }


def load_input() -> InputData:
    data = load_data()

    video_path = data['video_path']
    with open(data['stat_path'], 'r') as f:
        json_data = json.load(f)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    logger.info(f'data load completed. video_path: {video_path}, fps: {fps}, frame count: {frame_count}')
    timestamps = json_data["data"]["timestamps"]
    logger.info(f'json data timestamp length: {len(timestamps)}')
    if frame_count != len(timestamps):
        raise Exception(f'frame count and timestamp length are not matched. frame count: {frame_count}, timestamp length: {len(timestamps)}')

    return InputData(
        video_path=video_path,
        timestamps=timestamps,
    )
