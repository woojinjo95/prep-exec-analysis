import logging
import time
from typing import Dict
import json
import cv2

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.config.mongo import construct_report_data
from scripts.analysis.color_reference import calc_color_entropy
from scripts.config.config import get_setting_with_env
from scripts.format import ColorReferenceReport


logger = logging.getLogger('color_reference')


def postprocess():
    logger.info(f"start color_reference postprocess")
    data = load_input()
    skip_frame = get_setting_with_env('COLOR_REFERENCE_SKIP_FRAME', 60)
    
    cap = cv2.VideoCapture(data['video_path'])
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % skip_frame == 0:
            color_entropy = calc_color_entropy(frame)
            logger.info(f"color_entropy: {color_entropy}")
            report_output(color_entropy)
        idx += 1
    
    cap.release()


def load_input() -> Dict:
    # load data format to db
    data = {
        "path": "./data/workspace/testruns/2023-08-14T042445F738532/raw/videos/video_2023-08-14T181329F384025+0900_180.mp4",
        "stat_path": "./data/workspace/testruns/2023-08-14T042445F738532/raw/videos/video_2023-08-14T181329F384025+0900_180.mp4_stat",
    }
    return {
        'video_path': data['path'],
        'json_data': json.load(open(data['stat_path'], 'r'))
    }


def report_output(color_entropy: float):
    report = construct_report(color_entropy).__dict__
    logger.info(f'insert {report} to db')
    insert_to_mongodb('color_reference', report)


def construct_report(color_entropy: float) -> ColorReferenceReport:
    report_data = construct_report_data()
    return ColorReferenceReport(
        scenario_id=report_data.scenario_id,
        timestamp=report_data.timestamp,
        color_reference=color_entropy
    )

 