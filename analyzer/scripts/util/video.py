import cv2
import logging

logger = logging.getLogger('main')

class VideoCaptureContext:
    def __init__(self, *args, **kwargs):
        self.cap = cv2.VideoCapture(*args, **kwargs)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()
        cv2.destroyAllWindows()


def FrameGenerator(video_path: str, timestamps: list = None):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for frame_index in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            logger.warning(f"cannot read frame at {frame_index}")
            break

        if timestamps:
            cur_time = timestamps[frame_index]
        else:
            cur_time = 0

        yield frame, cur_time

    cap.release()
