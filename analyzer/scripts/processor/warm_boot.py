import logging
import tempfile
import traceback
from typing import Tuple
import numpy as np
import cv2

from scripts.analysis.boot_test.diff import task_boot_test_with_diff
from scripts.analysis.boot_test.match import task_boot_test_with_match
from scripts.analysis.video import check_poweroff_video
from scripts.config.config import get_setting_with_env
from scripts.connection.redis_pubsub import publish_msg
from scripts.external.data import load_input, read_analysis_config
from scripts.external.event import get_data_of_event_log, get_power_key_times
from scripts.external.report import report_output
from scripts.format import ReportName
from scripts.util._timezone import get_utc_datetime
from scripts.util.decorator import log_decorator
from scripts.util.video import crop_video_with_opencv
from scripts.format import LogName, Command

logger = logging.getLogger(LogName.BOOT_TEST.value)


@log_decorator(logger)
def test_warm_boot():
    try:
        analysis_config = read_analysis_config()
        # logger.info(f'analysis_config: {analysis_config}')
        processing_mode = analysis_config['resume']['type']
        logger.info(f'processing_mode: {processing_mode}')
        if processing_mode == 'image_matching':
            test_warm_boot_with_match()
        elif processing_mode == 'screen_change_rate':
            test_warm_boot_with_diff()

        publish_msg({'measurement': [Command.RESUME.value]}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': [Command.RESUME.value], 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in test_warm_boot: {err}")
        logger.warning(error_detail)


def test_warm_boot_with_diff():
    args = load_input()

    event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
    remocon_times = get_power_key_times(event_log)
    # remocon_times = [1692673582.4239447, 1692673592.3466334, 1692673696.58994, 1692673703.0160654]

    with tempfile.TemporaryDirectory(dir='/tmp') as output_dir:
        warm_boot_results = []
        crop_videos = crop_video_with_opencv(args.video_path, args.timestamps, remocon_times, output_dir, get_setting_with_env('WARM_BOOT_DURATION', 10))
        for crop_video in crop_videos:
            if not check_poweroff_video(crop_video.video_path):
                continue
            result = task_boot_test_with_diff(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0])
            warm_boot_results.append(result)

    for result in warm_boot_results:
        if result['status'] == 'success':
            report_output(ReportName.WARM_BOOT.value, {
                'timestamp': get_utc_datetime(result['diff_timestamp']),
                'measure_time': result['diff_time'],
            })


def test_warm_boot_with_match():
    args = load_input()
    template = get_template_from_config()
    roi = get_roi_from_config()

    event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
    remocon_times = get_power_key_times(event_log)
    # remocon_times = [1692673582.4239447, 1692673592.3466334, 1692673696.58994, 1692673703.0160654]

    with tempfile.TemporaryDirectory(dir='/tmp') as output_dir:
        warm_boot_results = []
        crop_videos = crop_video_with_opencv(args.video_path, args.timestamps, remocon_times, output_dir, get_setting_with_env('WARM_BOOT_DURATION', 10))
        for crop_video in crop_videos:
            if not check_poweroff_video(crop_video.video_path):
                continue
            result = task_boot_test_with_match(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0],
                                               roi, template, roi)
            warm_boot_results.append(result)

    for result in warm_boot_results:
        if result['status'] == 'success':
            report_output(ReportName.WARM_BOOT.value, {
                'timestamp': get_utc_datetime(result['match_timestamp']),
                'measure_time': result['match_time'],
            })


def get_template_from_config() -> np.ndarray:
    analysis_config = read_analysis_config()
    image_path = analysis_config['resume']['frame']['path']
    image = cv2.imread(image_path)
    logger.info(f'image shape: {image.shape}')
    return image


def get_roi_from_config() -> Tuple[int, int, int, int]:
    analysis_config = read_analysis_config()
    roi_data = analysis_config['resume']['frame']['roi']
    roi = roi_data['x'], roi_data['y'], roi_data['w'], roi_data['h']
    logger.info(f'roi: {roi}')
    return roi
