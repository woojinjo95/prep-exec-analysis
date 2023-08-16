import datetime
import logging
import time
import traceback
from multiprocessing import Event, Queue, queues
from typing import Dict

from .configs.config import get_value
from .configs.constant import RedisDBEnum
from .connection.mongo_db.create import insert_to_mongodb
from .utils._multi_process import ProcessMaintainer
from .utils._timezone import get_utc_datetime

logger = logging.getLogger('mongodb')


def get_scenario_id() -> str:
    scenario_id = get_value('testrun', 'scenario_id', '', db=RedisDBEnum.hardware)
    return scenario_id


def format_subscribed_log(subscribed_log: Dict):
    return {'timestamp': get_utc_datetime(subscribed_log.get('time', time.time())),
            'service': subscribed_log.get('service', 'Unknown'),
            'msg': subscribed_log.get('msg', 'Unknown'),
            'data': subscribed_log.get('data', {})}


class InsertToMongoDB:

    def __init__(self):
        self.log_queue = Queue()

        self.proc = ProcessMaintainer(func=self.consume, daemon=True, revive_interval=1)
        self.proc.start()

    def init_document(self, log_time: datetime.datetime, line: dict) -> Dict:
        document = {'timestamp': log_time.replace(microsecond=0),
                    'scenario_id': get_scenario_id(),
                    'lines': [line]}
        return document

    def put(self, log: dict):
        # add filter
        # if log.get('msg') in target_msg:
        if True:
            self.log_queue.put(log)

    def consume(self, stop_event: Event, run_state_event: Event):
        document = None

        while not stop_event.is_set():
            try:
                log = self.log_queue.get(timeout=1)
                log_time = get_utc_datetime(log.get('time', time.time()))

                if document is None:
                    # document가 없음
                    document = self.init_document(log_time, format_subscribed_log(log))
                elif document['timestamp'].second == log_time.second:
                    # 이미 document가 있고 추가된 로그도 같은 초
                    document['lines'].append(format_subscribed_log(log))
                else:
                    # 이미 document가 있고 로그 초는 늘어남
                    insert_to_mongodb('event_log', document)
                    document = self.init_document(log_time, format_subscribed_log(log))

            except queues.Empty:
                if document is not None:
                    # 1초가 지나고 document가 비지 않으면 업데이트
                    logger.info(f'Timeout for 1 second and update to mongodb')
                    insert_to_mongodb('event_log', document)
                    document = None

            except Exception as e:
                logger.error(f'Comsumeing log to upload mongodb failed: {e}')
                logger.info(traceback.format_exc())
