import tensorflow as tf

# Load your saved model
saved_model_dir = r'G:\공유 드라이브\Macro-Block\models\lightweight\2022-05-25_18-51-028\orig'  # Replace with the path to your actual saved model directory

# Convert the model to the TensorFlow Lite format with quantization
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quant_model = converter.convert()

# Save the converted model to disk
open("efficientnetb0_quant.tflite", "wb").write(tflite_quant_model)
