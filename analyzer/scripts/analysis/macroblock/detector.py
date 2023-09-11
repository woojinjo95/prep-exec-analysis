from typing import List
import logging
import time
import traceback

import numpy as np

from scripts.analysis.macroblock.model.tf_model import MacroblockModel
from scripts.analysis.macroblock.discriminator.crack_discriminator import CrackDiscriminator
from scripts.config.config import get_setting_with_env
from scripts.analysis.image import split_image_with_shape
from scripts.format import ClassificationResult, ImageSplitResult, MacroblockResult


logger = logging.getLogger('main')


class MacroblockDetector:
    def __init__(self, score_thld: float, continuity_set_thld: int):
        self.input_shape = get_setting_with_env('MODEL_INPUT_SHAPE', (224, 224, 3))

        model_dir_url = get_setting_with_env('TF_MODEL_URL')
        model_output_dir = get_setting_with_env('MODEL_SAVE_DIR', '/app/workspace/macroblock_models')
        self.macroblock_model = MacroblockModel(model_dir_url=model_dir_url, model_output_dir=model_output_dir)

        self.discriminator = CrackDiscriminator(crack_score_thld=score_thld,
                                                continuity_set_thld=continuity_set_thld,
                                                continuity_hold_thld=get_setting_with_env('CONTINUITY_HOLD_THLD', 1),
                                                crack_patch_ratio=get_setting_with_env('CRACK_PATCH_RATIO', 0.2),
                                                row_crack_patch_ratio=get_setting_with_env('ROW_CRACK_PATCH_RATIO', 0.5))

        self.last_occurred = False
        self.start_occurred_time = None

    def update(self, image: np.ndarray, timestamp: float) -> MacroblockResult:
        try:
            # check macroblock is occurred in this frame
            split_result = self.preprocess_image(image)
            cls_result = self.predict_with_patch_images(split_result.patches)
            occurred = self.postprocess_result(cls_result, split_result)

            # check macroblock is finally detected
            end_occurred_time, duration = None, None
            if occurred and not self.last_occurred:  # rising edge
                self.start_occurred_time = timestamp
                logger.info(f'Macroblock occurred! start_time: {self.start_occurred_time}')
                detect = False
            elif not occurred and self.last_occurred:  # falling edge
                end_occurred_time = timestamp
                duration = end_occurred_time - self.start_occurred_time
                logger.info(f'Macroblock disappeared! end_time: {end_occurred_time}, duration: {duration}')
                detect = True
            else:
                detect = False

            result = MacroblockResult(status='success', 
                                      detect=detect,
                                      occurred=occurred,
                                      start_time=self.start_occurred_time,
                                      end_time=end_occurred_time,
                                      duration=duration,
                                      split_result=split_result,
                                      cls_result=cls_result)
            self.last_occurred = occurred
            return result

        except Exception as err:
            logger.error(f'error in update. {err}')
            logger.warning(traceback.format_exc())
            return MacroblockResult(status='error')

    def preprocess_image(self, image: np.ndarray) -> ImageSplitResult:
        split_result = split_image_with_shape(image, self.input_shape)
        logger.debug(f'image_shape: {image.shape}, row_num: {split_result.row_num}, col_num: {split_result.col_num}')
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
        logger.debug(f'batch shape: {batch.shape}')

        # model predict with batch input datas
        start_pred_time = time.time()
        logger.debug('Start Prediction.')
        pred_result = self.macroblock_model.predict_with_preprocess(batch)
        logger.debug('End Prediction.')
        pred_delay = time.time() - start_pred_time

        # check validation
        logger.debug(f'result shape: {pred_result.shape}')
        if int(pred_result.shape[0]) != image_count:
            logger.error(
                f'image count and result length are diffrent. image count: {image_count} / result length: {pred_result.shape[0]}')
            raise Exception('invalid image count')

        scores = pred_result.tolist()
        # extract only true
        scores = [float(pred[1]) for pred in pred_result]

        total_delay = time.time() - start_time
        logger.debug(f'Total Delay: {round(total_delay, 4)} / Prediction Delay: {round(pred_delay, 4)}')

        # return result
        result = ClassificationResult(
            scores=scores,
            model_input_shape=self.macroblock_model.input_shape,
            total_delay=total_delay,
            pred_delay=pred_delay
        )
        logger.debug(f'result: {result}')
        return result
