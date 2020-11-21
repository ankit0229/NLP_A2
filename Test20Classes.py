# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 23:53:54 2019

@author: ANKIT
"""
import nltk 
import string 
import re 
import os
import pickle
import math
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter 

lemmatizer = WordNetLemmatizer()
folders = []
final = []
doc_counts = []
class_prob = []
prob_words_in_class = [0]*20
vocab = []
prob_doc_in_class = []
log_prob_doc_in_class = []
folders = []
doc_sum = 0

Picklefile1 = open('NestedDict', 'rb')      
classes_word_counts = pickle.load(Picklefile1)

Picklefile2 = open('ClassesWordCounts', 'rb')      
total_word_counts = pickle.load(Picklefile2)

Picklefile3 = open('VocCount', 'rb')
vocab_count = pickle.load(Picklefile3)

directory = r'D:\M.tech sem1\NLP\Assignments\A2\20news-19997\\'

for entry in os.listdir(directory):
    if os.path.isdir(os.path.join(directory, entry)):
        folders.append(entry)
        folder_path = os.path.join(r"D:\M.tech sem1\NLP\Assignments\A2\20news-19997", entry)
        files = []
        for entry in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, entry)):
                files.append(entry)
        doc_counts.append(len(files))

for i in range(20):
    doc_sum = doc_sum + doc_counts[i]

for i in range(20):
    a = doc_counts[i]/doc_sum
    
    class_prob.append(a)

for i in range(1,21):
    vocab.append(len(classes_word_counts[i]))

lemmas = []
print("Enter 1 to give a file and 2 to give a sentence:")
choice = int(input())
if choice == 1:
    print("Enter the path of file to be checked :")
    check_file = input()
    fp = open(check_file,"r",encoding="utf8")
    text = fp.read()
    fp.close()

else:
    print("Enter the sentence:")
    text = input()
      
words_list_input = []
text = text.lower()
text = text.translate(text.maketrans('','','\S+@\S+'))
text = re.sub(r'\d+', '', text)
text = text.translate(text.maketrans('','',string.punctuation))
text = re.sub(' +',' ',text)
stop_words = set(stopwords.words("english")) 
word_tokens = word_tokenize(text)
text = [word for word in word_tokens if word not in stop_words]
lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in text]
words_list_input.extend(lemmas)

word_count_input = Counter(words_list_input)
len_input = len(word_count_input)

for w in words_list_input:
    for i in range(20):
        prob_words_in_class[i] = prob_words_in_class[i] + math.log10((classes_word_counts[i+1][w] + 1) / (total_word_counts[i]+vocab_count))

for i in range(20):
    log_classprob = math.log10(class_prob[i])
    prob_doc_in_class.append(prob_words_in_class[i] + log_classprob )

for i in range(20):
    log_prob_doc_in_class.append(prob_doc_in_class[i])
    
max_prob = max(log_prob_doc_in_class)
max_prob_class_index = log_prob_doc_in_class.index(max(log_prob_doc_in_class))
max_prob_class = folders[max_prob_class_index]
print(f"Maximum prob is {max_prob}")
print()
print(f"Maximum prob class is {max_prob_class}")
