from __future__ import absolute_import, division, print_function, unicode_literals

from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

import os
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D
from tensorflow.keras.layers import Activation, Flatten, Dropout, Dense
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint

def network(input_shape, num_classes):
    model = Sequential()
    # extract image features by convolution and max pooling layers
    model.add(Conv2D(32, kernel_size = 3, padding = "same", input_shape = input_shape, activation = "relu"))
    model.add(Conv2D(32, kernel_size = 3, activation = 'relu'))
    model.add(MaxPool2D(pool_size= (2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, kernel_size = 3, padding = "same", activation = "relu"))
    model.add(Conv2D(64, kernel_size = 3, activation = 'relu'))
    model.add(MaxPool2D(pool_size= (2, 2)))
    model.add(Dropout(0.25))
    # classfy the calss by fully-connected layers
    model.add(Flatten())
    model.add(Dense(512, activation= "relu"))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation("softmax"))
    return model

class CIFAR10Dataset():
    def __init__(self):
        self.image_shape = (32, 32, 3)
        self.num_classes = 10
    
    def get_batch(self):
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        x_train, x_test = [self.preprocess(d) for d in [x_train, x_test]]
        y_train, y_test = [self.preprocess(d, label_data = True) for d in [y_train, y_test]]

        return x_train, y_train, x_test, y_test
    
    def preprocess(self, data, label_data = False):
        if label_data:
            #convert class vectors to binary class matrices
            data = to_categorical(data, self.num_classes)
        else:
            data = data.astype("float32")
            data /= 255 #convert the value to 0~1 scale
            shape = (data.shape[0],) + self.image_shape #add dataset length to top
            data = data.reshape(shape)

        return data

class Trainer():
    def __init__(self, model, loss, optimizer):
        self._target = model
        self._target.compile(loss = loss, optimizer = optimizer, metrics = ["accuracy"])
        self.verbose = 1
        self.log_dir = os.path.join(os.path.dirname(__file__), "logdir")
        self.model_file_name = "model_file.hdf5"
    
    def train(self, x_train, y_train, batch_size, epochs, validation_split):
        if os.path.exists(self.log_dir):
            import shutil
            shutil.rmtree(self.log_dir) #remove previous extension
        os.mkdir(self.log_dir)

        datagen = ImageDataGenerator(
            featurewise_center=False,  # set input mean to 0 over the dataset
            samplewise_center=False,  # set each sample mean to 0
            featurewise_std_normalization=False,  # divide inputs by std
            samplewise_std_normalization=False,  # divide each input by its std
            zca_whitening=False,  # apply ZCA whitening
            rotation_range=0,  # randomly rotate images in the range (0~180)
            width_shift_range=0.1,  # randomly shift images horizontally
            height_shift_range=0.1,  # randomly shift images vertically
            horizontal_flip=True,  # randomly flip images
            vertical_flip=False)  # randomly flip images
        
        datagen.fit(x_train) # compute quantities for normalization (mean, std etc)

        # split for validation data
        indices = np.arange(x_train.shape[0])
        np.random.shuffle(indices)
        validation_size = int(x_train.shape[0] * validation_split)
        x_train, x_valid = x_train[indices[:-validation_size], :], x_train[indices[-validation_size:], :]
        y_train, y_valid = y_train[indices[:-validation_size], :], y_train[indices[-validation_size:], :]

        model_path = os.path.join(self.log_dir, self.model_file_name)
        self._target.fit_generator(
            datagen.flow(x_train, y_train, batch_size=batch_size),
            steps_per_epoch=x_train.shape[0] // batch_size,
            epochs=epochs,
            validation_data=(x_valid, y_valid),
            callbacks=[
                TensorBoard(log_dir=self.log_dir),
                ModelCheckpoint(model_path, save_best_only=True)
            ],
            verbose=self.verbose,
            workers=4
        )

dataset = CIFAR10Dataset()

#make model
model = network(dataset.image_shape, dataset.num_classes)

#train the model
x_train, y_train, x_test, y_test = dataset.get_batch()
trainer = Trainer(model, loss = "categorical_crossentropy", optimizer = RMSprop())
trainer.train(x_train, y_train, batch_size = 128, epochs = 15, validation_split = 0.2)

#show_result
score = model.evaluate(x_test, y_test, verbose = 0)
print("Test loss:", score[0])
print("Test accuracy", score[1])