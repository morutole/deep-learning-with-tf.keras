from __future__ import absolute_import, division, print_function, unicode_literals

"""
import tensorflow as tf
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices: 
    tf.config.experimental.set_memory_growth(device, True)
"""

from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras import Model
import numpy as np

base_model = VGG19(weights="imagenet")
model = Model(inputs=base_model.input, outputs=base_model.get_layer("block4_pool").output)

img_path = "sample_images_pretrain\\elephant.jpg"
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

block4_pool_features = model.predict(x)

"""
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.vgg19 import preprocess_input, decode_predictions
import tensorflow.keras.preprocessing.image as Image
from tensorflow.keras import Model
import numpy as np

model = VGG19(weights = "imagenet", include_top=True)

image_path = "sample_images_pretrain\\elephant.jpg"
image = Image.load_img(image_path, target_size=(224, 224))  # imagenet size
x = Image.img_to_array(image)
x = np.expand_dims(x, axis=0)  # add batch size dim
x = preprocess_input(x)

result = model.predict(x)
result = decode_predictions(result, top=3)[0]
print(result[0][1])  # show description
"""