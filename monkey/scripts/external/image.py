import os

import cv2
import numpy as np
from scripts.config.constant import BASE_TESTRUN_RAW_DIR
from scripts.external.scenario import get_scenario_info



def save_image(name: str, image: np.ndarray) -> str:
    scenario_info = get_scenario_info()
    save_dir = BASE_TESTRUN_RAW_DIR.format(scenario_info['testrun_id'])
    os.makedirs(save_dir, exist_ok=True)
    image_path = os.path.join(save_dir, f'{name}.png')
    cv2.imwrite(image_path, image)
    return image_path
