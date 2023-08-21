from typing import List, Generator
import traceback
import logging
import cv2

from scripts.analysis.image import get_cropped_image, calc_diff_rate, calc_color_entropy

logger = logging.getLogger('boot_test')


def task_boot_test_with_diff(video_path: str, timestamps: List[float], event_time: float) -> float:
    try:
        diff_timestamp = measure_boot_with_diff(
            video_path=video_path,
            mode='start',
            timestamps=timestamps,
            event_time=event_time)
    except:
        logger.error(f'Error: {traceback.format_exc()}')
        diff_timestamp = 0

    diff_time = max(int((diff_timestamp - event_time) * 1000), 0)
    return {
        'diff_timestamp': diff_timestamp,
        'diff_time': diff_time
    }


def measure_boot_with_diff(video_path: str, mode: str, timestamps: list, event_time: float, roi: list = None, param: dict = {}) -> float:
    """
    ROI 내부에서의 변화 시작 감지
    Args:
        video_path (str): 분석 비디오 경로
        timestamps (list): 비디오의 각 프레임 별 타임 스탬프
        event_timestamp (float): 측정 기준 시간
        roi (dict): x, y, w, h 로 구성된 roi 영역
        param(dict): 추가 파라미터
    Returns:
        int: 변화 시작 시간
    """
    prev_frame = None

    trigger_threshold = param.get('trigger_count', 20)
    min_color_depth_diff = param.get('min_color_depth_diff', 8)
    min_rate = param.get('min_rate', 0.0002)
    start_timestamp = param.get('start_timestamp', timestamps[0])
    entropy_thld = param.get('entropy_thld', 4.5)
    patience_thld = param.get('patience_thld', 3)

    # Extract Information
    is_diffs = []
    is_high_entropies = []
    idx = 0

    for frame, timestamp in zip(FrameGenerator(video_path), timestamps):
        if timestamp < max(event_time, start_timestamp):
            is_diffs.append(False)
            is_high_entropies.append(False)
            idx += 1
            continue

        if roi is not None:
            frame = get_cropped_image(frame, roi)

        if prev_frame is not None:
            diff_rate = calc_diff_rate(prev_frame, frame, min_color_depth_diff=min_color_depth_diff)
            is_diff = diff_rate > min_rate
            if is_diff:
                prev_entropy = calc_color_entropy(prev_frame)
                high_prev_entropy = prev_entropy > entropy_thld
                if high_prev_entropy:
                    is_diffs.append(True)
                    is_high_entropies.append(True)
                else:
                    is_diffs.append(True)
                    is_high_entropies.append(False)
            else:
                high_prev_entropy = None
                is_diffs.append(False)
                is_high_entropies.append(False)
        else:
            is_diff = None
            high_prev_entropy = None
            is_diffs.append(False)
            is_high_entropies.append(False)

        idx += 1
        prev_frame = frame

    # Find Trigger Point
    trigger_cnt = 0
    patience = 0
    start_index = None
    end_index = None

    for idx, (is_diff, is_high_entropy, frame) in enumerate(zip(is_diffs, is_high_entropies, FrameGenerator(video_path))):
        # logger.info(f'idx: {idx} / is diff: {is_diff} / high prev entropy: {is_high_entropy}')
        # cv2.imwrite(f'{image_dir}/{idx}.jpg', frame)

        is_triggered = is_diff and is_high_entropy
        if is_triggered:
            trigger_cnt += 1
            if trigger_cnt == 1:
                start_index = idx
            patience = 0
        else:
            # handle juddering pattern (diff - not diff - diff - not diff, ...)
            patience += 1
            if patience >= patience_thld:
                trigger_cnt = 0
            else:
                pass

        if trigger_cnt >= trigger_threshold:
            logger.info(f'triggered. idx: {idx} / start index: {start_index} / diff threshold: {trigger_threshold}')
            end_index = idx
            break
    else:
        return 0

    # Calculate Diff Time
    if mode == 'start':
        if start_index is None:
            logger.error('start index is None')
            return 0
        else:
            diff_time = timestamps[start_index]
            logger.info(f'diff start time: {diff_time}')
            return diff_time
    elif mode == 'end':
        diff_time = timestamps[end_index]
        logger.info(f'diff end time: {diff_time}')
        return diff_time
    else:
        logger.error(f'invalid mode => {mode}')
        return 0
    

def FrameGenerator(video_path: str, start_index=0) -> Generator:
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for idx in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        if idx < start_index:
            continue
        yield frame

    cap.release()
