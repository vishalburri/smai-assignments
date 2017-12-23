'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

from __future__ import print_function
import keras
import sys
import numpy as np
#from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
f = open('q2_b_output.txt','w')
file1 = sys.argv[1]
file2 = sys.argv[2]
batch_size = 32
num_classes = 10
epochs = 15

# input image dimensions
img_rows, img_cols = 32, 32

# the data, shuffled and split between train and test sets
def unpickle(file):
    import cPickle
    with open(file, 'rb') as fo:
        dict = cPickle.load(fo)
    return dict
a = unpickle(file1+"/data_batch_1")
x_train = a["data"]
y_train = a["labels"]

a = unpickle(file1+"/data_batch_2")
x_train = np.append(x_train,a["data"],axis=0)
y_train = np.append(y_train,a["labels"],axis=0)

a = unpickle(file1+"/data_batch_3")
x_train = np.append(x_train,a["data"],axis=0)
y_train = np.append(y_train,a["labels"],axis=0)

a = unpickle(file1+"/data_batch_4")
x_train = np.append(x_train,a["data"],axis=0)
y_train = np.append(y_train,a["labels"],axis=0)

a = unpickle(file1+"/data_batch_5")
x_train = np.append(x_train,a["data"],axis=0)
y_train = np.append(y_train,a["labels"],axis=0)

b = unpickle(file2)
x_test = b["data"]
y_test = b["labels"]

b = unpickle(file1+"/batches.meta")
label_names = b["label_names"]

#[](x_train, y_train), (x_test, y_test) = mnist.load_data()
if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 3, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 3, img_rows, img_cols)
    input_shape = (3, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 3)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 3)
    input_shape = (img_rows, img_cols, 3)

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
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dropout(0.25))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
final = model.predict(x_test)
for i in range(len(final)):
    f.write(label_names[np.argmax(final[i])]+'\n')
#score = model.evaluate(x_test, y_test, verbose=0)
#print('Test loss:', score[0])
#print('Test accuracy:', score[1])
