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
	index_size = os.path.getsize(index)
	l = 0
	r = index_size
	while l<r:
		m = (l+r)/2
		# print(int(m))
		f.seek(int(m))
		line = f.readline()
		if(line == ""):
			r = index_size
			continue
		line = f.readline()
		output = line.split(" ")
		if(output[0] == word):
			f.close()
			return output
			break
		elif(output[0] > word):
			r = m-1
		else:
			l = m+1
	f.close()
	return [-1, -1, -1]

def process_word(word, field, file_names):
	# total_docs = 5311
	total_docs = 17700000
	token, occur, posting =  get_word_posting(file_names, word)
	if(token == -1):
		print("Not Found")
		return []
	else:
		# print(token + " " + occur + " " + posting)
		heap = []
		# field = 'b'
		posting = posting.split("\n")[0]
		posting = posting.split(",")[:-1]
		ref_count, links_count, info_count, category_count, title_count, body_count = [1 for _ in range(6)]
		query_arr = []
		len_posting = len(posting)
		for post in posting:
			# print post, len(posting)
			ref, links, info, category, title, body = [0 for _ in range(6)]
			if(post.find('r') is not -1):
				post, ref = post.split('r')
				ref_count = ref_count + 1
			if(post.find('l') is not -1):
				post, links = post.split('l')
				links_count = links_count + 1
			if(post.find('i') is not -1):
				post, info = post.split('i')
				info_count = info_count + 1
			if(post.find('c') is not -1):			
				post, category = post.split('c')
				category_count = category_count + 1
			if(post.find('t') is not -1):			
				post, title = post.split('t')
				title_count = title_count + 1
			if(post.find('b') is not -1):	
				post, body = post.split('b')
				body_count = body_count + 1

			if field == 'b':
				tf_idf_val = log10(1 + int(body)) * log10(total_docs/ body_count)
			elif field == 't':
				tf_idf_val = log10(1 + int(title)) * log10(total_docs/ title_count)
			elif field == 'c':
				tf_idf_val = log10(1 + int(category)) * log10(total_docs/ category_count)
			elif field == 'i':
				tf_idf_val = log10(1 + int(info)) * log10(total_docs/ info_count)
			elif field == 'l':
				tf_idf_val = log10(1 + int(links)) * log10(total_docs/ links_count)	
			elif field == 'r':
				tf_idf_val = log10(1 + int(ref)) * log10(total_docs/ ref_count)
			else:
				net = int(body) + int(title) + int(category) + int(info) + int(links) + int(ref)
				# print(len_posting)
				# print(total_docs/ len(posting))
				tf_idf_val = log10(1 + int(net)) * log10(total_docs/ len(posting))
				# print(tf_idf_val)

			# print((int(post),tf_idf_val))
			if(tf_idf_val != 0.0):
				query_arr.append((int(post),tf_idf_val))

		# print(query_arr)
		return(query_arr)

def process_query(queries, file_names):
	query_arrays = []
	for query in queries:
		sym = query.split(":")
		if(len(sym) == 1):
			# sym[0] = sym[0].translate(translator)
			sym[0] = stemmer.stemWord(sym[0].lower())
			query_arrays.append(process_word(sym[0], 'a', file_names))
		else:
			# sym[0] = sym[0].translate(translator)
			sym[0] = stemmer.stemWord(sym[0].lower())
			query_arrays.append(process_word(sym[1], sym[0], file_names))

	# print(len(query_arrays))
	if(len(query_arrays) == 1):
		# print("here in gogo")
		results = query_arrays[0]
		# print("final" + str(results))
	else:
		heap = []
		results = []
		# print("Main " + str(query_arrays))
		# print("")
		for i, arr in enumerate(query_arrays):
			if(len(arr) == 0):
				return results
			if(len(arr) > 0):
				temp = arr.pop(0)
				heapq.heappush(heap, [temp[0], i,  temp[1]])

		flag = 1
		while(len(heap) > 0 and flag == 1):
			top = heapq.heappop(heap)
			count = 1
			tf_idf = top[2]
			if(len(query_arrays[top[1]]) == 0):
				flag = 0
			else:
				temp = query_arrays[top[1]].pop(0)
				heapq.heappush(heap, [temp[0], top[1],  temp[1]])
			# print(heap)
			while(len(heap) > 0 and heap[0][0] == top[0]):
				now = heapq.heappop(heap)
				count = count + 1
				tf_idf = tf_idf + now[2]
				if(count == len(query_arrays)):
					results.append((now[0], tf_idf))
					# print("resuults" + str(results))
				if(len(query_arrays[now[1]]) == 0):
					flag = 0
				else:
					temp = query_arrays[now[1]].pop(0)
					heapq.heappush(heap, [temp[0], now[1],  temp[1]])

		# print("final" + str(results))

	heap = []
	top_count = 10
	for val in results:
		if(len(heap) < top_count):
			heapq.heappush(heap, [val[1], val[0]])
	# 		# print(heap)
		else:
			if(heap[0][0] < val[1]):
				heapq.heappop(heap)
				heapq.heappush(heap, [val[1], val[0]])
				# print(len(heap))
	
	# req = top_count
	# print(heap)
	docs = []
	while(len(heap) > 0):
		docs.insert(0, heapq.heappop(heap))
		# print(heapq.heappop(heap))
	# print(heap)	
	# print(heap)
	print(docs)
	# print("Here")
	# return(docs)

import sys
program_name = sys.argv[0]
arguments = sys.argv[1:]
count = len(arguments)

while True:
	queries = raw_input("Query-> ")
	queries = queries.split()
	start_time = time.time()
	process_query(queries, arguments[0])
	print("Process time : " + str(time.time()-start_time))

