import cv2
import os
import numpy as np

static_image_root_path = os.path.join('/app', 'static')


def get_static_image(*args: str) -> np.ndarray:
    image_path = os.path.join(static_image_root_path, *args)
    image = cv2.imread(image_path)
    return image
