import json
import logging
import os
import time

import cv2

from ..configs.config import get_value
from ..configs.constant import RedisChannel, RedisDBEnum
from ..connection.mongo_db.create import insert_to_mongodb
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from ..utils._timezone import (get_utc_datetime,
                               timestamp_to_datetime_with_timezone_str)

logger = logging.getLogger('snapshot')
file_logger = logging.getLogger('file')

IMAGE_EXTENSION = 'webp'
WEBP_QUALITY = 25
FRAME_SNAPSHOTS_IMAGE_SIZE = (160, 90)
WEBP_PARAMS = [cv2.IMWRITE_WEBP_QUALITY, WEBP_QUALITY]


def save_video_frame_snapshot(testrun_id: str = None, video_path: str = None, relative_time: float = None):
    workspace_info = get_value('testrun', db=RedisDBEnum.hardware)
    if testrun_id is None:
        testrun_id = workspace_info['id']
        logger.info(f'No testrun id defined: just use current id, {testrun_id}')

    output_path = os.path.join(workspace_info['workspace_path'], testrun_id, 'raw', 'frames')

    os.makedirs(output_path, exist_ok=True)

    log = ''
    log_level = 'info'
    image_name = ''
    image_path = ''
    metadata = {}
    try:
        logger.info(f'Image capture from {video_path}, relative_time: {relative_time}')
        if video_path is None or relative_time is None:
            log_level = 'error'
            log = f'no video path or relative_time: {video_path} / {relative_time}'

        cap = cv2.VideoCapture(video_path)
        total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        stat_path = f'{video_path}_stat'
        try:
            with open(stat_path, 'r') as f:
                json_data = json.load(f)

            timestamps = json_data['data']['timestamps']

        except:
            logger.warning('stat file is not exist. just calculate video')
            fps = cap.get(cv2.CAP_PROP_FPS)
            timestamps = [i / fps for i in range(total_frame_num)]

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

        cap.set(cv2.CAP_PROP_POS_FRAMES, target_idx)

        metadata = {'idx': target_idx, 'total_idx': total_frame_num, 'timestamp': timestamp_to_datetime_with_timezone_str(timestamps[target_idx])}
        logger.info(f'index {target_idx} / {total_frame_num}, abs time: {timestamps[target_idx]} / {timestamp_to_datetime_with_timezone_str(timestamps[target_idx])}')

        time_info = timestamp_to_datetime_with_timezone_str().replace('+00:00', 'Z')  # UTC+0 에서만 Z로 변경
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
            publish(redis_connection, RedisChannel.command, {'msg': 'video_frame_snapshot_response',
                                                             'level': log_level,
                                                             'data':  {'path': image_path, 'log': log, 'metadata': metadata}})


def save_full_frame_video_snapshots(scenario_id: str, testrun_id: str, video_path: str = None):

    output_path = os.path.join(os.path.dirname(video_path), 'frames')
    os.makedirs(output_path, exist_ok=True)

    logger.info(f'make snapshot image for {video_path}')

    log = ''
    log_level = 'info'

    try:
        cap = cv2.VideoCapture(video_path)
        total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        stat_path = f'{video_path}_stat'
        try:
            with open(stat_path, 'r') as f:
                json_data = json.load(f)

            timestamps = json_data['data']['timestamps']

        except:
            logger.warning('stat file is not exist. just calculate video')
            fps = cap.get(cv2.CAP_PROP_FPS)
            timestamps = [i / fps for i in range(total_frame_num)]

        if total_frame_num <= 180 * fps:  # 3 minutes
            snapshot_count = 60
        else:
            # if fps is 60, snapshot count in 180 s is 60.
            snapshot_count = total_frame_num // fps

        unit_step = total_frame_num / snapshot_count  # this value is floating
        logger.info(f'Video total frame count is {total_frame_num}, unit_step_index is {unit_step:.3f}, count: {snapshot_count}')

        snapshot_indices = [int(idx * unit_step) for idx in range(snapshot_count)]

        image_names = []
        for snapshot_index in snapshot_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, snapshot_index)
            ret, image = cap.read()
            if not ret:
                log += 'Failed to get images'
                break
            time_info = timestamp_to_datetime_with_timezone_str(timestamps[snapshot_index]).replace('+00:00', 'Z')  # UTC+0 에서만 Z로 변경
            image_name = f'{time_info}.{IMAGE_EXTENSION}'
            image_names.append(image_name)
            image_path = os.path.join(output_path, image_name)
            save_image = cv2.resize(image, FRAME_SNAPSHOTS_IMAGE_SIZE, interpolation=cv2.INTER_AREA)
            # save_image = image[::12, ::12]
            cv2.imwrite(image_path, save_image, WEBP_PARAMS)
        else:
            log += f'Succesfully {len(image_names)} images made'

        logger.info(log)

        document = {'timestamp': get_utc_datetime(time.time()),
                    'scenario_id': scenario_id,
                    'testrun_id': testrun_id,
                    'video_path': video_path,
                    'path': output_path,
                    'extension': IMAGE_EXTENSION,
                    'names': image_names,
                    }

        insert_to_mongodb('video_snapshot', document)

    except Exception as e:
        log += f'\n Error: {e}'
        log_level = 'error'
    finally:
        with get_strict_redis_connection() as redis_connection:
            publish(redis_connection, RedisChannel.command, {'msg': 'video_snapshots_response',
                                                             'level': log_level,
                                                             'data':  {'video_path': video_path,
                                                                       'path': output_path,
                                                                       'scenario_id': scenario_id,
                                                                       'testrun_id': testrun_id,
                                                                       'log': log,
                                                                       'count': snapshot_count,
                                                                       }})
