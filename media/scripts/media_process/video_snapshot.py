import json
import logging
import os
from typing import Tuple

import cv2

from ..configs.config import get_value
from ..configs.constant import RedisChannel, RedisDBEnum
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from ..utils._timezone import timestamp_to_datetime_with_timezone_str

logger = logging.getLogger('snapshot')
file_logger = logging.getLogger('file')


def save_video_snapshot(video_path: str = None, relative_time: float = None):
    workspace_info = get_value('testrun', db=RedisDBEnum.hardware)
    output_path = os.path.join(workspace_info['workspace_path'], workspace_info['id'], 'raw', 'frames')
    # output_path = os.path.join('/home/nextlab/projects/prep-exec-analysis/data/workspace/testruns', workspace_info['id'], 'raw', 'frames')

    os.makedirs(output_path, exist_ok=True)

    log = ''
    log_level = 'info'
    image_path = ''
    try:
        logger.info(f'Image capture from {video_path}, relative_time: {relative_time}')
        if video_path is None or relative_time is None:
            log_level = 'error'
            log = f'no video path or relative_time: {video_path} / {relative_time}'

        stat_path = f'{video_path}_stat'
        with open(stat_path, 'r') as f:
            json_data = json.load(f)

        timestamps = json_data['data']['timestamps']
        target_time = timestamps[0] + relative_time

        if target_time > timestamps[-1]:
            log_level = 'warning'
            log = 'requested relative time is over video time! '

        for idx, timestamp in enumerate(timestamps):
            if timestamp > target_time:
                target_idx = idx

                if target_time - timestamps[target_idx - 1] < timestamps[target_idx] - target_time:
                    target_idx = idx - 1

                break

        else:
            target_idx = idx

        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_idx)
        total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        logger.info(f'index {target_idx} / {total_frame_num}, abs time: {timestamps[target_idx]} / {timestamp_to_datetime_with_timezone_str(timestamps[target_idx])}')

        time_info = timestamp_to_datetime_with_timezone_str(format="%Y-%m-%dT%H%M%SF%f%z")
        image_name = f'image_{time_info}.webp'

        ret, image = cap.read()
        if ret:
            image_path = os.path.join(output_path, image_name)
            cv2.imwrite(image_path, image)
            file_logger.info(f'image saved in {image_path}')
            log += 'Succesfully image made'
        else:
            image_path = ''
            log += 'Failed to get image'

    except Exception as e:
        log += f'\n Error: {e}'
        log_level = 'error'
    finally:
        with get_strict_redis_connection() as redis_connection:
            publish(redis_connection, RedisChannel.command, {'msg': 'video_snapshot_response',
                                                             'level': log_level,
                                                             'data':  {'path': image_path, 'log': log}})
