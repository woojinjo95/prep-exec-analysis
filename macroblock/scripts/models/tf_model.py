import logging
import os
import re
import time

import cv2
import numpy as np
from patchify import patchify
import gdown
import tensorflow as tf


logger = logging.getLogger('main_logger')


class TensorflowModel:
    def __init__(self, model_dir_url: str, model_output_dir: str, gpu_index: int = None, gpus: list = []):
        """_summary_
        Args:
            model_dir_url (str): model directory path
            model_output_dir (str): model save directory
            gpu_index (int, optional): gpu index for model. if this value is not None then gpus value is ignored
                -> one gpu - one model binding
            gpus (list, optional): gpu list for model (tensorflow physical device). if this value is not None then gpu_index value is ignored
                -> multigpu binding
        """
        self.output_dir = model_output_dir
        self.gpu_index = gpu_index
        self.gpus = gpus

        # load model
        logger.info(f'model url: {model_dir_url}')
        model_dir = self.download_model(model_dir_url)
        if self.gpus:
            logger.info(f'GPU IDs: {self.gpus}')
            self.model = self.load_model_with_gpus(model_dir, self.gpus)
        elif self.gpu_index is not None:
            logger.info(f'GPU INDEX: {self.gpu_index}')
            self.model = self.load_model_with_gpu_index(model_dir)
        else:
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
    
    def load_model_with_gpu_index(self, model_dir: str):
        model = tf.keras.models.load_model(model_dir)
        return model

    def load_model_with_gpus(self, model_dir: str, gpus: list) -> tf.keras.Model:
        strategy = tf.distribute.MirroredStrategy(gpus)
        with strategy.scope():
            model = tf.keras.models.load_model(model_dir)
        return model

    def predict_with_batch(self, batch):
        if self.gpu_index is not None:
            with tf.device(f'/GPU:{self.gpu_index}'):
                result = self.model.predict_on_batch(batch)
        else:
            result = self.model.predict_on_batch(batch)
        return result


class MacroblockModel(TensorflowModel):

    def __init__(self, model_dir_url: str, model_output_dir: str, gpu_index: int = None, gpus: list = []):
        super().__init__(model_dir_url=model_dir_url, model_output_dir=model_output_dir, gpu_index=gpu_index, gpus=gpus)

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

    def predict_with_video_frame(self, image, step=200):
        patches = patchify(image, self.input_shape, step)
        patch_row, patch_col, _, h, w, c = patches.shape
        batch = np.reshape(patches, (patch_row * patch_col, h, w, c))

        pred = self.predict_with_preprocess(batch)
        scores = np.array([float(score[1]) for score in pred])
        return scores
