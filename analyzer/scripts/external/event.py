import logging
from typing import List, Dict

from scripts.config.constant import POWER_KEY_NAMES, CHANNEL_KEY_ADJOINT_CANDIDATES, CHANNEL_KEY_NON_ADJOINT_CANDIDATES
from scripts.connection.mongo_db.crud import aggregate_from_mongodb
from scripts.external.scenario import get_scenario_info
from scripts.util._timezone import get_utc_datetime
from scripts.format import RemoconKeyData

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
        key = str(data.get('key', '')).lower()
        if service == 'control' and msg == 'remocon_response' and key in POWER_KEY_NAMES:
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


# targets: ['adjoint_channel', 'non_adjoint_channel']
def get_channel_key_inputs(event_result: Dict, targets: List[str]) -> List[RemoconKeyData]:
    remocon_infos = []
    for item in event_result.get('items', []):
        service = item.get('service', '')
        msg = item.get('msg', '')
        data = item.get('data', {})
        key = str(data.get('key', '')).lower()
        if service == 'control' and msg == 'remocon_response':
            if 'adjoint_channel' in targets and key in CHANNEL_KEY_ADJOINT_CANDIDATES or \
                'non_adjoint_channel' in targets and key in CHANNEL_KEY_NON_ADJOINT_CANDIDATES:
                try:
                    remocon_infos.append(RemoconKeyData(
                        timestamp=data['sensor_time'],
                        key=key
                    ))
                except KeyError:
                    pass
    logger.info(f'remocon_infos: {remocon_infos}')
    return remocon_infos
