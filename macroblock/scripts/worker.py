from typing import List
import logging
import time
import traceback

import numpy as np

from scripts.models.tf_model import MacroblockModel
from scripts.config.config import get_setting_with_env


logger = logging.getLogger('main')


class Worker:
    def __init__(self):
        model_dir_url = get_setting_with_env('TF_MODEL_URL')
        model_output_dir = get_setting_with_env('MODEL_SAVE_DIR', '/app/data/models')
        self.macroblock_model = MacroblockModel(model_dir_url=model_dir_url, model_output_dir=model_output_dir)

    def predict_with_patch_images(self, images: List[np.ndarray]) -> dict:
        try:
            start_time = time.time()

            image_count = len(images)
            logger.debug(f'image count: {image_count}')
            batch = np.array(images)
            logger.info(f'batch shape: {batch.shape}')

            # model predict with batch input datas
            start_pred_time = time.time()
            logger.debug('Start Prediction.')
            pred_result = self.macroblock_model.predict_with_preprocess(batch)
            logger.debug('End Prediction.')
            pred_delay = time.time() - start_pred_time

            # check validation
            logger.info(f'result shape: {pred_result.shape}')
            if int(pred_result.shape[0]) != image_count:
                logger.error(
                    f'image count and result length are diffrent. image count: {image_count} / result length: {pred_result.shape[0]}')
                raise Exception('invalid image count')

            scores = pred_result.tolist()
            # extract only true
            scores = [float(pred[1]) for pred in pred_result]

            total_delay = time.time() - start_time
            logger.info(f'Total Delay: {round(total_delay, 4)} / Prediction Delay: {round(pred_delay, 4)}')

            # return result
            result = {
                'scores': scores,  # [[0.99, 0.01], [0.88, 0.12], ... ]
                'model_input_shape': self.macroblock_model.input_shape,  # (224, 224, 3)
                'total_delay': total_delay,  # 0.05 sec
                'pred_delay': pred_delay  # 0.02 sec
            }
            logger.debug(f'result: {result}')
            return result

        except Exception as err:
            logger.error(f'error in predict => {traceback.format_exc()}')
            raise Exception('error in predict')
