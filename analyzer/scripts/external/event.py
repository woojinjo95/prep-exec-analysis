from datetime import datetime
import logging

from scripts.connection.mongo_db.crud import aggregate_from_mongodb
from scripts.external.scenario import get_scenario_info

logger = logging.getLogger('connection')


def get_data_of_event_log(start_time: datetime, end_time: datetime):
    scenario_info = get_scenario_info()
    scenario_id = scenario_info['scenario_id']
    logger.info(f'scenario_id: {scenario_id}, start_time: {start_time}, end_time: {end_time}')
    
    event_log_pipeline = [
        {'$match': {'scenario_id': scenario_id,
                    'timestamp': {'$gte': start_time,
                                  '$lte': end_time}}},
        {'$project': {'_id': 0, 'lines': 1}},
        {'$unwind': {'path': '$lines'}},
        {'$replaceRoot': {'newRoot': '$lines'}}
    ]
    event_log = aggregate_from_mongodb(col='event_log', pipeline=event_log_pipeline)
    return {"items": event_log}
