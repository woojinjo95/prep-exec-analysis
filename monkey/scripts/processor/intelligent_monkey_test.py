import logging
import traceback

from scripts.util.decorator import log_decorator


logger = logging.getLogger('main')


@log_decorator(logger)
def test_intelligent_monkey():
    try:
        pass

        # publish_msg({'measurement': Command.COLOR_REFERENCE.value}, 'analysis_response')

    except Exception as err:
        error_detail = traceback.format_exc()
        # publish_msg({'measurement': Command.COLOR_REFERENCE.value, 'log': error_detail}, 'analysis_response', level='error')
        logger.error(f"error in test_color_reference: {err}")
        logger.warning(error_detail)
