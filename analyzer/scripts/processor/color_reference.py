import logging
from typing import Dict
import cv2
import traceback

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.connection.external import construct_report_data
from scripts.analysis.color_reference import calc_color_entropy
from scripts.config.config import get_setting_with_env
from scripts.format import ColorReferenceReport, CollecionName


logger = logging.getLogger('color_reference')


def postprocess():
    try:
        logger.info(f"start color_reference postprocess")
        data = load_input()
        skip_frame = get_setting_with_env('COLOR_REFERENCE_SKIP_FRAME', 60)
        
        cap = cv2.VideoCapture(data['video_path'])
        logger.info(f"frame count: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}")

        idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if idx % skip_frame == 0:
                color_entropy = calc_color_entropy(frame)
                logger.info(f"idx: {idx}, color_entropy: {color_entropy}")
                report_output(color_entropy)
            idx += 1
        
        cap.release()
        logger.info(f"end color_reference postprocess")

    except Exception as err:
        logger.error(f"error in color_reference postprocess: {err}")
        logger.warning(traceback.format_exc())


def load_input() -> Dict:
    # load data format to db
    data = {
        "path": "/app/workspace/video_2023-08-04T152424F626855+0900_30.mp4",
        # "stat_path": "./data/workspace/testruns/2023-08-14T042445F738532/raw/videos/video_2023-08-14T181329F384025+0900_180.mp4_stat",
    }
    return {
        'video_path': data['path'],
        # 'json_data': json.load(open(data['stat_path'], 'r'))
    }


def report_output(color_entropy: float):
    report = construct_report(color_entropy).__dict__
    logger.info(f'insert {report} to db')
    insert_to_mongodb(CollecionName.COLOR_REFERENCE.value, report)


def construct_report(color_entropy: float) -> ColorReferenceReport:
    report_data = construct_report_data()
    return ColorReferenceReport(
        scenario_id=report_data.scenario_id,
        timestamp=report_data.timestamp,
        color_reference=color_entropy
    )

 