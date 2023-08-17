import logging
from typing import Dict
import cv2
import traceback

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.connection.external import construct_report_data
from scripts.analysis.color_reference import calc_color_entropy
from scripts.config.config import get_setting_with_env
from scripts.format import ColorReferenceReport, CollecionName
from scripts.connection.external import load_input

logger = logging.getLogger('color_reference')


def process():
    try:
        logger.info(f"start color_reference process")
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
                report_output({
                    'color_reference': color_entropy,
                })
            idx += 1
        
        cap.release()
        logger.info(f"end color_reference process")

    except Exception as err:
        logger.error(f"error in color_reference process: {err}")
        logger.warning(traceback.format_exc())


def report_output(additional_data: Dict):
    report = ColorReferenceReport(
        **construct_report_data(),
        **additional_data
    ).__dict__
    logger.info(f'insert {report} to db')
    insert_to_mongodb(CollecionName.COLOR_REFERENCE.value, report)
