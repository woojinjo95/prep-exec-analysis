from typing import Dict
import json
import cv2
import logging
import os

from scripts.format import VideoInfo
from scripts.external.scenario import load_testrun, get_scenario_info
from scripts.connection.mongo_db.crud import aggregate_from_mongodb

logger = logging.getLogger('main')


def load_data() -> Dict:
    testrun = load_testrun()
    video_path = str(testrun['raw']['videos'][0]['path'])
    stat_path = str(testrun['raw']['videos'][0]['stat_path'])
    # video_path = video_path.replace('./data', '/app')
    # stat_path = stat_path.replace('./data', '/app')
    return {
        "video_path": video_path,
        "stat_path": stat_path,
    }


def load_input() -> VideoInfo:
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

    return VideoInfo(
        video_path=video_path,
        timestamps=timestamps,
        frame_count=frame_count,
        fps=fps,
    )


def read_analysis_config() -> Dict:
    scenario_info = get_scenario_info()
    pipeline = [{"$match": {'id': scenario_info['scenario_id']}},
                {"$unwind": "$testruns"},
                {"$project": {"testrun_id": "$testruns.id",
                            "config": "$testruns.analysis.config"}},
                {"$match": {"testrun_id": scenario_info['testrun_id']}},
                {"$project": {"_id": 0, "config": "$config"}}]
    res = aggregate_from_mongodb('scenario', pipeline)
    if res:
        analysis_config = res[0].get('config', {})
    else:
        analysis_config = {}
    return analysis_config
