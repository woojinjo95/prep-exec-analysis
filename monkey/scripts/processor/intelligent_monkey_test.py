import logging
import traceback
from typing import Dict

from scripts.util.decorator import log_decorator
from scripts.monkey.intelligent_monkey_test.roku import IntelligentMonkeyTestRoku
from scripts.connection.redis_conn import get_all


logger = logging.getLogger('main')


@log_decorator(logger)
def test_intelligent_monkey():
    try:
        # redis 상에서 갱신된 환경 설정 정보를 가져옴. (sub으로 올 수도 있고, redis에서 직접 가져올 수도 있음.)
        # 현재는 dummy로 처리
        arguments = get_arguments()
        logger.info(f"arguments: {arguments}")

        profile = arguments['profile']
        if profile == 'roku':
            imt = IntelligentMonkeyTestRoku(
                key_interval=arguments['interval'],
                duration_per_menu=arguments['duration_per_menu'],
                enable_smart_sense=arguments['enable_smart_sense'],
                waiting_time=arguments['waiting_time']
            )
            imt.run()
        elif profile == 'sk':
            pass
        else:
            raise NotImplementedError(f"invalid profile: {profile}")

        # publish_msg({'measurement': Command.COLOR_REFERENCE.value}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        # publish_msg({'measurement': Command.COLOR_REFERENCE.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in test_color_reference: {err}")
        logger.warning(error_detail)


def get_arguments() -> Dict:
    # return get_all('monkey_test_arguments')
    # DUMMY
    return {
        'profile': 'roku',
        'interval': 1.3,
        'duration_per_menu': 3,
        'enable_smart_sense': True,
        'waiting_time': 5
    }
