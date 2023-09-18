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
    def __init__(self, model_url: str, model_output_dir: str):
        self.output_dir = model_output_dir

        # load model
        logger.info(f'model url: {model_url}')
        model_path = self.download_model(model_url)
        self.model = self.load_model(model_path)

        self.input_shape = self.get_input_shape()

    def download_model(self, model_url: str) -> str:
        model_name = re.search('/uc\?id=(.*)', model_url).group(1)
        logger.info(f'model name: {model_name}')
        model_path = os.path.join(self.output_dir, model_name) + '.tflite'

        if not os.path.exists(model_path):
            os.makedirs(self.output_dir, exist_ok=True)
            try:
                gdown.download(url=model_url, output=model_path)
                time.sleep(10)
                logger.info('Model Download Complete.')
            except Exception:
                logger.error('Model Download Failed.')
                raise Exception('Model Download Failed.')
        else:
            logger.info('Model Already Exists.')
        return model_path

    def load_model(self, model_path: str) -> tf.lite.Interpreter:
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter

    def predict_with_batch(self, batch) -> np.ndarray:
        # Get input and output details
        input_details = self.model.get_input_details()
        output_details = self.model.get_output_details()

        # Check if the interpreter supports batching.
        if input_details[0]['shape'][0] == 1:
            results = []
            for sample in batch:
                sample = np.expand_dims(sample, axis=0).astype(input_details[0]['dtype'])
                self.model.set_tensor(input_details[0]['index'], sample)
                self.model.invoke()
                output_data = self.model.get_tensor(output_details[0]['index'])
                results.append(output_data)
            return np.vstack(results)
        else:
            # In this case, your tflite model is already configured to accept batches.
            batch = np.array(batch).astype(input_details[0]['dtype'])
            self.model.set_tensor(input_details[0]['index'], batch)
            self.model.invoke()
            output_data = self.model.get_tensor(output_details[0]['index'])
            return output_data

    def get_input_shape(self) -> tuple:
        input_details = self.model.get_input_details()
        input_shape = input_details[0]['shape'][1:]
        logger.info(f'input shape: {input_shape}')
        return input_shape

class MacroblockModel(TensorflowModel):

    def __init__(self, model_url: str, model_output_dir: str):
        super().__init__(model_url=model_url, model_output_dir=model_output_dir)

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
