# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 16:04:21 2017

@author: Sarika Nanda
"""

import codecs
#generating english character dictionary
eng = []
for i in range(97,123):
    eng.append(chr(i))
eng.append(chr(36))
eng_to_int = dict((c,i) for i,c in enumerate(eng))
int_to_eng = dict((i,c) for i,c in enumerate(eng))

def cleanup(line):
    line = line.replace('\r', '')
    line = line.replace('\ufeff', '')
    line = line.replace('\n', '')
    line = line.replace('(', '')
    line = line.replace(')', '')
    line = line.replace('[', '')
    line = line.replace(']', '')
    line = line.replace('.', '')
    line = line.replace(',', '')
    line = line.replace("'", '')
    line = line.replace('#', '')
    line = line.replace('"', '')
    line = line.replace('…', '')
    line = line.replace('!', '')
    line = line.split(' ')
    return line

def replace_with_newlines(element):
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, str):
            text += elem.strip()
        elif elem.name == 'br':
            text += '\n'
        elif elem.name == 'i':#break to prevent uneccessary text
            break
    return text

def get_hindi_tr_google(name):
    from urllib.request import Request,urlopen
    from bs4 import BeautifulSoup as bs
    part1 = 'http://www.google.com/transliterate/indic?tlqt=1&langpair=en|hi&text='
    part2 = '&&tl_app=1'
    page = part1 + name + part2
    u=urlopen(Request(page,headers={"User-Agent":'Mozilla'}))
    soup=bs(u,'lxml')
    for para in soup.find_all('p'):
        line = str(replace_with_newlines(para))
        flag = 0
        str1 = ""
        for i,ch in enumerate(line):
            if i == 0:
                continue
            if ch == '[':
                flag = 1
            elif (flag == 1 and (ch == ',' or ch == ']')):
                break
            elif (flag == 1 and ch is not '"'):
                str1 = str1 + ch
        return str1

filenew = 'scraped_data_google.txt'
filename = 'ScrapedLyrics.txt'
file1 = codecs.open(filename, encoding = 'utf-8')
filenew = open(filenew, 'w', encoding = 'utf-8')
engWords = {'':1, ' ':1}
for line in file1:
    engC = cleanup(line)
    for engW in engC:
        engW = engW.lower()
        flag = 0
        for ch in engW:
            if ch not in eng_to_int:
                flag = 1
                break
        if (engW not in engWords and len(engW) >=2 and flag == 0):
            engWords[engW] = 1
            print(engW)
            hindiW = get_hindi_tr_google(engW)
            filenew.write(engW + " " + hindiW + "\n")
filenew.close()
file1.close()