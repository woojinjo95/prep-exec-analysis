import logging
import traceback
import os

from scripts.format import CollectionName
from scripts.external.data import load_input
from scripts.external.report import report_output
from scripts.connection.redis_pubsub import publish_msg
from scripts.util._timezone import get_utc_datetime
from scripts.util.video import FrameGenerator, crop_video
from scripts.external.event import get_data_of_event_log, get_remocon_times
from scripts.config.config import get_setting_with_env

logger = logging.getLogger('boot_test')


def test_warm_boot():
    try:
        logger.info(f"start test_warm_boot process")        
        args = load_input()

        event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
        remocon_times = get_remocon_times(event_log)
        logger.info(f'remocon_times: {remocon_times}')

        tmp_dir = os.path.join('/tmp', 'video', 'warm_boot')
        os.makedirs(tmp_dir, exist_ok=True)
        cropped_videos = []
        for remocon_time in remocon_times:
            cropped_video_path = os.path.join(tmp_dir, f'{remocon_time}.mp4')
            crop_video(video_path=args.video_path,
                        output_path=cropped_video_path,
                        start_time=remocon_time,
                        end_time=remocon_time + get_setting_with_env('WARM_BOOT_DURATION', 10))
            cropped_videos.append(cropped_video_path)

        

        # publish_msg({'measurement': ['freeze']}, 'analysis_response')
        logger.info(f"end test_warm_boot process")

    except Exception as err:
        error_detail = traceback.format_exc()
        # publish_msg({'measurement': ['freeze']}, error_detail, level='error')
        logger.error(f"error in test_warm_boot: {err}")
        logger.warning(error_detail)
