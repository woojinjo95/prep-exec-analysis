from typing import List, Generator
import traceback
import logging
import numpy as np
import cv2

from scripts.analysis.image import get_cropped_image, is_similar_by_match_template
from scripts.util.decorator import log_decorator

logger = logging.getLogger('boot_test')


@log_decorator(logger)
def task_boot_test_with_match(video_path: str, timestamps: List[float], video_roi: List[int], template: np.ndarray, template_roi: List[int],
                              event_time: float, continuity_count: int):
    match_start_timestamp = 0
    try:
        # ir event time ~ home ui find time
        match_start_timestamp = calc_match_interval(
            video_path, timestamps, video_roi, template, template_roi, event_time, continuity_count, release=False)
    except:
        logger.error(f'Error: {traceback.format_exc()}')
    match_start_interval = max(int(match_start_timestamp - event_time * 1000), 0) if match_start_timestamp else 0

    result = {
        'match_timestamp': match_start_timestamp,
        'match_time': match_start_interval,
    }
    return result


def calc_match_interval(video_path: str, timestamps: list, video_roi: List[int], template: np.ndarray, template_roi: list, event_time: float,
                        continuity_count: int = 10, threshold: float = 0.8, binary_search=False, release=False) -> float:
    # set video capture object param
    video_data = cv2.VideoCapture(video_path)
    video_data.set(cv2.CAP_PROP_POS_FRAMES, 0)

    start_index = find_start_event_time_index(timestamps, event_time)

    # use binary search
    if binary_search:
        logger.info('binary search start')
        # start binary search
        start = start_index
        frame_count = int(video_data.get(cv2.CAP_PROP_FRAME_COUNT))
        end = frame_count - 1
        matched_flag = False

        while start <= end:
            mid = (start + end) // 2
            video_data.set(cv2.CAP_PROP_POS_FRAMES, mid)

            # validate matching using continuity
            for i in range(continuity_count):
                _, frame = video_data.read()
                frame_image = get_cropped_image(frame, video_roi)
                template_image = get_cropped_image(template, template_roi)
                if not is_similar_by_match_template(frame_image, template_image, threshold):
                    matched = False
                    break
            else:
                matched = True

            # Fix start and end index by matching
            if matched:
                end = mid - 1
                matched_flag = True
            else:
                start = mid + 1
        video_data.release()
        # return match index
        if matched_flag:
            return timestamps[mid]
        else:  # 마지막까지 못찾으면 None 반환
            return 0

    # whole frame search
    else:
        logger.info('Binary search option is False, Activate FrameGerator')
        match_cnt = 0

        for frame, timestamp in FrameTimestampGenerator(video_path, timestamps, start_index, release=release):
            frame_image = get_cropped_image(frame, video_roi)
            template_image = get_cropped_image(template, template_roi)

            matched = is_similar_by_match_template(frame_image, template_image, threshold)
            if matched:
                match_cnt += 1
            else:
                match_cnt = 0

            if match_cnt == 1:
                start_time = timestamp

            if match_cnt >= continuity_count:
                return start_time

        return 0


def find_start_event_time_index(timestamps: List[float], event_time: float) -> int:
    start_index = 0
    end_index = len(timestamps) - 1

    for index, timestamp in enumerate(timestamps):
        if event_time < timestamp:
            start_index = index
            break
    else:
        start_index = end_index

    return start_index


def FrameTimestampGenerator(video_path: str, timestamps: List[float], start_index=0, end_index=None, release=True) -> Generator:
    cap = cv2.VideoCapture(video_path)
    frame_count = len(timestamps)

    if end_index is None:
        end_index = frame_count - 1

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_index)
    timestamps = timestamps[start_index:end_index]

    for timestamp in timestamps:
        ret, frame = cap.read()
        if not ret:
            break
        yield frame, timestamp

    if release:
        cap.release()
