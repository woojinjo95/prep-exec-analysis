import logging
from typing import Dict
import cv2
import traceback
import time

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.connection.external import construct_report_data
from scripts.config.config import get_setting_with_env
from scripts.analysis.freeze_detect import FreezeDetector
from scripts.format import FreezeReport, CollecionName


logger = logging.getLogger('freeze_detect')


def detect_freeze():
    try:
        logger.info(f"start detect_freeze process")
        
        data = load_input()
        cap = cv2.VideoCapture(data['video_path'])
        fps = cap.get(cv2.CAP_PROP_FPS)
        logger.info(f"fps: {fps}, frame count: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}")

        freeze_detector = FreezeDetector(
            fps=fps,
            sampling_rate=get_setting_with_env('FREEZE_DETECT_SKIP_FRAME', 6),
            min_interval=get_setting_with_env('FREEZE_DETECT_MIN_INTERVAL', 5),
            min_color_depth_diff=get_setting_with_env('FREEZE_DETECT_MIN_COLOR_DEPTH_DIFF', 10),
            min_diff_rate=get_setting_with_env('FREEZE_DETECT_MIN_DIFF_RATE', 0.0001),
            frame_stdev_thres=get_setting_with_env('FREEZE_DETECT_FRAME_STDEV_THRES', 0.01),
        )
        
        idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            result = freeze_detector.update(frame, time.time())
            if result['detect']:
                logger.info(f"freeze detected at {idx}")
                report_output(result['freeze_type'])

            idx += 1
        
        cap.release()
        logger.info(f"end detect_freeze process")

    except Exception as err:
        logger.error(f"error in detect_freeze postprocess: {err}")
        logger.warning(traceback.format_exc())


def load_input() -> Dict:
    # load data format to db
    data = {
        "path": "/app/workspace/test.mp4",
        # "stat_path": "./data/workspace/testruns/2023-08-14T042445F738532/raw/videos/video_2023-08-14T181329F384025+0900_180.mp4_stat",
    }
    return {
        'video_path': data['path'],
        # 'json_data': json.load(open(data['stat_path'], 'r'))
    }


def report_output(freeze_type: str):
    report = construct_report(freeze_type).__dict__
    logger.info(f'insert {report} to db')
    insert_to_mongodb(CollecionName.FREEZE.value, report)


def construct_report(freeze_type: str) -> FreezeReport:
    report_data = construct_report_data()
    return FreezeReport(
        scenario_id=report_data.scenario_id,
        timestamp=report_data.timestamp,
        freeze_type=freeze_type
    )
