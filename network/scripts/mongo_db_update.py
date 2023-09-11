import datetime
import logging
import time
import traceback
from multiprocessing import Event, Queue, queues
from typing import Dict

from .capture.parser import get_packet_info
from .analysis.packet_analyzer.protocols.enum import convert_protocol_enum_to_str
from .configs.config import get_value
from .configs.constant import RedisDBEnum
from .connection.mongo_db.create import insert_to_mongodb
from .utils._multi_process import ProcessMaintainer
from .utils._timezone import get_utc_datetime

logger = logging.getLogger('mongodb')


def get_testrun_info() -> Dict[str, str]:
    all_testrun_info = get_value('testrun', db=RedisDBEnum.hardware)

    testrun_info = {'scenario_id': all_testrun_info.get('scenario_id', 'unknown'),
                    'testrun_id': all_testrun_info.get('id', 'unknown'),
                    }

    return testrun_info


def format_subscribed_log(subscribed_log: Dict) -> Dict:
    data = {'timestamp': get_utc_datetime(subscribed_log.get('time', time.time())),
            'src': subscribed_log.get('src', ''),
            'dst': subscribed_log.get('dst', ''),
            'protocol': convert_protocol_enum_to_str(subscribed_log.get('protocol', '')),
            'length': subscribed_log.get('length', 0),
            'info': subscribed_log.get('info', ''),
            }

    if subscribed_log.get('metadata'):
        data.update({'metadata': subscribed_log.get('metadata')})

    return data


class InsertToMongoDB:

    def __init__(self):
        self.log_queue = Queue()

        self.proc = ProcessMaintainer(func=self.consume, daemon=True, revive_interval=1)
        self.proc.start()

    def init_document(self, log_time: datetime.datetime, line: dict) -> Dict:
        document = {'timestamp': log_time.replace(microsecond=0),
                    **get_testrun_info(),
                    'lines': [line]}
        return document

    def put(self, log: dict):
        # add filter
        # if log.get('msg') in target_msg:
        if True:
            # logger.info(log)
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
                    insert_to_mongodb('network_trace', document)
                    document = self.init_document(log_time, format_subscribed_log(log))

            except queues.Empty:
                if document is not None:
                    # 1초가 지나고 document가 비지 않으면 업데이트
                    # logger.info(f'Timeout for 1 second and update to mongodb')
                    insert_to_mongodb('network_trace', document)
                    document = None

            except Exception as e:
                logger.error(f'Comsumeing log to upload mongodb failed: {e}')
                logger.info(traceback.format_exc())
                # drop too many erros
                time.sleep(0.5)


class PacketMongoSession(InsertToMongoDB):

    def __init__(self):
        super().__init__()

    def put_network_trace(self, timestamp: float, packet: bytes = None, info: str = '', metadata={}):

        data = {'time': timestamp,
                'info': info,
                }

        if packet is not None:
            src, dst, protocol, length = get_packet_info(packet)
            data.update({'src': src,
                         'dst': dst,
                         'protocol': protocol,
                         'length': length,
                         })
            if metadata:
                data.update({'metadata': metadata})

        else:
            pass

        # logger.info(data)
        super().put(data)
