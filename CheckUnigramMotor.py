# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 00:55:01 2019

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
directory = r'D:\M.tech sem1\NLP\Assignments\A2\20news-19997\rec.motorcycles\\'

for entry in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, entry)):
        files.append(entry)
doc_count1 = len(files)

for file_name in files:
    full_path = os.path.join(r"D:\M.tech sem1\NLP\Assignments\A2\20news-19997\rec.motorcycles", file_name)
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
    words_list1.extend(text)

words_number1 = len(words_list1)
word_count1 = Counter(words_list1)
sent_prob = 0
sorted_freq = sorted(word_count1.items(), key=operator.itemgetter(1))
len_sorted_freq = len(sorted_freq)

print("Enter the input sentence:")
sentence_check = input()

sentence_check = sentence_check.lower()
sentence_check = sentence_check.translate(sentence_check.maketrans('','','\S+@\S+'))
    
sentence_check = re.sub(r'\d+', '', sentence_check)
sentence_check = sentence_check.translate(sentence_check.maketrans('','',string.punctuation))
sentence_check = re.sub(' +',' ',sentence_check)
stop_words = set(stopwords.words("english"))
word_tokens_input = word_tokenize(sentence_check)
sentence_check = [word for word in word_tokens_input if word not in stop_words]
sentence_check_len = len(sentence_check)
   
sentence_check_prob = 0
for j in range(sentence_check_len):
    current = sentence_check[j]
    sentence_check_prob = sentence_check_prob + math.log10((word_count1[current] + 1) / (words_number1 + len_sorted_freq))

print(f"log(probability of input sentence) = {sentence_check_prob}")
print()
prod = pow(10,sentence_check_prob)
final = 1/prod
perplexity = pow(final,(1/sentence_check_len))
print(f"perplexity = {perplexity}")



    
