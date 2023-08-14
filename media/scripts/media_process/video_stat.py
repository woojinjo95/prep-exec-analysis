import json
import logging
import os
from typing import Tuple, List, Dict

import cv2

from ..configs.config import RedisDBEnum, get_value
from ..configs.constant import RedisChannel
from ..utils.file_manage import JsonManager, substitute_path_extension
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from ..utils._exceptions import handle_errors

logger = logging.getLogger('main')


@handle_errors
def process_video_info(file_info: dict) -> dict:
    name = file_info['name']
    created_time = file_info['created']
    index = file_info['index']

    # Get video info
    cap = cv2.VideoCapture(name)
    last_modified = os.path.getmtime(name)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    calculated_fps = round(frame_count / (last_modified - created_time), 4)

    video_info = {'frame_count': frame_count,
                  'fps': fps,
                  'width': width,
                  'height': height,
                  'fourcc': fourcc,
                  'index': index,
                  'created_time': created_time,
                  'last_modified': last_modified,
                  'calculated_fps': calculated_fps}

    json_file_name = substitute_path_extension(name, 'mp4_stat')

    with open(json_file_name, 'w', encoding='utf-8') as metadata:
        metadata.write(json.dumps(video_info, ensure_ascii=False, indent=4))

    return video_info


@handle_errors
def summerize_merged_video_info(requested_start_time: float, output_json_path: str, json_name_list: List[str]):
    video_infos = []
    for json_file in json_name_list:
        with open(json_file, 'r') as f:
            video_infos.append(json.loads(f.read()))

    # use first info data
    if len(video_infos) == 0:
        logger.error('No valid video in merged json file!')
        return
    else:
        primary_data = video_infos[0]

    info = {'video_name': substitute_path_extension(output_json_path, 'mp4'),
            'height': primary_data['height'],
            'width': primary_data['width'],
            'fps': primary_data['fps'],
            'resize_rate': 1,
            'skip_rate': 1,
            'fourcc': primary_data['fourcc'],
            'merged_info': video_infos,
            'logs': [],
            'timestamps': [],
            }

    # video #1 ~ video #last-1
    # 첫번째 ~ 마지막에서 두번째 영상은 만들어진 시간 편차를 실제 프레임 수로 나누어서 각각의 간격을 계산
    # 웬만하면 가장 마지막 수정 시각으로 계산해도 ~3 ms 이하의 오차를 보이나, 시간이 뒤집히지 않도록 양쪽 데이터를 맞춤
    if len(video_infos) >= 2:
        for prev_info, current_info in zip(video_infos, video_infos[1:]):
            start_time = prev_info['created_time']
            calculated_interval = current_info['created_time'] - prev_info['created_time']
            inter_calculated_fps = prev_info['frame_count'] / calculated_interval

            error_logging(primary_data, info, start_time, calculated_interval, inter_calculated_fps)
            info['timestamps'] += [round(start_time + idx / inter_calculated_fps, 6) for idx in range(prev_info['frame_count'])]
    else:
        current_info = video_infos[0]

    # video #last
    # 마지막 영상은 다음 영상이 없으므로, 자신의 가장 마지막 수정 시각 이용
    last_video_info = current_info
    start_time = last_video_info['created_time']
    calculated_interval = last_video_info['last_modified'] - last_video_info['created_time']
    calculated_fps = last_video_info['frame_count'] / calculated_interval

    error_logging(primary_data, info, start_time, calculated_interval, calculated_fps)
    info['timestamps'] += [round(start_time + idx / calculated_fps, 6) for idx in range(prev_info['frame_count'])]

    # 비디오 평가
    first_video_time = info['timestamps'][0]
    if requested_start_time < first_video_time:
        diff = first_video_time - requested_start_time
        log = f'Video is not exist before {first_video_time}, first {diff:.3f} seconds missed.'
        logger.warning(log)
        info['logs'].append(('warning', log))

    with JsonManager(output_json_path) as jf:
        jf.change('data', info)

    if 'error' in [el[0] for el in info['logs']]:
        log_level = 'error'
    elif 'warning' in [el[0] for el in info['logs']]:
        log_level = 'warning'
    else:
        log_level = 'info'

    with get_strict_redis_connection() as redis_connection:
        publish(redis_connection, RedisChannel.command, {'msg': 'recording_response',
                                                         'level': log_level,
                                                         'data': {'log': str(info['logs'])}})


def error_logging(primary_data: Dict, info: Dict, start_time: float, calculated_interval: float, inter_calculated_fps: float):
    fps_ratio = inter_calculated_fps / primary_data['fps']
    if abs(fps_ratio - 1) > 0.01:
        if abs(fps_ratio - 1) > 0.1:
            log = f'Local FPS ratio diff is over 10%! ({fps_ratio:.3f}), {start_time:.6f} to {calculated_interval:.3f}: Normal analysis cannot be done.'
            logger.error(log)
            info['logs'].append(('error', log))
        else:
            log = f'Local FPS ratio diff is over 1%! ({fps_ratio:.3f}), {start_time:.6f} to {calculated_interval:.3f}: check device settings.'
            logger.warning(log)
            info['logs'].append(('warning', log))
