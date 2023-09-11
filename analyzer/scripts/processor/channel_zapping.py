import logging
import tempfile
import traceback
from typing import Dict, List

from scripts.config.config import get_setting_with_env
from scripts.connection.redis_pubsub import publish_msg
from scripts.format import VideoInfo
from scripts.external.data import load_input, read_analysis_config
from scripts.external.event import (get_channel_key_inputs,
                                    get_data_of_event_log)
from scripts.external.network import (get_data_of_network_log,
                                      get_igmp_join_infos)
from scripts.external.report import report_output
from scripts.external.progress import ProgressManager
from scripts.format import (ChannelZappingEventData, Command, IgmpJoinData,
                            RemoconKeyData, ReportName)
from scripts.util._timezone import get_utc_datetime
from scripts.util.decorator import log_decorator
from scripts.util.video import crop_video_with_opencv
from scripts.analysis.channel_zapping import calculate_channel_zapping

logger = logging.getLogger('main')


@log_decorator(logger)
def test_channel_zapping():
    try:
        args = load_input()
        config = get_config()
        task_channel_zapping(args, config)

        publish_msg({'measurement': Command.CHANNEL_ZAPPING.value}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': Command.CHANNEL_ZAPPING.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in test_channel_zapping: {err}")
        logger.warning(error_detail)


def task_channel_zapping(args: VideoInfo, config: Dict):
    progress_manager = ProgressManager(Command.CHANNEL_ZAPPING.value)

    network_log = get_data_of_network_log(args.timestamps[0], args.timestamps[-1])
    igmp_join_infos = get_igmp_join_infos(network_log)  # igmp join occured time

    event_log = get_data_of_event_log(args.timestamps[0], args.timestamps[-1])
    channel_key_inputs = get_channel_key_inputs(event_log, config['targets'])  # channel key: all number key, ok key, channelup key, channeldown key

    event_datas = get_channel_zapping_event_datas(igmp_join_infos, channel_key_inputs,
                                                    igmp_join_time_margin=get_setting_with_env('IGMP_JOIN_TIME_MARGIN', 5))

    with tempfile.TemporaryDirectory(dir='/tmp') as output_dir:

        crop_videos = crop_video_with_opencv(args.video_path, args.timestamps, [ei.event_time for ei in event_datas], 
                                             output_dir, get_setting_with_env('CHANNEL_ZAPPING_VIDEO_LENGTH', 8))
        for idx, (crop_video, event_info) in enumerate(zip(crop_videos, event_datas)):
            result = calculate_channel_zapping(crop_video.video_path, crop_video.timestamps, crop_video.timestamps[0],
                                               min_diff_rate=get_setting_with_env('CHANNEL_ZAPPING_MIN_DIFF_RATE', 0.00002))
            if result.status == 'success':
                report_output(ReportName.CHANNEL_ZAPPING.value, {
                    'timestamp': get_utc_datetime(event_info.event_time),
                    'measure_time': result.total,
                    'remocon_key': event_info.key,
                    'src_channel': event_info.src,
                    'dst_channel': event_info.dst,
                    'channel_name': event_info.channel_name,
                })
            progress_manager.update_progress(idx / len(crop_videos))


def get_config() -> Dict:
    return read_analysis_config()[Command.CHANNEL_ZAPPING.value]


# iterate all igmp join times.
# if any channel_key_input_time is between ('igmp join time - 5', 'igmp join time') 
#   -> valid key input time. accumulate last event info from igmp join time.
# else
#   -> invalid key input time. skip.
def get_channel_zapping_event_datas(igmp_join_infos: List[IgmpJoinData], channel_key_inputs: List[RemoconKeyData], 
                                    igmp_join_time_margin: int) -> List[ChannelZappingEventData]:
    # sorting is skipped because the data is already sorted by timestamp

    i, j = 0, 0
    n, m = len(igmp_join_infos), len(channel_key_inputs)

    event_datas = []

    while i < n and j < m:
        igmp_join = igmp_join_infos[i]
        channel_key_input = channel_key_inputs[j]
        
        last_fitting_input = None  # To keep track of the last fitting channel_key_input
        
        while j < m and channel_key_input.timestamp <= igmp_join.timestamp:
            if channel_key_input.timestamp >= igmp_join.timestamp - igmp_join_time_margin:
                last_fitting_input = channel_key_input  # Update last fitting input
                
            j += 1  # Move to next channel_key_input
            if j < m:
                channel_key_input = channel_key_inputs[j]
                
        if last_fitting_input is not None:  # If a fitting input was found, store it
            event_datas.append(ChannelZappingEventData(
                event_time=last_fitting_input.timestamp,
                key=last_fitting_input.key,
                src=igmp_join.src,
                dst=igmp_join.dst,
                channel_name=igmp_join.channel_info,
            ))
                            
        i += 1  # Move to next igmp_join

    logger.info(f'event datas: {event_datas}')
    return event_datas
