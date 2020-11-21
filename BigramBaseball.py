# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:10:03 2019

@author: ANKIT
"""

import nltk 
import string 
import re 
import os
import math
import operator
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter 

files = []
words_list1 = []
sentences_list = []
directory = r'D:\M.tech sem1\NLP\Assignments\A2\20news-19997\rec.sport.baseball\\'
for entry in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, entry)):
        files.append(entry)
doc_count1 = len(files)
for file_name in files:
    full_path = os.path.join(r"D:\M.tech sem1\NLP\Assignments\A2\20news-19997\rec.sport.baseball", file_name)
    fp = open(full_path,"r")
    text = fp.read()
    fp.close()
    ll = text.split("\n\n")
    del ll[0]    
    text = "\n\n".join(ll)
    text = text.lower()
    text = text.translate(text.maketrans('','','\S+@\S+'))
    text = re.sub(r'\d+', '', text)
    text = re.sub('\s+',' ',text)
    sentences = sent_tokenize(text)
    sentences_list.append(sentences)
    text = text.translate(text.maketrans('','',string.punctuation))
    text = re.sub(' +',' ',text)
    word_tokens = word_tokenize(text)
    text = [word for word in word_tokens]
    words_list1.extend(text)

words_number1 = len(words_list1)
word_count1 = Counter(words_list1)
word_freq_len = len(word_count1)
sentences_list_length = len(sentences_list)
for i in range(sentences_list_length):
    y = len(sentences_list[i])
    for j in range(y):
        sent = sentences_list[i][j]
        sent = sent.translate(sent.maketrans('','',string.punctuation))
        sentences_list[i][j] = sent
        
bigrams =[]
sent_starting_words = []
for i in range(0,sentences_list_length):
    y = len(sentences_list[i])
    for j in range(y):
        sent = sentences_list[i][j]
        word_tokens = word_tokenize(sent)
        sent = [word for word in word_tokens]
        k = len(sent)
        if k > 0:
            sent_starting_words.append(sent[0])            
        for m in range(k-1):
            pair = (sent[m],sent[m+1])
            bigrams.append(pair)
        
len_sent_starting_words = len(sent_starting_words)
first_words_count = Counter(sent_starting_words)
sorted_first_words_count = sorted(first_words_count.items(), key=operator.itemgetter(1))

bigrams_count = Counter(bigrams)   
sorted_bigrams_count = sorted(bigrams_count.items(), key=operator.itemgetter(1))

len_sorted_first_words_count  = len(sorted_first_words_count)
abc = sorted_first_words_count[len_sorted_first_words_count-1][0]
print(abc, end = " ")
len_sorted_bigrams_count = len(sorted_bigrams_count)
sent_prob = math.log10((sorted_first_words_count[len_sorted_first_words_count-1][1]) / (len_sent_starting_words))
for i in range(7):
    for j in range(len_sorted_bigrams_count-1,-1,-1):
        x = sorted_bigrams_count[j][0]        
        if x[0] == abc:
            print(x[1], end = " ")
            sent_prob = sent_prob + math.log10((sorted_bigrams_count[j][1])/ (word_count1[x[0]]))
            abc = x[1]
            break
print()
print(f"log probablity of the sentence = {sent_prob}")