import logging
from typing import Dict, List
from scripts.connection.mongo_db.crud import aggregate_from_mongodb
from scripts.external.scenario import get_scenario_info
from scripts.util._timezone import get_utc_datetime

logger = logging.getLogger('connection')


def get_data_of_log_level_finder(start_time: float, end_time: float) -> List[Dict]:
    start_time = get_utc_datetime(start_time)
    end_time = get_utc_datetime(end_time)
    scenario_info = get_scenario_info()
    scenario_id = scenario_info['scenario_id']
    logger.info(f'get_data_of_log_level_finder. scenario_id: {scenario_id}, start_time: {start_time}, end_time: {end_time}')

    log_level_finder_pipeline = [
        {'$match': {'scenario_id': scenario_id,
                    'timestamp': {'$gte': start_time, '$lte': end_time}}},
        {'$project': {'_id': 0, 'lines': 1}},
        {'$unwind': {'path': '$lines'}},
        {'$project': {'timestamp': '$lines.timestamp', 'log_level': '$lines.log_level'}}
    ]
    log_level_finder = aggregate_from_mongodb(col='stb_log', pipeline=log_level_finder_pipeline)
    logger.info(f'log_level_finder: {log_level_finder}')
    return {"items": log_level_finder}
