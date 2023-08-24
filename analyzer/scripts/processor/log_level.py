import logging
from typing import List
from scripts.external.data import load_input
from scripts.external.log import get_data_of_log_level_finder
from scripts.util.decorator import log_decorator
from scripts.external.data import load_input, read_analysis_config


logger = logging.getLogger('log_level')


@log_decorator(logger)
def parse_log_level():
    args = load_input()
    log_data = get_data_of_log_level_finder(args.timestamps[0], args.timestamps[-1])

    target_levels = get_target_level_from_config()
    for log in log_data:
        if log['log_level'] in target_levels:
            logger.info(f'{log["timestamp"]}, {log["log_level"]}')


def get_target_level_from_config() -> List[str]:
    analysis_config = read_analysis_config()
    target_levels = analysis_config['log_level_finder']['targets']
    logger.info(f'target_levels: {target_levels}')
    return target_levels
