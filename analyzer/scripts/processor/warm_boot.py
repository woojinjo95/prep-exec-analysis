import logging
import traceback
import tempfile

from scripts.format import CollectionName
from scripts.external.data import load_input, read_analysis_config, get_roi
from scripts.external.report import report_output
from scripts.connection.redis_pubsub import publish_msg
from scripts.util._timezone import get_utc_datetime
from scripts.util.video import crop_video_with_opencv
from scripts.external.event import get_data_of_event_log, get_power_key_times
from scripts.config.config import get_setting_with_env
from scripts.analysis.boot_test.diff import task_boot_test_with_diff
from scripts.analysis.boot_test.match import task_boot_test_with_match
from scripts.util.decorator import log_decorator
from scripts.analysis.video import check_poweroff_video

logger = logging.getLogger('boot_test')


@log_decorator(logger)
def test_warm_boot():
    try:
        analysis_config = read_analysis_config()
        processing_mode = analysis_config['resume']['type']
        if processing_mode == 'image_matching':
            test_warm_boot_with_match()
        elif processing_mode == 'screen_change_rate':
            test_warm_boot_with_diff()

        publish_msg({'measurement': ['resume']}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': ['resume']}, error_detail, level='error')
        logger.error(f"error in test_warm_boot: {err}")
        logger.warning(error_detail)


def test_warm_boot_with_diff():
    args = load_input()

    event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
    remocon_times = get_power_key_times(event_log)
    logger.info(f'remocon_times: {remocon_times}')

    with tempfile.TemporaryDirectory(dir='/tmp') as output_dir:
        warm_boot_results = []
        crop_videos = crop_video_with_opencv(args.video_path, args.timestamps, remocon_times, output_dir, get_setting_with_env('WARM_BOOT_DURATION', 10))
        for crop_video in crop_videos:
            if not check_poweroff_video(crop_video.video_path):
                continue
            result = task_boot_test_with_diff(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0])
            logger.info(f'result: {result}')
            warm_boot_results.append(result)

    for result in warm_boot_results:
        if result['status'] == 'success':
            report_output(CollectionName.WARM_BOOT.value, {
                'timestamp': get_utc_datetime(result['diff_timestamp']),
                'measure_time': result['diff_time'],
            })


def test_warm_boot_with_match():
    args = load_input()
    roi = get_roi()
    logger.info(f'roi: {roi}')

    event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
    remocon_times = get_power_key_times(event_log)
    logger.info(f'remocon_times: {remocon_times}')

    with tempfile.TemporaryDirectory(dir='/tmp') as output_dir:
        warm_boot_results = []
        crop_videos = crop_video_with_opencv(args.video_path, args.timestamps, remocon_times, output_dir, get_setting_with_env('WARM_BOOT_DURATION', 10))
        for crop_video in crop_videos:
            if not check_poweroff_video(crop_video.video_path):
                continue
            result = task_boot_test_with_match(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0])
            logger.info(f'result: {result}')
            warm_boot_results.append(result)

    for result in warm_boot_results:
        if result['status'] == 'success':
            report_output(CollectionName.WARM_BOOT.value, {
                'timestamp': get_utc_datetime(result['diff_timestamp']),
                'measure_time': result['diff_time'],
            })