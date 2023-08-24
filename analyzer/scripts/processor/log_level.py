import logging
from scripts.external.data import load_input
from scripts.external.log import get_data_of_log_level_finder
from scripts.util.decorator import log_decorator


logger = logging.getLogger('log_level')


@log_decorator(logger)
def parse_log_level():
    args = load_input()
    log_data = get_data_of_log_level_finder(args.timestamps[0], args.timestamps[-1])
    # target_levels = load_target_level()
    # for log in log_data:
    #     if log['level'] in target_levels:
    #         publish(log)
