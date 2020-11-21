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

for i in range(len_sorted_freq-1,len_sorted_freq-8,-1):
    sent_prob = sent_prob + math.log10(sorted_freq[i][1] / words_number1)
    print(f"{sorted_freq[i][0]}",end=" ")

print()
print(f"log(probability of the sentence) = {sent_prob}")
