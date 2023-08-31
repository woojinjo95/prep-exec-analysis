import numpy as np
import cv2
from typing import Dict
import logging

from scripts.analysis.image import (calc_diff_rate, calc_image_value_rate, 
                                    calc_image_whole_stdev, is_similar_by_match_template)
from scripts.util.static import get_static_image

logger = logging.getLogger('main')

class FreezeDetector:
    def __init__(self, fps: float, sampling_rate: int, min_interval: float, min_color_depth_diff: int, 
                 min_diff_rate: float, frame_stdev_thres: float):
        self.fps = fps
        self.sampling_rate = sampling_rate
        self.min_interval = min_interval
        self.min_color_depth_diff = min_color_depth_diff
        self.min_diff_rate = min_diff_rate
        self.frame_stdev_thres = frame_stdev_thres

        self.freeze_info = {
            'fps': self.fps / self.sampling_rate,
            'prev_info': {
                'frame': None,
                'index': 0,
                'freeze_count': 0, 
                'start_time': 0,
                'freeze_type': 'none',
            },
        }

        power_off_image = get_static_image('power_off', 'off_screen_magewell.png')
        self.power_off_image = cv2.resize(power_off_image, (power_off_image.shape[1]//2, power_off_image.shape[0]//2))

    def update(self, frame: np.ndarray, timestamp: float) -> Dict:
        freeze_state = self.get_freeze_state(frame,
                                            timestamp,
                                            self.freeze_info['prev_info'],
                                            fps=self.freeze_info['fps'],
                                            sampling_rate=self.sampling_rate,
                                            min_interval=self.min_interval,
                                            frame_stdev_thres=self.frame_stdev_thres,
                                            min_color_depth_diff=self.min_color_depth_diff,
                                            min_diff_rate=self.min_diff_rate)
        if freeze_state['occured']:
            return {
                'detect': True,
                'start_time': freeze_state['start_time'],
                'duration': freeze_state['duration'],
                'freeze_type': freeze_state['freeze_type'],
            }
        else:
            return {
                'detect': False
            }

    def get_freeze_state(self, frame: np.ndarray, timestamp: float,
                        prev_info: dict, fps: float, sampling_rate: int,
                        min_interval: float, frame_stdev_thres: float,
                        min_color_depth_diff: int, min_diff_rate: float) -> dict:

        min_freeze_count = int(min_interval * fps)
        result = {'occured': False, 'skip': False}

        if prev_info['frame'] is None:
            # first frame skip
            prev_info['frame'] = frame
        elif prev_info['index'] % sampling_rate != 0:
            # sampling rate skip
            pass
        else:
            prev_info['index'] = 0

            diff_rate = calc_diff_rate(prev_info['frame'], frame, min_color_depth_diff=min_color_depth_diff)
            is_frame_freezed = diff_rate < min_diff_rate
            prev_info['frame'] = frame

            # manage freeze count and status
            status = 'none'
            if is_frame_freezed:
                if prev_info['freeze_count'] == 0:  # freeze count rising edge
                    status = 'rising'
                prev_info['freeze_count'] += 1
            else:
                if prev_info['freeze_count'] > 0:  # freeze count falling edge
                    status = 'falling'
                    if prev_info['freeze_count'] >= min_freeze_count:
                        status = 'occured'
                prev_info['freeze_count'] = 0

            if status == 'rising':
                prev_info['start_time'] = timestamp
                prev_info['freeze_type'] = self.get_freeze_type(frame, frame_stdev_thres)
            elif status == 'occured':
                result['occured'] = True
                result['start_time'] = prev_info['start_time']
                result['end_time'] = timestamp
                result['duration'] = timestamp - prev_info['start_time']
                result['freeze_type'] = prev_info['freeze_type']

            # logger.info(f'freeze_count: {prev_info["freeze_count"]}, diff_rate: {diff_rate}, is_frame_freezed: {is_frame_freezed}, min_freeze_count: {min_freeze_count}')

        prev_info['index'] += 1

        return result

    def get_freeze_type(self, frame: np.ndarray, frame_stdev_thres: float) -> str:
        resized_frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
        is_similar = is_similar_by_match_template(resized_frame, self.power_off_image)

        if is_similar:
            freeze_type = 'no_signal'
        else:
            frame_brightess = calc_image_value_rate(frame)
            frame_stdev = calc_image_whole_stdev(frame)

            if frame_stdev < frame_stdev_thres:
                if frame_brightess < 0.001:
                    freeze_type = 'black'
                elif frame_brightess > 0.999:
                    freeze_type = 'white'
                else:
                    freeze_type = 'one_colored'
            else:
                freeze_type = 'default'

        return freeze_type
