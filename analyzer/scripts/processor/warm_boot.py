import logging
import tempfile
import traceback
from typing import Tuple, Dict

import cv2
import numpy as np
from scripts.analysis.boot_test.diff import task_boot_test_with_diff
from scripts.analysis.boot_test.match import task_boot_test_with_match
from scripts.analysis.video import check_poweroff_video
from scripts.config.config import get_setting_with_env
from scripts.connection.redis_pubsub import publish_msg
from scripts.external.data import load_input, read_analysis_config
from scripts.external.event import get_data_of_event_log, get_power_key_times
from scripts.external.report import report_output
from scripts.external.progress import ProgressManager
from scripts.format import Command, ReportName, VideoInfo
from scripts.util._timezone import get_utc_datetime
from scripts.util.decorator import log_decorator
from scripts.util.video import crop_video_with_opencv

logger = logging.getLogger('main')


@log_decorator(logger)
def test_warm_boot():
    try:
        args = load_input()
        config = get_config()

        processing_mode = config['type']
        logger.info(f'processing_mode: {processing_mode}')
        if processing_mode == 'image_matching':
            task_warm_boot_with_match(args, config)
        elif processing_mode == 'screen_change_rate':
            task_warm_boot_with_diff(args)

        publish_msg({'measurement': Command.RESUME.value}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': Command.RESUME.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in test_warm_boot: {err}")
        logger.warning(error_detail)


def task_warm_boot_with_diff(args: VideoInfo):
    progress_manager = ProgressManager(Command.RESUME.value)
    event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
    remocon_times = get_power_key_times(event_log)

    with tempfile.TemporaryDirectory(dir='/tmp') as output_dir:
        crop_videos = crop_video_with_opencv(args.video_path, args.timestamps, remocon_times, output_dir, get_setting_with_env('WARM_BOOT_DURATION', 10))
        for idx, crop_video in enumerate(crop_videos):
            if not check_poweroff_video(crop_video.video_path):
                continue
            result = task_boot_test_with_diff(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0])
            if result['status'] == 'success':
                report_output(ReportName.WARM_BOOT.value, {
                    'timestamp': get_utc_datetime(result['diff_timestamp']),
                    'measure_time': result['diff_time'],
                })
            progress_manager.update_progress(idx / len(crop_videos))


def task_warm_boot_with_match(args: VideoInfo, config: Dict):
    progress_manager = ProgressManager(Command.RESUME.value)
    template, roi = get_template_info(config)
    event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
    remocon_times = get_power_key_times(event_log)

    with tempfile.TemporaryDirectory(dir='/tmp') as output_dir:
        crop_videos = crop_video_with_opencv(args.video_path, args.timestamps, remocon_times, output_dir, get_setting_with_env('WARM_BOOT_DURATION', 10))
        for idx, crop_video in enumerate(crop_videos):
            if not check_poweroff_video(crop_video.video_path):
                continue
            result = task_boot_test_with_match(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0],
                                               roi, template, roi)
            if result['status'] == 'success':
                report_output(ReportName.WARM_BOOT.value, {
                    'timestamp': get_utc_datetime(result['match_timestamp']),
                    'measure_time': result['match_time'],
                })
            progress_manager.update_progress((idx + 1) / len(crop_videos))


def get_config() -> Dict:
    analysis_config = read_analysis_config()
    config = analysis_config[Command.RESUME.value]
    logger.info(f'config: {config}')
    return config


def get_template_info(config) -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
    template = cv2.imread(config['frame']['path'])
    roi_data = config['frame']['roi']
    roi = (roi_data['x'], roi_data['y'], roi_data['w'], roi_data['h'])
    logger.info(f'template shape: {template.shape}, roi: {roi}')
    return template, roi