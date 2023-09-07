import os
from typing import List

import cv2
import numpy as np
from scripts.config.constant import (BASE_TESTRUN_RAW_DIR, BASE_DEV_TEST_RAW_DIR, 
                                     BANNED_IMAGE_DIR, SKIPPED_IMAGE_DIR)
from scripts.external.scenario import get_scenario_info



def save_section_cursor_image(name: str, image: np.ndarray) -> str:
    scenario_info = get_scenario_info()
    save_dir = BASE_TESTRUN_RAW_DIR.format(scenario_info['testrun_id'])
    os.makedirs(save_dir, exist_ok=True)
    image_path = os.path.join(save_dir, f'{name}.png')
    cv2.imwrite(image_path, image)
    return image_path


def save_test_image(name: str, image: np.ndarray) -> str:
    scenario_info = get_scenario_info()
    save_dir = BASE_DEV_TEST_RAW_DIR.format(scenario_info['testrun_id'])
    os.makedirs(save_dir, exist_ok=True)
    image_path = os.path.join(save_dir, f'{name}.png')
    cv2.imwrite(image_path, image)
    return image_path


def get_banned_images() -> List[np.ndarray]:
    banned_images = []
    for banned_image_name in os.listdir(BANNED_IMAGE_DIR):
        banned_image_path = os.path.join(BANNED_IMAGE_DIR, banned_image_name)
        banned_image = cv2.imread(banned_image_path)
        banned_images.append(banned_image)
    return banned_images


def get_skipped_images() -> List[np.ndarray]:
    skipped_images = []
    for skipped_image_name in os.listdir(SKIPPED_IMAGE_DIR):
        skipped_image_path = os.path.join(SKIPPED_IMAGE_DIR, skipped_image_name)
        skipped_image = cv2.imread(skipped_image_path)
        skipped_images.append(skipped_image)
    return skipped_images
