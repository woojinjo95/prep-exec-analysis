import logging
import tempfile
import traceback
from typing import Tuple

import cv2
import numpy as np
from scripts.analysis.boot_test.match import task_boot_test_with_match
from scripts.analysis.video import check_poweroff_video
from scripts.config.config import get_setting_with_env
from scripts.connection.redis_pubsub import publish_msg
from scripts.external.data import load_input, read_analysis_config
from scripts.external.event import get_data_of_event_log, get_dut_power_times
from scripts.external.report import report_output
from scripts.external.analysis import set_analysis_info
from scripts.format import Command, ReportName
from scripts.util._timezone import get_utc_datetime
from scripts.util.decorator import log_decorator
from scripts.util.video import crop_video_with_opencv

logger = logging.getLogger('main')


@log_decorator(logger)
def test_cold_boot():
    try:
        analysis_config = read_analysis_config()
        processing_mode = analysis_config['boot']['type']
        logger.info(f'processing_mode: {processing_mode}')
        if processing_mode == 'image_matching':
            test_cold_boot_with_match()
        elif processing_mode == 'screen_change_rate':
            raise NotImplementedError

        publish_msg({'measurement': Command.BOOT.value}, 'analysis_response')
        set_analysis_info(Command.BOOT.value)

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': Command.BOOT.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in test_cold_boot: {err}")
        logger.warning(error_detail)


def test_cold_boot_with_match():
    args = load_input()
    template = get_template_from_config()
    roi = get_roi_from_config()

    event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
    power_times = get_dut_power_times(event_log)
    # power_times = [1692694635.952278]

    with tempfile.TemporaryDirectory(dir='/tmp') as output_dir:
        results = []
        crop_videos = crop_video_with_opencv(args.video_path, args.timestamps, power_times, output_dir, get_setting_with_env('COLD_BOOT_DURATION', 90))
        for crop_video in crop_videos:
            if not check_poweroff_video(crop_video.video_path):
                continue
            result = task_boot_test_with_match(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0],
                                               roi, template, roi)
            results.append(result)

    for result in results:
        if result['status'] == 'success':
            report_output(ReportName.COLD_BOOT.value, {
                'timestamp': get_utc_datetime(result['match_timestamp']),
                'measure_time': result['match_time'],
            })


def get_template_from_config() -> np.ndarray:
    analysis_config = read_analysis_config()
    image_path = analysis_config['boot']['frame']['path']
    image = cv2.imread(image_path)
    logger.info(f'image shape: {image.shape}')
    return image


def get_roi_from_config() -> Tuple[int, int, int, int]:
    analysis_config = read_analysis_config()
    roi_data = analysis_config['boot']['frame']['roi']
    roi = roi_data['x'], roi_data['y'], roi_data['w'], roi_data['h']
    logger.info(f'roi: {roi}')
    return roi
