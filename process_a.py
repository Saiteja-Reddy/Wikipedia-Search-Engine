f = open("text_orig.txt", 'r')
t = f.read()
f.close()

import nltk
tokens = nltk.word_tokenize(t)

import re
t = re.sub("\n", "", t)
# tokens = set(tokens)
from nltk.corpus import stopwords

s_words = stopwords.words("english")
tokens = [token for token in tokens if token not in s_words]

from nltk.stem.porter import *
stemmer = PorterStemmer()
stemmed = [stemmer.stem(token) for token in tokens]

from collections import Counter
counts = Counter(stemmed)


import Stemmer
stemmer = Stemmer.Stemmer('english')
stemmed_tokens = stemmer.stemWords(tokens)

cit = re.compile("{{cite?(?:ation)?.*?}}")
cites = cit.findall(t)
t = re.sub(cit, "", t)

ref = re.compile("<ref(?:[^<])*?\/>")
refs = ref.findall(t)
t = re.sub(ref, "", t)

ref = re.compile("<ref(?:[^<])*?<\/ref>")
refs += ref.findall(t)
t = re.sub(ref, "", t)



