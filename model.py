# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 23:06:34 2017

@author: Sarika Nanda
"""
#change directory
import os
default_path = "C:\Users\Sarika Nanda\Desktop\Samsung"
os.chdir(default_path)

#load dataset
import h5py
h5f = h5py.File('TLdataset.h5', 'r')
X = h5f['eng_set'][:]
Y = h5f['hind_set'][:]
h5f.close()

#split test and train data
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

#many to many LSTM model
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, TimeDistributed
model = Sequential()
model.add(LSTM(256, input_shape = (X.shape[1], X.shape[2]), return_sequences = True))
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(Y.shape[2], activation = 'softmax')))
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

#define checkpoint
from keras.callbacks import ModelCheckpoint
filepath = 'weights-improvement-{epoch:02d}-{loss:.4f}.hdf5'
checkpoint = ModelCheckpoint(filepath, monitor = 'loss', verbose = 1, save_best_only=True, mode = 'min')
callbacks_list = [checkpoint]

#fit the model
model.fit(X_train, Y_train, batch_size=128, nb_epoch=100,
          validation_data=(X_test, Y_test), callbacks = callbacks_list)
#model.fit(X_train, Y_train, epochs = 20, batch_size=128, callbacks = callbacks_list)

#save model and weights
from keras.models import model_from_json
# serialize model to JSON
model_json = model.to_json()
with open("lstmModel.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("lstmWeights.h5")

#final accuracy
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, batch_size=128, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
 
# later...
 
# load json and create model
'''json_file = open('lstmModel.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("lstmWeights.h5")'''
