import logging
from typing import Dict
import cv2
import traceback
import time

from scripts.config.config import get_setting_with_env
from scripts.analysis.freeze_detect import FreezeDetector
from scripts.format import CollectionName
from scripts.connection.external import load_input, report_output, publish_msg
from scripts.util._timezone import get_utc_datetime

logger = logging.getLogger('freeze_detect')


def detect_freeze():
    try:
        logger.info(f"start detect_freeze process")
        
        args = load_input()
        cap = cv2.VideoCapture(args.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        freeze_detector = set_freeze_detector(fps)

        for frame_index in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break

            cur_time = args.timestamps[frame_index]

            result = freeze_detector.update(frame, cur_time)
            if result['detect']:
                logger.info(f"freeze detected at {frame_index}")
                report_output(CollectionName.FREEZE.value, {
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


def set_freeze_detector(fps: float) -> FreezeDetector:
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
    return freeze_detector
