import logging
import re
import traceback
from typing import Dict, List

from scripts.connection.redis_pubsub import publish_msg
from scripts.external.data import load_input, read_analysis_config
from scripts.external.log import get_data_of_log
from scripts.external.report import report_output
from scripts.external.progress import ProgressManager
from scripts.format import Command, ReportName, VideoInfo
from scripts.util.decorator import log_decorator

logger = logging.getLogger('main')


@log_decorator(logger)
def test_log_pattern_matching():
    try:
        args = load_input()
        config = get_config()

        task_log_pattern_matching(args, config)

        publish_msg({'measurement': Command.LOG_PATTERN_MATCHING.value}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': Command.LOG_PATTERN_MATCHING.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in match_log_pattern: {err}")
        logger.warning(error_detail)


def task_log_pattern_matching(args: VideoInfo, config: Dict):
    progress_manager = ProgressManager(Command.LOG_PATTERN_MATCHING.value)
    log_data = get_data_of_log(args.timestamps[0], args.timestamps[-1])
    # log_data = get_data_of_log(time.time() - 600, time.time() - 300)
    target_items = config['items']
    log_datas = log_data['items']

    count = 0
    for idx, log in enumerate(log_datas):
        matched_target = check_log_pattern_match(log, target_items)
        if matched_target:
            # logger.info(f'log: {log}')
            report_output(ReportName.LOG_PATTERN.value, {
                **log,
                'matched_target': matched_target
            })
            count += 1
        progress_manager.update_progress(idx / log_datas)
    logger.info(f'matched log count: {count}')


def get_config() -> Dict:
    analysis_config = read_analysis_config()
    config = analysis_config['log_pattern_matching']
    logger.info(f'config: {config}')
    return config


def check_pattern_match(msg: str, pattern: str) -> bool:
    found = re.search(pattern, msg)
    return True if found else False


# n개의 target 조건 중 하나라도 충족하면 True  -> 매칭된 타겟을 반환
def check_log_pattern_match(log: Dict, target_items: List[Dict]) -> Dict:
    log_level = log['log_level']
    log_msg = log['message']

    for target in target_items:
        target_level = target['level']
        target_re = target['regular_expression']
        if log_level == target_level and check_pattern_match(log_msg, target_re):
            return target
    return None
