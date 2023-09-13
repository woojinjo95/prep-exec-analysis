import logging
import time
from typing import Dict

from scripts.connection.mongo_db.crud import insert_to_mongodb, load_by_id_from_mongodb, update_by_id_to_mongodb
from scripts.external.scenario import get_scenario_info
from scripts.util._timezone import get_utc_datetime
from scripts.format import SectionData

logger = logging.getLogger('main')


def construct_report_data() -> Dict:
    scenario_info = get_scenario_info()
    return {
        'scenario_id': scenario_info['scenario_id'],
        'testrun_id': scenario_info['testrun_id'],
        'timestamp': get_utc_datetime(time.time()),
    }


def report_data(col_name: str, data: Dict) -> str:
    report = {**construct_report_data(), **data}
    logger.info(f'insert {report} to db')
    res = insert_to_mongodb(col_name, report)
    return res.inserted_id


def create_section(section_data: SectionData) -> str:
    return report_data('monkey_section', section_data.__dict__)


def update_section(id: str, section_in: SectionData):
    section_data = load_by_id_from_mongodb(col='monkey_section', id=id)
    if not section_data:
        raise Exception(f'The section with this id does not exist in the system: {id}')
    
    data_to_update = {key: value for key, value in section_in.__dict__.items() if value is not None}
    if data_to_update:
        logger.info(f'update section {id} with data {data_to_update}')
        update_by_id_to_mongodb(col='monkey_section', id=id, data=data_to_update)
