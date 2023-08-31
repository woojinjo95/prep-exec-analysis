from datetime import datetime
import logging
from typing import List, Dict

from scripts.connection.mongo_db.crud import aggregate_from_mongodb
from scripts.external.scenario import get_scenario_info
from scripts.util._timezone import get_utc_datetime

logger = logging.getLogger('main')


def get_data_of_event_log(start_time: float, end_time: float):
    start_time = get_utc_datetime(start_time)
    end_time = get_utc_datetime(end_time)

    scenario_info = get_scenario_info()
    scenario_id = scenario_info['scenario_id']
    logger.info(f'get_data_of_event_log. scenario_id: {scenario_id}, start_time: {start_time}, end_time: {end_time}')
    
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


def get_power_key_times(event_result: Dict) -> List[float]:
    remocon_times = []
    for item in event_result.get('items', []):
        service = item.get('service', '')
        msg = item.get('msg', '')
        data = item.get('data', {})
        key = str(data.get('key', ''))
        if service == 'control' and msg == 'remocon_response' and key.lower() == 'power':
            try:
                sensor_time = data['sensor_time']
                remocon_times.append(sensor_time)
            except KeyError:
                pass
    logger.info(f'remocon_times: {remocon_times}')
    return remocon_times


def get_dut_power_times(event_result: Dict) -> List[float]:
    control_times = []
    for item in event_result.get('items', []):
        service = item.get('service', '')
        msg = item.get('msg', '')
        data = item.get('data', {})
        dut_power_transition = data.get('enable_dut_power_transition', '')
        if service == 'control' and msg == 'on_off_control_response' and dut_power_transition == 'rising':
            try:
                sensor_time = data['sensor_time']
                control_times.append(sensor_time)
            except KeyError:
                pass
    logger.info(f'control_times: {control_times}')
    return control_times
