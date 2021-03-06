# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 13:41:11 2020

@author: MIT-DGMIF
"""

from keras import utils, models, layers, optimizers
from keras.models import Model, load_model, Sequential

from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D, Input, concatenate
from keras.preprocessing.image import ImageDataGenerator
from keras import initializers, regularizers, metrics
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import GlobalAveragePooling2D, ZeroPadding2D, Add
from keras.callbacks import ModelCheckpoint
from keras.applications import VGG16, VGG19, ResNet50

from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint

from keras import backend as K
from keras.applications.resnet50 import ResNet50

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()
import keras

import sklearn
from sklearn.model_selection import train_test_split
import numpy as np
import os, sys

import matplotlib.pyplot as plt
from keras.utils import multi_gpu_model


import numpy as np
import os
from PIL import Image
import os, glob
import matplotlib.pyplot as plt

base_path = 'E:\\Dataset\\rsna-intracranial-hemorrhage-detection\\brain_diagnosis\\4-Model'
dataset_path = os.path.join(base_path + '\\dataset')

X_train = np.load(dataset_path + '\\X_train.npy', allow_pickle=True)
y_train = np.load(dataset_path + '\\y_train.npy', allow_pickle=True)
X_test = np.load(dataset_path + '\\X_test.npy', allow_pickle=True)
y_test = np.load(dataset_path + '\\y_test.npy', allow_pickle=True)


'''
weight = 'E:\\Dataset\\rsna-intracranial-hemorrhage-detection\\brain_diagnosis\\4-Model\\dataset\\models\\model_weights_resnet.h5'
conv_base = ResNet50(weights = weight, include_top = False, input_shape = (128, 128, 3), pooling = 'max')
conv_base.trainable = True

model = Sequential()
model.add(conv_base)
#model.add(Flatten())
model.add(Dense(1024, activation = 'relu'))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(6, activation = 'sigmoid'))

model.compile(optimizer = optimizers.Adam(lr = 1e-4), loss = 'binary_crossentropy', metrics = ['binary_accuracy'])
model.summary()

'''
import efficientnet.keras as efn
from iterstrat.ml_stratifiers import MultilabelStratifiedShuffleSplit

base_model = efn.EfficientNetB2(weights = 'imagenet', include_top = False, pooling = 'avg', input_shape = (128, 128, 3))
x = base_model.output
x = Dropout(0.5)(x)
output = Dense(6, activation = 'sigmoid')(x)
model = Model(base_model.input, output)
#model = multi_gpu_model(resnet50, gpus = None)
model.summary()
model.compile(optimizer=optimizers.Adam(lr = 1e-4), loss = 'binary_crossentropy',  metrics=['binary_accuracy'])

hdf5_file = "E:\\Dataset\\rsna-intracranial-hemorrhage-detection\\brain_diagnosis\\5-Results\\weight_Classification_200514_Adam.hdf5"

'''
#datagenerator
batch_size = 16
epochs = 50
train_datagen = ImageDataGenerator()
val_datagen = ImageDataGenerator()

train_data_flow = train_datagen.flow(X_train, y_train, batch_size = batch_size)
val_data_flow = val_datagen.flow(X_test, y_test, batch_size = batch_size)
'''

early_stopping = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)
mc = ModelCheckpoint('best_model_classification_200514.h5', monitor='val_loss', mode='min', save_best_only=True)

if os.path.exists(hdf5_file):
    # 기존에 학습된 모델 불러들이기
    model.load_weights(hdf5_file)
else:
    # 학습한 모델이 없으면 파일로 저장
    #early_stopping = EarlyStopping(monitor = 'val_loss', patience = 10)

    #history = model.fit_generator(train_data_flow, epochs = epochs, steps_per_epoch = 25, verbose = 2, validation_data = val_data_flow, validation_steps = 16, workers = 4, callbacks=[ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=30, verbose=1, mode='auto', min_lr=1e-10)])
    #callbacks = [checkpoint])    
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, verbose = 2, validation_split = 0.2, callbacks=[early_stopping, mc])
    model.save_weights(hdf5_file)
    model.save('E:\\Dataset\\rsna-intracranial-hemorrhage-detection\\brain_diagnosis\\5-Results\\model_Classification_200514_Adam.h5')
    
    fig, ax = plt.subplots(2, 2, figsize=(10, 7))

    ax[0, 0].set_title('loss')
    ax[0, 0].plot(history.history['loss'], 'r')
    ax[0, 1].set_title('acc')
    ax[0, 1].plot(history.history['binary_accuracy'], 'b')

    ax[1, 0].set_title('val_loss')
    ax[1, 0].plot(history.history['val_loss'], 'r--')
    ax[1, 1].set_title('val_acc')
    ax[1, 1].plot(history.history['val_binary_accuracy'], 'b--')
    
loss_and_metrics = model.evaluate(X_test, y_test, batch_size=32)
print('## evaluation loss and_metrics ##')
print(loss_and_metrics)

# 7. 모델 사용하기
xhat = X_test[0:1]
yhat = model.predict(xhat)
print('## yhat ##')
print(yhat)  
    
    
    

    
    
    
    