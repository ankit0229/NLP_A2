import nltk 
import string 
import re 
import os
import math
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter 

lemmatizer = WordNetLemmatizer()

files = []
files2 = []
words_list1 = []
words_list2 = []
vocabulary_list = []
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

    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in text]
    words_list1.extend(lemmas)

vocabulary_list.extend(words_list1)
words_number1 = len(words_list1)
word_count1 = Counter(words_list1)

lemmas = []
directory = r'D:\M.tech sem1\NLP\Assignments\A2\20news-19997\rec.sport.baseball\\'
for entry in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, entry)):
        files2.append(entry)
doc_count2 = len(files2)

for file_name in files2:
    full_path = os.path.join(r"D:\M.tech sem1\NLP\Assignments\A2\20news-19997\rec.sport.baseball", file_name)
    fp = open(full_path,"r")
    text = fp.read()
    fp.close()
    ll = text.split("\n\n")
    del ll[0]    
    text = "\n\n".join(ll)
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('','',string.punctuation))
    text = re.sub(' +',' ',text)

    stop_words = set(stopwords.words("english")) 
    word_tokens = word_tokenize(text)

    text = [word for word in word_tokens if word not in stop_words]

    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in text]
    words_list2.extend(lemmas)

vocabulary_list.extend(words_list2)
words_number2 = len(words_list2)
vocab_count = Counter(vocabulary_list)
vocab_size = len(vocab_count)
word_count2 = Counter(words_list2)

prob_motor = math.log10(doc_count1/(doc_count1 + doc_count2))
prob_base = math.log10(doc_count2/(doc_count1 + doc_count2))

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
text = re.sub(r'\d+', '', text)
text = text.translate(str.maketrans('','',string.punctuation))
text = re.sub(' +',' ',text)
stop_words = set(stopwords.words("english")) 
word_tokens = word_tokenize(text)
text = [word for word in word_tokens if word not in stop_words]
lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in text]
words_list_input.extend(lemmas)

word_count_input = Counter(words_list_input)
len_input = len(word_count_input)

prob_w_motor = 0
prob_w_base = 0

for w in words_list_input:
        prob_w_motor = prob_w_motor + math.log10((word_count1[w] + 1) / (words_number1+vocab_size))
        prob_w_base = prob_w_base + math.log10((word_count2[w] + 1) / (words_number2+vocab_size))
    
prob_file_in_motor = prob_w_motor + prob_motor
prob_file_in_base = prob_w_base + prob_base

print(f"Probability of rec.motorcycles = {prob_file_in_motor}")
print(f"Probability of rec.sport.baseball = {prob_file_in_base}")

if prob_file_in_motor > prob_file_in_base:
    print("rec.motorcycles has highest probability")

if prob_file_in_motor < prob_file_in_base:
    print("rec.sport.baseball has highest probability")