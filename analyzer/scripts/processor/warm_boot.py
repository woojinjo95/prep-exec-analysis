import logging
import traceback

from scripts.format import CollectionName
from scripts.external.data import load_input
from scripts.external.report import report_output
from scripts.connection.redis_pubsub import publish_msg
from scripts.util._timezone import get_utc_datetime
from scripts.util.video import VideoCaptureContext

logger = logging.getLogger('boot_test')


def test_warm_boot():
    try:
        logger.info(f"start test_warm_boot process")        
        args = load_input()

        with VideoCaptureContext(args.video_path) as vc:
            freeze_detector = set_freeze_detector(vc.fps)
            for frame_index in range(vc.frame_count):
                ret, frame = vc.cap.read()
                if not ret:
                    logger.warning(f"cannot read frame at {frame_index}")
                    break
                cur_time = args.timestamps[frame_index]
                result = freeze_detector.update(frame, cur_time)
                if result['detect']:
                    logger.info(f"freeze detected at {frame_index}")
                    report_output(CollectionName.FREEZE.value, {
                        'timestamp': get_utc_datetime(cur_time),
                        'freeze_type': result['freeze_type'],
                    })

        # publish_msg({'measurement': ['freeze']}, 'analysis_response')
        logger.info(f"end test_warm_boot process")

    except Exception as err:
        error_detail = traceback.format_exc()
        # publish_msg({'measurement': ['freeze']}, error_detail, level='error')
        logger.error(f"error in test_warm_boot: {err}")
        logger.warning(error_detail)
