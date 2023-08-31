import cv2
import logging

from scripts.util.static import get_static_image
from scripts.analysis.image import is_similar_by_match_template

logger = logging.getLogger('main')


def check_poweroff_video(video_path) -> bool:
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        logger.warning("cannot read frame")
        return False
    cap.release()
    
    power_off_image = get_static_image('power_off', 'off_screen_magewell.png')
    is_similar = is_similar_by_match_template(frame, power_off_image)
    if is_similar:
        logger.info(f'power off video: {video_path}')
        return True
    else:
        logger.info(f'not power off video: {video_path}')
        return False
