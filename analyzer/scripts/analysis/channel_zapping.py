import logging
from datetime import datetime
from typing import List
import cv2

from algorithm.channel_zapping.key_point.finder import KeypointFinder

logger = logging.getLogger('main')


def calculate_channel_zapping(video_path: str, timestamps: List[float], event_time: float,
                              min_diff_rate: float = 0.00002) -> List[int]:
    # get IR index
    ir_index = min(enumerate(timestamps),
                   key=lambda args: abs(args[1] - event_time))[0]  # find nearest index

    # calculate channel zapping
    try:
        video_data = cv2.VideoCapture(video_path)
        finder = KeypointFinder(video_data, ir_index=ir_index, timestamps=timestamps, min_diff_rate=min_diff_rate)
        indices_dict = finder.find_key_points()
        video_data.release()
        logger.info(f'key points: {indices_dict}')
    except Exception as err:
        logger.error(f'Fail to get key point indices in channel zapping algorithm. => {err}')
        raise Exception  # propagate to upper

    a_index = indices_dict['a_index']
    b_index = indices_dict['b_index']
    c_index = indices_dict['c_index']
    logger.info(
        f"indices: {ir_index}, {a_index}, {b_index}, {c_index}")

    # convert index to interval
    ir_date = datetime.fromtimestamp(timestamps[ir_index])
    a_date = datetime.fromtimestamp(timestamps[a_index])
    b_date = datetime.fromtimestamp(timestamps[b_index])
    c_date = datetime.fromtimestamp(timestamps[c_index])

    a = int((a_date - ir_date).total_seconds() * 1000)
    b = int((b_date - a_date).total_seconds() * 1000)
    c = int((c_date - b_date).total_seconds() * 1000)

    logger.info(
        f'[channel-zapping result] A: {a} ms / B: {b} ms / C: {c} ms / D: {d} ms / total: {a + b + c} ms.')

    return a, b, c
