from typing import Dict, Tuple
import json
import cv2
import logging
import os

from scripts.format import InputData
from scripts.config.constant import RedisDB
from scripts.connection.redis_conn import get_strict_redis_connection, parse_bytes_to_value
from scripts.external.scenario import load_scenario

logger = logging.getLogger('connection')


def load_data() -> Dict:
    # scenario = load_scenario()
    # # logger.info(f'scenario: {scenario}')
    # video_path = scenario['testrun']['raw']['videos'][0]['path']
    # stat_path = scenario['testrun']['raw']['videos'][0]['stat_path']
    video_path = "/app/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-22T172921F075886+0900_1800.mp4"
    stat_path = "/app/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-22T172921F075886+0900_1800.mp4_stat"
    return {
        "video_path": video_path,
        "stat_path": stat_path,
    }


def load_input() -> InputData:
    data = load_data()

    video_path = data['video_path']
    if not video_path or not video_path.endswith('.mp4') or not os.path.exists(video_path):
        raise Exception(f'video path is invalid. video path: {video_path}')

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


def read_analysis_config() -> Dict:
    with get_strict_redis_connection(RedisDB.hardware) as src:
        analysis_config = {}
        for key in src.scan_iter(match="analysis_config:*"):
            group = parse_bytes_to_value(key).split(':')[1]
            analysis_config[group] = {parse_bytes_to_value(k): parse_bytes_to_value(v)
                                        for k, v in src.hgetall(key).items()}
    return analysis_config
