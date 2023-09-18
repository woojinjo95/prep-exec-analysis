import tensorflow as tf

# Define the path to the folder containing the .pb file
model_folder_path = r"G:\공유 드라이브\Macro-Block\models\lightweight\2022-05-25_18-51-028\orig"

# Load the model
loaded_model = tf.keras.models.load_model(model_folder_path)

# Inspect input layer names
for layer in loaded_model.layers:
    print(layer.name)
