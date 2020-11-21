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

lemmatizer = WordNetLemmatizer()
files = []
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
len_sorted_bigrams_count = len(sorted_bigrams_count)

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

if(sentence_check_len > 0):
    abc = sent_check[0]
    
bigrams_input = []
for i in range(sentence_check_len-1):
    pair = (sent_check[i],sent_check[i+1])
    bigrams_input.append(pair)

len_bigrams_input = len(bigrams_input)
sentence_check_prob = 0 

sentence_check_prob = math.log10((first_words_count[abc] + 1) / (len_sent_starting_words + word_freq_len))

for z in range(len_bigrams_input):
    current = bigrams_input[z]
    flag = 0
    for j in range(len_sorted_bigrams_count-1,-1,-1):
        x = sorted_bigrams_count[j][0]
        if current[0] == x[0] and current[1] == x[1]:
            sentence_check_prob = sentence_check_prob + math.log10((sorted_bigrams_count[j][1] + 1) / (word_count1[current[0]] + word_freq_len))
            flag = 1
            break
    if flag == 0:
        sentence_check_prob = sentence_check_prob + math.log10((0 + 1) / (word_count1[current[0]] + word_freq_len))

print(f"The log probability of the sentence = {sentence_check_prob}")
print()
prod = pow(10,sentence_check_prob)
final = 1/prod
perplexity = pow(final,(1/sentence_check_len))
print(f"perplexity = {perplexity}")