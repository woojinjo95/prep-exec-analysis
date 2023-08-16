import logging
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from typing import Dict

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.util._timezone import get_utc_datetime
from scripts.config.mongo import get_scenario_id


logger = logging.getLogger('color_reference')


def postprocess():
    logger.info(f"start color_reference postprocess")

    scheduler = BlockingScheduler()
    scheduler.add_job(insert_to_db, 'interval', args=[], seconds=10)
    scheduler.start()


def insert_to_db():
    json_data = construct_json_data()
    logger.info(f'insert {json_data} to db')
    insert_to_mongodb('color_reference', json_data)


def construct_json_data() -> Dict:
    return {
        'scenario_id': get_scenario_id(),
        'timestamp': get_utc_datetime(time.time()),
    }
 