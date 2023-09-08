import logging
import traceback

from scripts.util.decorator import log_decorator
from scripts.monkey.intelligent_monkey_test.roku import IntelligentMonkeyTestRoku
from scripts.monkey.intelligent_monkey_test.sk import IntelligentMonkeyTestSK
from scripts.monkey.monkey_test.default import MonkeyTest
from scripts.monkey.format import MonkeyArgs, RemoconInfo
from scripts.connection.redis_pubsub import publish_msg
from scripts.external.redis import get_monkey_test_arguments
from scripts.external.scenario import update_history


logger = logging.getLogger('main')


@log_decorator(logger)
def test_monkey():
    try:
        # redis 상에서 갱신된 환경 설정 정보를 가져옴. (sub으로 올 수도 있고, redis에서 직접 가져올 수도 있음.)
        # 현재는 dummy로 처리
        arguments = get_monkey_test_arguments()
        logger.info(f"arguments: {arguments}")

        arguments['interval'] /= 1000  # ms -> s
        analysis_type = arguments['type']
        if analysis_type == 'intelligent_monkey_test':
            profile = str(arguments['profile']).lower()

            if profile == 'roku':
                imt = IntelligentMonkeyTestRoku(
                    key_interval=arguments['interval'],
                    monkey_args=MonkeyArgs(
                        duration=arguments['duration_per_menu'],
                        enable_smart_sense=arguments['enable_smart_sense'],
                        waiting_time=arguments['waiting_time']
                    ),
                )
                imt.run()

            elif profile == 'skb':
                imt = IntelligentMonkeyTestSK(
                    key_interval=arguments['interval'],
                    monkey_args=MonkeyArgs(
                        duration=arguments['duration_per_menu'],
                        enable_smart_sense=arguments['enable_smart_sense'],
                        waiting_time=arguments['waiting_time']
                    ),
                )
                imt.run()

            else:
                raise NotImplementedError(f"invalid profile: {profile}")
            
        elif analysis_type == 'monkey_test':
            mt = MonkeyTest(
                key_interval=arguments['interval'],
                monkey_args=MonkeyArgs(
                    duration=arguments['duration'],
                    enable_smart_sense=arguments['enable_smart_sense'],
                    waiting_time=arguments['waiting_time']
                ),
                remocon_info=RemoconInfo(
                    remocon_name=arguments['remocon_name'],
                    remote_control_type=arguments['remote_control_type']
                )
            )
            mt.run()
            
        else:
            raise NotImplementedError(f"invalid analysis_type: {analysis_type}")

        publish_msg({'measurement': analysis_type}, 'monkey_response')
        update_history(analysis_type)

    except Exception as err:
        error_detail = traceback.format_exc()
        publish_msg({'measurement': analysis_type, 'log': error_detail}, 'monkey_response', level='error')
        logger.error(f"error in test_monkey: {err}")
        logger.warning(error_detail)
