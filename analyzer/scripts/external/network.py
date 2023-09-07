import logging
from typing import Dict, List

from scripts.connection.mongo_db.crud import aggregate_from_mongodb
from scripts.external.scenario import get_scenario_info
from scripts.util._timezone import get_utc_datetime
from scripts.format import IgmpJoinData

logger = logging.getLogger('main')


def get_data_of_network_log(start_time: float, end_time: float):
    start_time = get_utc_datetime(start_time)
    end_time = get_utc_datetime(end_time)

    scenario_info = get_scenario_info()
    scenario_id = scenario_info['scenario_id']
    logger.info(f'get_data_of_network_log. scenario_id: {scenario_id}, start_time: {start_time}, end_time: {end_time}')
    
    pipeline = [
        {'$match': {'scenario_id': scenario_id,
                    'timestamp': {'$gte': start_time,
                                  '$lte': end_time}}},
        {'$project': {'_id': 0, 'lines': 1}},
        {'$unwind': {'path': '$lines'}},
        {'$replaceRoot': {'newRoot': '$lines'}}
    ]
    event_log = aggregate_from_mongodb(col='network_trace', pipeline=pipeline)
    return {"items": event_log}


def get_igmp_join_infos(event_result: Dict) -> List[IgmpJoinData]:
    igmp_join_infos = []
    for item in event_result.get('items', []):
        src = item.get('src', '')
        dst = item.get('dst', '')
        meta_data = item.get('metadata', {})
        type = meta_data.get('type', '')
        if type == 'igmp_join':
            try:
                igmp_join_infos.append(IgmpJoinData(
                    timestamp=meta_data['timestamp'],  # required
                    src=src,
                    dst=dst,
                    channel_info=meta_data.get('channel_info', '')
                ))
            except KeyError:
                pass
    logger.info(f'igmp_join_infos: {igmp_join_infos}')
    return igmp_join_infos
