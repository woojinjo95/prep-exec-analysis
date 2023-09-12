import logging
import traceback
from typing import Dict

from scripts.analysis.macroblock.detector import MacroblockDetector
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
def test_macroblock():
    try:  
        args = load_input()
        config = get_config()

        task_macroblock(args, config)

        publish_msg({'measurement': Command.MACROBLOCK.value}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': Command.MACROBLOCK.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in test_macroblock postprocess: {err}")
        logger.warning(error_detail)


def task_macroblock(args: VideoInfo, config: Dict):
    progress_manager = ProgressManager(Command.MACROBLOCK.value)
    continuity_set_thld = max(int(config['duration'] * args.fps), 1)
    detector = MacroblockDetector(score_thld=config['score_threshold'], 
                                  continuity_set_thld=continuity_set_thld)
    logger.info(f'start time: {get_utc_datetime(args.timestamps[0])}')

    for idx, (frame, cur_time) in enumerate(FrameGenerator(args.video_path, args.timestamps)):
        if idx % config['sampling_interval'] == 0:
            result = detector.update(frame, cur_time)
            if result.status == 'success' and result.detect and result.duration > config['duration']:
                logger.info(f'relative time: {seconds_to_time(result.start_time - args.timestamps[0])}')
                report_output(ReportName.MACROBLOCK.value, {
                    'timestamp': get_utc_datetime(result.start_time),
                    'duration': result.duration,
                })
            progress_manager.update_progress((idx + 1) / args.frame_count)


def get_config() -> Dict:
    analysis_config = read_analysis_config()
    config = analysis_config[Command.MACROBLOCK.value]
    logger.info(f'config: {config}')
    return config
