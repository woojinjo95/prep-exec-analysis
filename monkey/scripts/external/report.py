import logging
import time
from typing import Dict
from uuid import uuid4

import numpy as np
from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.external.image import save_image
from scripts.external.redis import get_monkey_test_arguments
from scripts.external.scenario import get_scenario_info
from scripts.util._timezone import get_utc_datetime

logger = logging.getLogger('main')


def construct_report_data() -> Dict:
    scenario_info = get_scenario_info()
    return {
        'scenario_id': scenario_info['scenario_id'],
        'testrun_id': scenario_info['testrun_id'],
        'timestamp': get_utc_datetime(time.time()),
    }


def report_data(col_name: str, data: Dict):
    report = {**construct_report_data(), **data}
    logger.info(f'insert {report} to db')
    insert_to_mongodb(col_name, report)


def report_section(start_time: float, end_time: float, analysis_type: str, section_id: int, image: np.ndarray, smart_sense_times: int):
    if image is not None:
        image_name = get_utc_datetime(time.time()).strftime('%y-%m-%d %H:%M:%S')
        image_path = save_image(image_name, image)
        insert_to_mongodb('file', {'id': str(uuid4()), "name": f'{image_name}.png', "path": image_path})
    else:
        image_path = ''

    report_data('monkey_section', {
        'start_timestamp': get_utc_datetime(start_time),
        'end_timestamp': get_utc_datetime(end_time),
        'analysis_type': analysis_type,
        'section_id': section_id,
        'image_path': image_path,
        'smart_sense_times': smart_sense_times,
        'user_config': get_monkey_test_arguments()
    })
