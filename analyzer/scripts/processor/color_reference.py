import logging
import traceback
from typing import Dict

import cv2
from scripts.analysis.image import calc_color_entropy
from scripts.config.config import get_setting_with_env
from scripts.connection.redis_pubsub import publish_msg
from scripts.external.data import load_input
from scripts.external.report import report_output
from scripts.external.analysis import set_analysis_info
from scripts.format import Command, ReportName
from scripts.util._timezone import get_utc_datetime
from scripts.util.decorator import log_decorator
from scripts.util.video import FrameGenerator

logger = logging.getLogger('main')


@log_decorator(logger)
def test_color_reference():
    try:
        args = load_input()
        config = get_config()
        
        for idx, (frame, cur_time) in enumerate(FrameGenerator(args.video_path, args.timestamps)):
            if idx % config['skip_frame'] == 0:
                frame = cv2.resize(frame, config['resolution'])
                color_entropy = calc_color_entropy(frame)
                logger.info(f"idx: {idx}, color_entropy: {color_entropy}")
                report_output(ReportName.COLOR_REFERENCE.value, {
                    'timestamp': get_utc_datetime(cur_time),
                    'color_reference': color_entropy,
                }) 

        publish_msg({'measurement': Command.COLOR_REFERENCE.value}, 'analysis_response')
        set_analysis_info(Command.COLOR_REFERENCE.value)

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': Command.COLOR_REFERENCE.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in test_color_reference: {err}")
        logger.warning(error_detail)


def get_config() -> Dict:
    resolution = get_setting_with_env('COLOR_REFERENCE_RESOLUTION', (960, 540))
    skip_frame = get_setting_with_env('COLOR_REFERENCE_SKIP_FRAME', 60)
    return {
        'resolution': resolution,
        'skip_frame': skip_frame,
    }
