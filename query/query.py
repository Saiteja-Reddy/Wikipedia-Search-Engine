from __future__ import division
import os
import heapq
from math import log10
import time
import string

s_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
s_words.append("name")
s_words.append("br")
s_words.append("nbsp")

translator = string.maketrans(string.punctuation + '|', ' '*(len(string.punctuation)+1))

import Stemmer
stemmer = Stemmer.Stemmer('english')

def get_word_posting(index, word):
	f = open(index, 'r')
	# print(index)
	index_size = os.path.getsize(index)
	l = 0
	r = index_size
	while l<r:
		m = (l+r)/2
		m = int(m)
		# print(int(m))
		print(m)
		f.seek(m)
		line = f.readline()
		if(line == ""):
			r = index_size
			continue
		line = f.readline()
		output = line.split(" ")
		if(output[0] == word):
			f.close()
			# print(output)
			return output
			break
		elif(output[0] > word):
			r = m-1
		else:
			l = m+1
	f.close()
	return [-1, -1, -1]

def get_title(t_id, filename = "out_titles.txt"):
	f = open(filename, 'r')
	index_size = os.path.getsize(filename)
	l = 0
	r = index_size
	line = f.readline()
	output = line.split(",")
	if(int(output[0]) == t_id):
		f.close()
		return output
	while l<r:
		m = (l+r)/2
		f.seek(int(m))
		line = f.readline()
		if(line == ""):
			r = index_size
			continue
		line = f.readline()
		output = line.split(",")
		if(int(output[0]) == t_id):
			print(output)
			f.close()
			return output
			break
		elif(int(output[0]) > t_id):
			r = m-1
		else:
			l = m+1
	f.close()
	return [-1,-1]

def process_word(word, field):
	if field == "t":
		file_name = "indexes/600_tf_index_title.txt"
	elif field == "b":
		file_name = "indexes/600_tf_index_body.txt"
	elif field == "c":
		file_name = "indexes/600_tf_index_category.txt"
	elif field == "i":
		file_name = "indexes/600_tf_index_infobox.txt"
	elif field == "l":
		file_name = "indexes/600_tf_index_links.txt"
	elif field == "r":
		file_name = "indexes/600_tf_index_references.txt"
	else:
		file_name = "indexes/600_tf_index_all.txt"												

	token, idf,  posting =  get_word_posting(file_name, word)
	# print(posting)
	if(token == -1):
		print("Not Found")
		return []
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	tuples = []
	for post in posting:
		if(post.find(field) is not -1):			
			post, title = post.split(field)
			tuples.append((post, title))
			# print(get_title(int(post)))
			# print(get_title(int(post))
			# print((post,title))
	return tuples


process_word("telangana", "a")
# print("done")