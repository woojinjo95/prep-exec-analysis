import logging
import traceback
import os
import shutil

from scripts.format import CollectionName
from scripts.external.data import load_input
from scripts.external.report import report_output
from scripts.connection.redis_pubsub import publish_msg
from scripts.util._timezone import get_utc_datetime
from scripts.util.video import crop_video_with_timestamps
from scripts.external.event import get_data_of_event_log, get_remocon_times
from scripts.config.config import get_setting_with_env
from scripts.analysis.boot_test.diff import task_boot_test_with_diff
from scripts.util.decorator import log_decorator

logger = logging.getLogger('boot_test')


@log_decorator(logger)
def test_warm_boot():
    try:  
        args = load_input()

        event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
        # logger.info(f'event_log: {event_log}')
        remocon_times = get_remocon_times(event_log)
        logger.info(f'remocon_times: {remocon_times}')

        output_dir = os.path.join('/tmp', 'video', 'warm_boot')
        crop_videos = crop_video_with_timestamps(args.video_path, args.timestamps, remocon_times, output_dir, get_setting_with_env('WARM_BOOT_DURATION', 10))
        for crop_video in crop_videos:
            result = task_boot_test_with_diff(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0])
            logger.info(f'result: {result}')
        shutil.rmtree(output_dir)

        publish_msg({'measurement': ['resume']}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': ['resume']}, error_detail, level='error')
        logger.error(f"error in test_warm_boot: {err}")
        logger.warning(error_detail)
