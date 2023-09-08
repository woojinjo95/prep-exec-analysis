import logging
import os

import cv2
import numpy as np
from patchify import patchify
import gdown
import onnxruntime as rt
from scripts.config import get_setting_with_env


logger = logging.getLogger('main')


class OnnxModel:
    def __init__(self, model_id):
        self.output_dir = get_setting_with_env('MODEL_SAVE_DIR')

        # load model
        model_path = self.download_model(model_id)
        self.sess = self.load_model(model_path)
        self.input_shape = tuple(self.sess.get_inputs()[0].shape[1:])
        logger.info(f'input shape: {self.input_shape}')

    def download_model(self, model_id):
        model_path = os.path.join(self.output_dir, f'{model_id}.onnx')

        if not os.path.exists(model_path):
            os.makedirs(self.output_dir, exist_ok=True)
            try:
                url = f"https://drive.google.com/uc?id={model_id}"
                gdown.download(url, model_path)
                logger.info('Model Download Complete.')
            except Exception:
                logger.error('Model Download Failed.')
                raise Exception('Model Download Failed.')
        else:
            logger.info('Model Already Exists.')
        return model_path

    def load_model(self, model_path):
        try:
            device = rt.get_device()
        except AttributeError:
            logger.error('Please reboot program. if it is your first installation of onnxruntime.')
            raise Exception('Please reboot program. if it is your first installation of onnxruntime.')

        if device == 'GPU':
            try:
                sess = rt.InferenceSession(model_path, providers=["CUDAExecutionProvider"])
                logger.info('GPU provider is successfully connected.')
            except Exception:
                logger.error('Error in GPU provider connection.')
                raise Exception('Error in GPU provider connection.')
        else:
            # sess = rt.InferenceSession(model_path)
            logger.error('Cannot detect GPU device to connect ONNX GPU provider.')
            raise Exception('Cannot detect GPU device to connect ONNX GPU provider.')
        return sess

    def predict_with_batch(self, batch):
        input_name = self.sess.get_inputs()[0].name
        pred = self.sess.run(None, {input_name: batch})[0]
        return pred


class MacroblockModel(OnnxModel):

    def __init__(self, model_id):
        super().__init__(model_id=model_id)

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
