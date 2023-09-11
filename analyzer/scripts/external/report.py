from typing import Dict
import time
import logging

from scripts.util._timezone import get_utc_datetime
from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.external.scenario import get_scenario_info
from scripts.format import CollectionName, ReportName, Command
from scripts.external.data import read_analysis_config

logger = logging.getLogger('main')


report_info = {
    ReportName.COLOR_REFERENCE.value: {
        'col_name': CollectionName.COLOR_REFERENCE.value,
    },
    ReportName.FREEZE.value: {
        'col_name': CollectionName.FREEZE.value,  # collection name for mongo db
        'user_config_name': Command.FREEZE.value  # user config name for redis (analysis_config/analysis_config:freeze)
    },
    ReportName.WARM_BOOT.value: {
        'col_name': CollectionName.WARM_BOOT.value,
        'user_config_name': Command.RESUME.value
    },
    ReportName.COLD_BOOT.value: {
        'col_name': CollectionName.COLD_BOOT.value,
        'user_config_name': Command.BOOT.value
    },
    ReportName.LOG_PATTERN.value: {
        'col_name': CollectionName.LOG_PATTERN.value,
        'user_config_name': Command.LOG_PATTERN_MATCHING.value
    },
    ReportName.CHANNEL_ZAPPING.value: {
        'col_name': CollectionName.CHANNEL_ZAPPING.value,
        'user_config_name': Command.CHANNEL_ZAPPING.value
    },
}


def construct_report_data() -> Dict:
    scenario_info = get_scenario_info()
    return {
        'scenario_id': scenario_info['scenario_id'],
        'testrun_id': scenario_info['testrun_id'],
        'timestamp': get_utc_datetime(time.time()),
    }


def report_output(name: str, additional_data: Dict):
    try:
        col_name = report_info[name]['col_name']
    except KeyError:
        raise Exception(f'invalid report name: {name}')
    
    try:
        user_config_name = report_info[name]['user_config_name']
        analysis_config = read_analysis_config()
        user_config = analysis_config[user_config_name]
    except Exception:
        user_config = {}
    
    additional_data.update({'user_config': user_config})
    report = {**construct_report_data(), **additional_data}
    logger.info(f'insert {report} to db')
    insert_to_mongodb(col_name, report)
