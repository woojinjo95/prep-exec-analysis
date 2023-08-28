import logging
import cv2
import traceback

from scripts.analysis.image import calc_color_entropy
from scripts.config.config import get_setting_with_env
from scripts.format import ReportName
from scripts.external.data import load_input
from scripts.external.report import report_output
from scripts.util.decorator import log_decorator
from scripts.format import LogName

logger = logging.getLogger(LogName.COLOR_REFERENCE.value)


@log_decorator(logger)
def process():
    try:
        args = load_input()
        skip_frame = get_setting_with_env('COLOR_REFERENCE_SKIP_FRAME', 60)
        
        cap = cv2.VideoCapture(args.video_path)
        logger.info(f"frame count: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}")

        idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if idx % skip_frame == 0:
                color_entropy = calc_color_entropy(frame)
                logger.info(f"idx: {idx}, color_entropy: {color_entropy}")
                report_output(ReportName.COLOR_REFERENCE.value, {
                    'color_reference': color_entropy,
                })
            idx += 1
        
        cap.release()

    except Exception as err:
        logger.error(f"error in color_reference process: {err}")
        logger.warning(traceback.format_exc())
