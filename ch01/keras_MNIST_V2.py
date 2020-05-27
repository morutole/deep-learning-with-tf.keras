from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import TensorBoard

np.random.seed(1671) # for reproducibility
# network and training
NB_EPOCH = 20
BATCH_SIZE = 128
VERBOSE = 1
NB_CLASSES = 10 # number of outputs = number of digits
OPTIMIZER = SGD() #SGD optimizer, explained later in this chapter
N_HIDDEN = 128
VALIDATION_SPLIT = 0.2 #how much TRAIN is reversed for VALIDATION

# data: shuffled and split between train and test sets
#
(X_train, y_train), (X_test, y_test) = mnist.load_data()
#X_train is 60000 rows of 28x28 values --> reshaped in 60000x784
RESHAPED = 784
#
X_train = X_train.reshape(60000, RESHAPED)
X_test = X_test.reshape(10000, RESHAPED)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
# normalize
#
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')
#convert calss vectors to binary class matrices
Y_train = to_categorical(y_train, NB_CLASSES)
Y_test = to_categorical(y_test, NB_CLASSES)

model = Sequential()
model.add(Dense(N_HIDDEN, input_shape = (RESHAPED,)))
model.add(Activation('relu'))
model.add(Dense(N_HIDDEN))
model.add(Activation('relu'))
model.add(Dense(NB_CLASSES))
model.add(Activation('softmax'))
model.summary()

import os
from time import gmtime, strftime

def make_tensorboard(set_dir_name= ''):
    tictoc = strftime("%a_%d_%b_%Y_%H_%M_%S", gmtime())
    directory_name = tictoc
    log_dir = set_dir_name + '_' + directory_name
    os.mkdir(log_dir)
    tensorboard = TensorBoard(log_dir= log_dir)
    return tensorboard

callbacks = [make_tensorboard(set_dir_name= 'keras_MNIST_V2')]

model.compile(loss= 'categorical_crossentropy', optimizer= OPTIMIZER, metrics= ['accuracy'])
model.fit(X_train, Y_train, batch_size= BATCH_SIZE, epochs= NB_EPOCH, callbacks= callbacks, verbose= VERBOSE, validation_split= VALIDATION_SPLIT)
score = model.evaluate(X_test, Y_test, verbose = VERBOSE)
print("\nTest score:", score[0])
print("Test accuracy:", score[1])