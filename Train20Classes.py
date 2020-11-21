# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 23:33:05 2019

@author: ANKIT
"""
import nltk 
import string 
import re 
import os
import pickle
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter 

lemmatizer = WordNetLemmatizer()
folders = []
total_words_in_classes = []
vocabulary = []
dict_of_dict = dict()
i = 0
directory = r'D:\M.tech sem1\NLP\Assignments\A2\20news-19997\\'

for entry in os.listdir(directory):
    if os.path.isdir(os.path.join(directory, entry)):
        folders.append(entry)

for folder_name in folders:
    folder_path = os.path.join(r"D:\M.tech sem1\NLP\Assignments\A2\20news-19997", folder_name)
    files = []
    i = i + 1
    for entry in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, entry)):
            files.append(entry)
            words_list = []
    for file_name in files:
        lemmas = []
        full_path = os.path.join(folder_path, file_name)
        fp = open(full_path,"r")
        text = fp.read()
        fp.close()
        ll = text.split("\n\n")
        del ll[0]    
        text = "\n\n".join(ll)
        text = text.lower()
        text = text.translate(text.maketrans('','','\S+@\S+'))
        text = re.sub(r'\d+', '', text)
        text = text.translate(text.maketrans('','',string.punctuation))
        text = re.sub(' +',' ',text)
        stop_words = set(stopwords.words("english")) 
        word_tokens = word_tokenize(text)
        text = [word for word in word_tokens if word not in stop_words]
        lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in text]
        words_list.extend(lemmas)

    total_words_in_classes.append(len(words_list))
    vocabulary.extend(words_list)
    word_count = Counter(words_list)
    size = len(word_count)
    print(f"for class = {size}")
    print("doing")
    dict_of_dict[i] = word_count

dict_vocab = Counter(vocabulary)
vocab_len = len(dict_vocab)
print("starting")
Picklefile1 = open('NestedDict', 'wb') 
pickle.dump(dict_of_dict, Picklefile1)                      
Picklefile1.close()

Picklefile2 = open('ClassesWordCounts', 'wb') 
pickle.dump(total_words_in_classes, Picklefile2)                      
Picklefile2.close()

Picklefile3 = open('VocCount', 'wb')
pickle.dump(vocab_len, Picklefile3)
Picklefile3.close()
