# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 14:27:40 2019

@author: ANKIT
"""
import nltk 
import string 
import re 
import os
import math
import operator
import sys
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter 

files = []
files2 = []
words_list1 = []
sentences_list = []
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
        

trigrams =[]
bigrams = []
sent_starting_words = []
sent_first_word = []
for i in range(0,sentences_list_length):
    y = len(sentences_list[i])
    for j in range(y):
        sent = sentences_list[i][j]
        word_tokens = word_tokenize(sent)
        sent = [word for word in word_tokens]
        k = len(sent)
        if k > 0:
            sent_first_word.append(sent[0]) 
        if k > 1:
            pair = (sent[0],sent[1])
            sent_starting_words.append(pair)            
        for m in range(k-2):
            triple = (sent[m],sent[m+1],sent[m+2])
            trigrams.append(triple)
        m=0
        for m in range(k-1):
            pair = (sent[m],sent[m+1])
            bigrams.append(pair)
                     
len_sent_starting_words = len(sent_starting_words)
first_words_count = Counter(sent_starting_words)
sorted_first_words_count = sorted(first_words_count.items(), key=operator.itemgetter(1))
len_sent_first_word = len(sent_first_word)
start_word_count = Counter(sent_first_word)

trigrams_count = Counter(trigrams)     
sorted_trigrams_count = sorted(trigrams_count.items(), key=operator.itemgetter(1))
len_sorted_trigrams_count = len(sorted_trigrams_count)

bigrams_count = Counter(bigrams)
sorted_bigrams_count = sorted(bigrams_count.items(), key=operator.itemgetter(1))
len_sorted_bigrams_count = len(sorted_bigrams_count)

len_sorted_first_words_count  = len(sorted_first_words_count)

print("Enter the sentence:")
sent_check = input()
sent_check = sent_check.lower()
sent_check = sent_check.translate(sent_check.maketrans('','','\S+@\S+'))
sent_check = re.sub(r'\d+', '', sent_check)
sent_check = re.sub('\s+',' ',sent_check)
sent_check = sent_check.translate(sent_check.maketrans('','',string.punctuation))
word_tokens_input = word_tokenize(sent_check)
sent_check = [word for word in word_tokens_input]
sentence_check_len = len(sent_check)

trigrams_input = []
if sentence_check_len < 2:
    print("Insufficient lngth sentence")
    sys.exit(0)

input_starting = (sent_check[0],sent_check[1])
for i in range(sentence_check_len-2):
    triple = (sent_check[i],sent_check[i+1],sent_check[i+2])
    trigrams_input.append(triple)

len_trigrams_input = len(trigrams_input)
sent_prob = math.log10((start_word_count[sent_check[0]] + 1) / (len_sent_first_word + word_freq_len))
sent_prob = sent_prob + math.log10((first_words_count[input_starting] + 1) / (start_word_count[sent_check[0]] + word_freq_len))

for i in range(len_trigrams_input):
    current = trigrams_input[i]
    flag = 0
    dual = (current[0],current[1])
    for j in range(len_sorted_trigrams_count-1,-1,-1):
        x = sorted_trigrams_count[j][0]
        if x[0] == current[0] and x[1] == current[1] and x[2] == current[2]:
            sent_prob = sent_prob + math.log10((trigrams_count[x] + 1) / (bigrams_count[dual] + word_freq_len))
            flag = 1
            break
    if flag == 0:
        sent_prob = sent_prob + math.log10((0 + 1) / (bigrams_count[dual] + word_freq_len))

print()
print(f"Sentence probablity = {sent_prob}")
print()
prod = pow(10,sent_prob)
final = 1/prod
perplexity = pow(final,(1/sentence_check_len))
print(f"perplexity = {perplexity}")
