'''
Created on Dec, 2016

@author: hugo

'''
from __future__ import absolute_import
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping, ReduceLROnPlateau


def neural_network(input_size, n_class):
    model = Sequential()
    model.add(Dense(n_class, input_dim=input_size, init='glorot_normal', activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

def neural_classifier(X_train, Y_train, X_val, Y_val, X_test, Y_test, nb_epoch=200, batch_size=10, seed=7):
    clf = neural_network(X_train.shape[1], Y_train.shape[1])
    clf.fit(X_train, Y_train,
                        nb_epoch=nb_epoch,
                        batch_size=batch_size,
                        shuffle=True,
                        validation_data=(X_val, Y_val),
                        callbacks=[
                                    ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.01),
                                    EarlyStopping(monitor='val_loss', min_delta=1e-5, patience=5, verbose=0, mode='auto'),
                        ]
                        )
    acc = clf.test_on_batch(X_test, Y_test)[1]

    return acc