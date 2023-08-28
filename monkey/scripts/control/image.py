from typing import List

import cv2
import numpy as np

from scripts.config.config import get_setting_with_env


def get_snapshots(frame_num: int = 1) -> List[np.ndarray]:
    capture_device = get_setting_with_env('CAPTURE_DEVICE', '/dev/video0')
    cap = cv2.VideoCapture(capture_device)
    frames = []
    for i in range(frame_num):
        ret, frame = cap.read()
        if not ret:
            raise Exception('Could not read frame from camera')
        frames.append(frame)
    cap.release()
    return frames


def get_snapshot() -> np.ndarray:
    return get_snapshots()[0]

