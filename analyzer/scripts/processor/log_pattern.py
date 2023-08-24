import logging
from typing import List
import time
from scripts.external.data import load_input
from scripts.external.log import get_data_of_log
from scripts.util.decorator import log_decorator
from scripts.external.data import load_input, read_analysis_config
from scripts.external.report import report_output
from scripts.format import CollectionName
from scripts.util._timezone import get_utc_datetime

logger = logging.getLogger('log_pattern')


@log_decorator(logger)
def match_log_pattern():
    args = load_input()
    # log_data = get_data_of_log(args.timestamps[0], args.timestamps[-1])
    log_data = get_data_of_log(time.time() - 180, time.time())

    target_levels = get_target_level_from_config()
    # for log in log_data['items']:
    #     if log['log_level'] in target_levels:
    #         logger.info(f'log: {log}')
    #         # report_output(CollectionName.LOG_LEVEL.value, {
    #         #     'timestamp': get_utc_datetime(log['timestamp'].timestamp()),
                
    #         # })


def get_target_level_from_config() -> List[str]:
    analysis_config = read_analysis_config()
    target_item = analysis_config['log_pattern_matching']['items']
    logger.info(f'target_item: {target_item}')
    return target_item
