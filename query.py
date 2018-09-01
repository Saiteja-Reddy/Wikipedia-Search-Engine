import os
import heapq
from math import log10
import time

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

def process_word(word, field):
	total_docs = 5311
	token, occur, posting =  get_word_posting("outfiles/inv_outfile.txt", word)
	if(token == -1):
		print("Not Found")
	else:
		print(token + " " + occur + " " + posting)
		heap = []
		# field = 'b'
		top_count = 10
		posting = posting.split("\n")[0]
		posting = posting.split(",")[:-1]
		ref_count, links_count, info_count, category_count, title_count, body_count = [1 for _ in range(6)]
		query_arr = []
		for post in posting:
			# print post
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
				tf_idf_val = log10(1 + int(net)) * log10(total_docs/ len(posting))

			if(tf_idf_val != 0.0):
				query_arr.append((int(post),tf_idf_val))

		return(query_arr)
		# 	if(len(heap) < top_count):
		# 		heapq.heappush(heap, [tf_idf_val, int(post)])
		# 		# print(heap)
		# 	else:
		# 		if(heap[0][0] < tf_idf_val):
		# 			heapq.heappop(heap)
		# 			heapq.heappush(heap, [tf_idf_val, int(post)])
		# 			# print(len(heap))
		# 	# print(post + " b - " + str(body) + " t - " + str(title) + " c - " + str(category) + " i - " + str(info) + " l - " + str(links) + " r - " + str(ref))
		
		# req = top_count
		# # print(heap)
		# while(len(heap) > 0 and req > 0):
		# 	req = req - 1
		# 	print(heapq.heappop(heap))
		# # print(heap)	

def process_query(queries):
	query_arrays = []
	for query in queries:
		sym = query.split(":")
		if(len(sym) == 1):
			query_arrays.append(process_word(sym[0], 'a'))
		else:
			query_arrays.append(process_word(sym[1], sym[0]))

	heap = []
	results = []
	print(query_arrays)
	print("")
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

	print("final" + str(results))
	# print(heap)

while True:
	queries = raw_input("Query-> ")
	queries = queries.split()
	process_query(queries)
	# start_time = time.time()
	# for query in queries:
	# process_word(query, 'a')
	# print("Process time : " + str(time.time()-start_time))

