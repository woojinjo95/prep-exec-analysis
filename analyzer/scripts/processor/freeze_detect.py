import logging
from typing import Dict
import cv2
import traceback
import time

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.connection.external import construct_report_data
from scripts.config.config import get_setting_with_env
from scripts.analysis.freeze_detect import FreezeDetector
from scripts.format import FreezeReport, CollectionName
from scripts.connection.external import load_input, publish_msg
from scripts.util._timezone import get_utc_datetime

logger = logging.getLogger('freeze_detect')


def detect_freeze():
    try:
        logger.info(f"start detect_freeze process")
        
        data = load_input()
        cap = cv2.VideoCapture(data['video_path'])
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        logger.info(f'data load completed. video_path: {data["video_path"]}, fps: {fps}, frame count: {frame_count}')
        timestamps = data["json_data"]["data"]["timestamps"]
        logger.info(f'json data timestamp length: {len(timestamps)}')
        if frame_count != len(timestamps):
            raise Exception(f'frame count and timestamp length are not matched. frame count: {frame_count}, timestamp length: {len(timestamps)}')

        sampling_rate = get_setting_with_env('FREEZE_DETECT_SKIP_FRAME', 6)
        min_interval = get_setting_with_env('FREEZE_DETECT_MIN_INTERVAL', 5)
        min_color_depth_diff = get_setting_with_env('FREEZE_DETECT_MIN_COLOR_DEPTH_DIFF', 10)
        min_diff_rate = get_setting_with_env('FREEZE_DETECT_MIN_DIFF_RATE', 0.0001)
        frame_stdev_thres = get_setting_with_env('FREEZE_DETECT_FRAME_STDEV_THRES', 0.01)

        freeze_detector = FreezeDetector(
            fps=fps,
            sampling_rate=sampling_rate,
            min_interval=min_interval,
            min_color_depth_diff=min_color_depth_diff,
            min_diff_rate=min_diff_rate,
            frame_stdev_thres=frame_stdev_thres,
        )

        logger.info(f"start detect freeze. sampling rate: {sampling_rate}, min interval: {min_interval}, min color depth diff: {min_color_depth_diff}, min diff rate: {min_diff_rate}, frame stdev thres: {frame_stdev_thres}")

        for frame_index in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break

            cur_time = timestamps[frame_index]

            result = freeze_detector.update(frame, cur_time)
            if result['detect']:
                logger.info(f"freeze detected at {frame_index}")
                report_output({
                    'timestamp': get_utc_datetime(cur_time),
                    'freeze_type': result['freeze_type'],
                })

        cap.release()
        publish_msg({'measurement': ['freeze']}, 'analysis_response')
        logger.info(f"end detect_freeze process")

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': ['freeze']}, error_detail, level='error')
        logger.error(f"error in detect_freeze postprocess: {err}")
        logger.warning(error_detail)


def report_output(additional_data: Dict):
    merged_data = {**construct_report_data(), **additional_data}
    report = FreezeReport(**merged_data).__dict__
    logger.info(f'insert {report} to db')
    insert_to_mongodb(CollectionName.FREEZE.value, report)
