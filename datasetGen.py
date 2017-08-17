# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 22:45:27 2017

@author: Sarika Nanda
"""
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
dev.close()

eng_char = 27#total characters in english dict
hind_char = 78#total characters in hindi dict

#preparation of dataset manually one hot encoding
file = codecs.open('scraped_data_google.txt', encoding = 'utf-8')
X = []
Y = []
for line in file:
    line = line.replace('\r', '')
    line = line.replace('\ufeff', '')
    line = line.replace('\n', '')
    line = line.split(' ')
    x = []
    y = []
    temp = line[0]#english word
    temp1 = line[1]#hindi word
    flag = 0
    for ch in temp1:#check if characters in hindi dictionary
        if ch not in hind_to_int:
            flag = 1
            break
    if flag == 1:#if not in dict, skip
        continue
    for char in temp:
        z = np.zeros(eng_char)
        z[eng_to_int[char]] = 1
        x.append(z)
    noPhi = 40 - len(x)
    for v in range(noPhi):
        z = np.zeros(eng_char)
        z[eng_to_int['$']] = 1
        x.append(z)
    for char in temp1:
        z = np.zeros(hind_char)
        z[hind_to_int[char]] = 1
        y.append(z)
    noPhi = 40 - len(y) - len(temp)
    for v in range(len(temp)):
        z = np.zeros(hind_char)
        z[hind_to_int['$']] = 1
        y.insert(0, z)
    for v in range(noPhi):
        z = np.zeros(hind_char)
        z[hind_to_int['$']] = 1
        y.append(z)
    X.append(x)
    Y.append(y)
X = np.array(X)
Y = np.array(Y)
file.close()

#save arrays
import h5py
h5f = h5py.File('TLdataset_2.h5', 'w')
h5f.create_dataset('eng_set', data = X)
h5f.create_dataset('hind_set', data = Y)
h5f.close()