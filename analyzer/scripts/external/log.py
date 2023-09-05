import logging
from typing import Dict, List
from scripts.connection.mongo_db.crud import aggregate_from_mongodb
from scripts.external.scenario import get_scenario_info
from scripts.util._timezone import get_utc_datetime

logger = logging.getLogger('main')


def get_data_of_log(start_time: float, end_time: float) -> List[Dict]:
    start_time = get_utc_datetime(start_time)
    end_time = get_utc_datetime(end_time)
    scenario_info = get_scenario_info()
    scenario_id = scenario_info['scenario_id']
    logger.info(f'get_data_of_log_level_finder. scenario_id: {scenario_id}, start_time: {start_time}, end_time: {end_time}')

    log_pipeline = [
        {'$match': {'scenario_id': scenario_id,
                    'timestamp': {'$gte': start_time, '$lte': end_time}}},
        {'$project': {'_id': 0, 'lines': 1}},
        {'$unwind': {'path': '$lines'}},
        {'$project': {'timestamp': '$lines.timestamp', 
                      'module': '$lines.module',
                      'log_level': '$lines.log_level', 
                      'process_name': '$lines.process_name',
                      'pid': '$lines.pid',
                      'tid': '$lines.tid',
                      'message': '$lines.message'}}
    ]
    log_data = aggregate_from_mongodb(col='stb_log', pipeline=log_pipeline)
    logger.info(f'log count: {len(log_data)}')
    return {"items": log_data}
