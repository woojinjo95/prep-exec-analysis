from typing import List
import logging
import time
import traceback
from multiprocessing.managers import BaseManager

import numpy as np

from scripts.models.tf_model import MacroblockModel
from scripts.image_util import decode_image_from_base64


logger = logging.getLogger('main_logger')


class GPUWorker:
    def __init__(self, model_dir_url: str, model_output_dir: str, batch_size: int,
                queue_server_url: str, queue_server_port: int, patch_wait_timeout: float):
        # set model
        self.macroblock_model = MacroblockModel(model_dir_url=model_dir_url, model_output_dir=model_output_dir)

        self.queue_server_url = queue_server_url
        self.queue_server_port = queue_server_port

        # set patch data
        self.patch_datas = []
        self.batch_size = batch_size
        self.patch_wait_timeout = patch_wait_timeout
    
    def set_queue_connection(self):
        class QueueManager(BaseManager): pass

        QueueManager.register('get_patch_queue')
        QueueManager.register('get_result_queue')

        self.manager = QueueManager(address=(self.queue_server_url, self.queue_server_port), authkey=b'admin')
        self.manager.connect()

        self.patch_queue = self.manager.get_patch_queue()
        self.result_queue = self.manager.get_result_queue()

    def start_consumer(self):
        index = 0
        prev_consume_time = time.time()
        last_handle_time = time.time()

        self.set_queue_connection()

        while True:
            patch_data = self.patch_queue.get()

            if index % 1000 == 0:  # check queue status
                logger.info(f'patch consume interval each 1000 iteration. {time.time() - prev_consume_time} sec')
                prev_consume_time = time.time()
                qsize = self.patch_queue.qsize()
                if qsize > 2000:
                    logger.warning(f'patch queue size: {qsize}')

            self.patch_datas.append(patch_data)  # O(1)

            if len(self.patch_datas) >= self.batch_size or time.time() > last_handle_time + self.patch_wait_timeout:
                if len(self.patch_datas) > 0:
                    self.handle_batch(self.patch_datas)
                    self.patch_datas.clear()
                    last_handle_time = time.time()

            index += 1

    def run(self):
        while True:
            try:
                self.start_consumer()
            except Exception as err:
                logger.warning(f'Restart patch consumer with new connection. Cause => {err}')
                time.sleep(3)

    def handle_batch(self, patch_datas: List[dict]):
        start_time = time.time()

        try:
            logger.info(f'start to handle batch')

            batch = []
            patch_indices = []
            report_ids = []

            for patch_data in patch_datas:      
                # get image file
                image = decode_image_from_base64(patch_data['patch_byte'])
                batch.append(image)
                # get meta infos
                patch_indices.append(patch_data['patch_index'])
                report_ids.append(patch_data['report_id'])

            logger.info(f'decode patches. delay: {time.time() - start_time}')

            result = self.predict_with_patch_images(batch)
            result['patch_indices'] = patch_indices
            result['report_ids'] = report_ids
            result['status'] = 'success'

        except Exception as err:
            logger.error(f'error in predict => {traceback.format_exc()}')
            # dummy result data
            result = {
                'status': 'error',
                'model_input_shape': [224, 224, 3],
                'pred_delay': 0.0,
                'total_delay': 0.0,
                'patch_indices': patch_indices,
                'report_ids': report_ids,
                'scores': [0.0] * len(patch_indices),
            }

        finally:
            # TODO: send result to assembler
            logger.info(f'end to handle batch. delay: {round(time.time() - start_time, 4)} sec')
            self.send_to_assembler(result)

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

    def send_to_assembler(self, msg: dict):
        self.result_queue.put(msg)
