import logging
import traceback
from typing import Dict

from scripts.analysis.freeze_detect import FreezeDetector
from scripts.config.config import get_setting_with_env
from scripts.connection.redis_pubsub import publish_msg
from scripts.external.data import load_input, read_analysis_config
from scripts.external.report import report_output
from scripts.external.progress import ProgressManager
from scripts.format import Command, ReportName, VideoInfo
from scripts.util._timezone import get_utc_datetime
from scripts.util.common import seconds_to_time
from scripts.util.decorator import log_decorator
from scripts.util.video import FrameGenerator

logger = logging.getLogger('main')


@log_decorator(logger)
def test_freeze_detection():
    try:  
        args = load_input()
        config = get_config()

        task_freeze_detection(args, config)

        publish_msg({'measurement': Command.FREEZE.value}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': Command.FREEZE.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in detect_freeze postprocess: {err}")
        logger.warning(error_detail)


def task_freeze_detection(args: VideoInfo, config: Dict):
    progress_manager = ProgressManager(Command.FREEZE.value)
    freeze_detector = set_freeze_detector(args.fps, config['duration'])
    logger.info(f'start time: {get_utc_datetime(args.timestamps[0])}')

    for idx, (frame, cur_time) in enumerate(FrameGenerator(args.video_path, args.timestamps)):
        result = freeze_detector.update(frame, cur_time)
        if result['detect'] and result['duration'] > config['duration']:
            logger.info(f'relative time: {seconds_to_time(result["start_time"] - args.timestamps[0])}')
            report_output(ReportName.FREEZE.value, {
                'timestamp': get_utc_datetime(result['start_time']),
                'freeze_type': result['freeze_type'],
                'duration': result['duration'],
            })
        progress_manager.update_progress((idx + 1) / args.frame_count)


def set_freeze_detector(fps: float, min_duration: float) -> FreezeDetector:
    sampling_rate = get_setting_with_env('FREEZE_DETECT_SKIP_FRAME', 6)
    min_interval = min_duration
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


def get_config() -> Dict:
    analysis_config = read_analysis_config()
    config = analysis_config[Command.FREEZE.value]
    logger.info(f'config: {config}')
    return config
