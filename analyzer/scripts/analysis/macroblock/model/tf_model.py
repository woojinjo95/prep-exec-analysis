import logging
import os
import re
import time

import cv2
import numpy as np
import gdown
import tensorflow as tf


logger = logging.getLogger('main')


class TensorflowModel:
    def __init__(self, model_dir_url: str, model_output_dir: str):
        """_summary_
        Args:
            model_dir_url (str): model directory path
            model_output_dir (str): model save directory
        """
        self.output_dir = model_output_dir

        # load model
        logger.info(f'model url: {model_dir_url}')
        model_dir = self.download_model(model_dir_url)
        self.model = self.load_model(model_dir)

        self.input_shape = self.model.input_shape[1:]
        logger.info(f'input shape: {self.input_shape}')

    
    def download_model(self, model_dir_url):
        model_name = re.search('folders/(.*)\?usp', model_dir_url).group(1)
        model_dir = os.path.join(self.output_dir, model_name)

        if not os.path.exists(model_dir):
            os.makedirs(self.output_dir, exist_ok=True)
            os.makedirs(model_dir, exist_ok=True)
            try:
                gdown.download_folder(url=model_dir_url, output=model_dir)
                time.sleep(10)
                logger.info('Model Download Complete.')
            except Exception:
                logger.error('Model Download Failed.')
                raise Exception('Model Download Failed.')
        else:
            logger.info('Model Already Exists.')
        return model_dir

    def load_model(self, model_dir: str):
        model = tf.keras.models.load_model(model_dir)
        return model

    def predict_with_batch(self, batch):
        result = self.model.predict_on_batch(batch)
        return result


class MacroblockModel(TensorflowModel):

    def __init__(self, model_dir_url: str, model_output_dir: str):
        super().__init__(model_dir_url=model_dir_url, model_output_dir=model_output_dir)

    # preprocess for macroblock
    def preprocess(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype(np.float32) / 255.0
        return image

    # override onnx predict
    def predict(self, batch):
        return super().predict_with_batch(batch)

    def predict_with_preprocess(self, batch):
        batch = np.array([self.preprocess(patch) for patch in batch])
        return self.predict(batch)
