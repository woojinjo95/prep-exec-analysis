from typing import List
import logging
import time
import traceback

import numpy as np

from scripts.analysis.macroblock.model.tf_model import MacroblockModel
from scripts.analysis.macroblock.discriminator.crack_discriminator import CrackDiscriminator
from scripts.config.config import get_setting_with_env
from scripts.analysis.image import split_image_with_shape
from scripts.format import ClassificationResult, ImageSplitResult


logger = logging.getLogger('main')


class Worker:
    def __init__(self):
        self.input_shape = get_setting_with_env('MODEL_INPUT_SHAPE', (224, 224, 3))

        model_dir_url = get_setting_with_env('TF_MODEL_URL')
        model_output_dir = get_setting_with_env('MODEL_SAVE_DIR', '/app/workspace/macroblock_models')
        self.macroblock_model = MacroblockModel(model_dir_url=model_dir_url, model_output_dir=model_output_dir)

        self.discriminator = CrackDiscriminator(crack_score_thld=get_setting_with_env('CRACK_SCORE_THLD', 0.995),
                                                continuity_set_thld=get_setting_with_env('CONTINUITY_SET_THLD', 3), 
                                                continuity_hold_thld=get_setting_with_env('CONTINUITY_HOLD_THLD', 1),
                                                crack_patch_ratio=get_setting_with_env('CRACK_PATCH_RATIO', 0.2),
                                                row_crack_patch_ratio=get_setting_with_env('ROW_CRACK_PATCH_RATIO', 0.5))

    def process_image(self, image: np.ndarray) -> bool:
        try:
            split_result = self.preprocess_image(image)
            cls_result = self.predict_with_patch_images(split_result.patches)
            result = self.postprocess_result(cls_result, split_result)
            return result
        except Exception as err:
            logger.error(f'error in process_image. {err}')
            logger.warning(traceback.format_exc())

    def preprocess_image(self, image: np.ndarray) -> ImageSplitResult:
        split_result = split_image_with_shape(image, self.input_shape)
        logger.info(f'image_shape: {image.shape}, row_num: {split_result.row_num}, col_num: {split_result.col_num}')
        return split_result

    def postprocess_result(self, cls_results: ClassificationResult, split_result: ImageSplitResult) -> bool:
        self.discriminator.update(cls_results.scores, split_result.row_num, split_result.col_num)
        summary = self.discriminator.get_summary()
        return summary['error_state']

    def predict_with_patch_images(self, images: List[np.ndarray]) -> ClassificationResult:
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
        result = ClassificationResult(
            scores=scores,
            model_input_shape=self.macroblock_model.input_shape,
            total_delay=total_delay,
            pred_delay=pred_delay
        )
        logger.debug(f'result: {result}')
        return result
