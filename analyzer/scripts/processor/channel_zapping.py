import logging
import tempfile
import traceback
from typing import Dict

from scripts.config.config import get_setting_with_env
from scripts.connection.redis_pubsub import publish_msg
from scripts.external.data import load_input, read_analysis_config
from scripts.external.event import get_data_of_event_log, get_channel_key_inputs
from scripts.external.network import get_data_of_network_log, get_igmp_join_infos
from scripts.external.report import report_output
from scripts.external.analysis import set_analysis_info
from scripts.format import Command, ReportName
from scripts.util._timezone import get_utc_datetime
from scripts.util.decorator import log_decorator
from scripts.util.video import crop_video_with_opencv

logger = logging.getLogger('main')


@log_decorator(logger)
def test_channel_zapping():
    try:
        measure_channel_zapping()

        publish_msg({'measurement': Command.CHANNEL_ZAPPING.value}, 'analysis_response')
        set_analysis_info(Command.CHANNEL_ZAPPING.value)

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': Command.CHANNEL_ZAPPING.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in test_channel_zapping: {err}")
        logger.warning(error_detail)


def measure_channel_zapping():
    args = load_input()
    config = get_config()
    targets = config['targets']  # ['adjoint_channel', 'non_adjoint_channel']

    network_log = get_data_of_network_log(args.timestamps[0], args.timestamps[-1])
    igmp_join_infos = get_igmp_join_infos(network_log)  # igmp join occured time

    event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
    channel_key_inputs = get_channel_key_inputs(event_log)  # channel key: all number key, ok key, channelup key, channeldown key

    # iterate all igmp join times.
    # if any channel_key_input_time is between ('igmp join time - 5', 'igmp join time') 
    #   -> valid key input time. and accumulate 'channel key event time' and 'event key' and meta info(src ch num, dst ch num)
    #   -> accumulate key along to adj or non adj
    # else
    #   -> invalid key input time. skip.
    event_times = get_channel_zapping_event_times(igmp_join_infos, channel_key_inputs, targets)

    with tempfile.TemporaryDirectory(dir='/tmp') as output_dir:

        crop_videos = crop_video_with_opencv(args.video_path, args.timestamps, event_times, output_dir, get_setting_with_env('CHANNEL_ZAPPING_VIDEO_LENGTH', 8))
        for crop_video in crop_videos:
            result = task_channel_zapping(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0])

            if result['status'] == 'success':
                report_output(ReportName.CHANNEL_ZAPPING.value, {
                    'timestamp': get_utc_datetime(result['measure_timestamp']),
                    'measure_time': result['measure_time'],
                })


def get_config() -> Dict:
    return read_analysis_config()['channel_change_time']
