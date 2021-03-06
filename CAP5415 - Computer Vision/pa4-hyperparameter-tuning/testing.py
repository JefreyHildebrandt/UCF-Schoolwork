'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

from __future__ import print_function
from time import time

import keras
from keras.datasets import mnist, fashion_mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras import backend as K
from keras.callbacks import TensorBoard


def train_model_with_different_learning_rate(optimizer, type):
    batch_size = 128
    num_classes = 10
    epochs = 30

    # input image dimensions
    img_rows, img_cols = 28, 28

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    model = Sequential()
    model.add(Conv2D(filters=6,
                     kernel_size=5,
                     strides=1,
                     activation='relu',
                     input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=2, strides=2))
    model.add(Conv2D(filters=16,
                     kernel_size=5,
                     strides=1,
                     activation='relu',
                     input_shape=(14, 14, 6)))
    model.add(MaxPooling2D(pool_size=2, strides=2))
    model.add(Flatten())
    model.add(Dense(units=120, activation='relu'))
    model.add(Dense(units=84, activation='relu'))
    model.add(Dense(units=10, activation='softmax'))

    start_time = time()

    # sgd = keras.optimizers.SGD(lr=learning_rate)

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=optimizer,
                  # optimizer=keras.optimizers.Adadelta(lr=learning_rate),
                  metrics=['accuracy'])
    log_file = "logs/{}".format(time()) + '-fashion-no-lr-' + type
    tensorboard = TensorBoard(log_dir=log_file, histogram_freq=0, write_graph=True, write_images=True)

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_test, y_test),
              callbacks=[tensorboard])
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    print('Total time:', (time() - start_time), 'seconds')

sgd = keras.optimizers.SGD(lr=learning_rate)
train_model_with_different_learning_rate(sgd, 'sgd')
train_model_with_different_learning_rate(keras.optimizers.Adadelta(), 'ada')