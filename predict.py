# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 15:47:42 2017

@author: Sarika Nanda
"""
from keras.models import model_from_json
json_file = open('lstmModel_2.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("lstmWeights_2.h5")


import codecs
import numpy as np

#generating english character dictionary
eng = []
for i in range(97,123):
    eng.append(chr(i))
eng.append(chr(36))
eng_to_int = dict((c,i) for i,c in enumerate(eng))
int_to_eng = dict((i,c) for i,c in enumerate(eng))

#generating hindi character dictionary
dev = codecs.open('devanagri.txt', encoding = 'utf-8')
hind = []
for line in dev:
    line = line.replace('\r', '')
    line = line.replace(' ', '')
    line = line.replace('\ufeff', '')
    line = line.replace('\n', '')
    line = line.split('\t')
    temp = list(line)
    for i in temp:
        hind.append(i)
hind.append(chr(36))
hind_to_int = dict((c,i) for i,c in enumerate(hind))
int_to_hind = dict((i,c) for i,c in enumerate(hind))

#open file of words to be transliterated
file = codecs.open('words.txt', encoding = 'utf-8')
X = []

#one hot vector
eng_char = 27
for line in file:
    line=line.replace('\r', '')
    line=line.replace('\ufeff', '')
    line=line.replace('\n', '')
    print(line)
    x=[]
    for char in line:
        z = np.zeros(eng_char)
        z[eng_to_int[char]] = 1
        x.append(z)
    noPhi = 40 - len(x)
    for v in range(noPhi):
        z = np.zeros(eng_char)
        z[eng_to_int['$']] = 1
        x.append(z)
    X.append(x)
X = np.array(X)
#get predictions
Y = model.predict(X)

for samples in Y:
    output = ""
    for letters in samples:
        letters = letters.tolist()
        idx = letters.index(max(letters))
        if (idx!=77):
            output = output+int_to_hind[idx]
    print(output)

file.close()
