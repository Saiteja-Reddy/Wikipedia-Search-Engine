word = "alabama"

import os

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

token, occur, posting =  get_word_posting("outfiles/inv_outfile.txt", word)
if(token == -1):
	print("Not Found")
else:
	print(token + " " + occur + " " + posting)
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	for post in posting:
		ref, links, info, category, title, body = [0 for _ in range(6)]
		if(post.find('r') is not -1):
			post, ref = post.split('r')
		if(post.find('l') is not -1):
			post, links = post.split('l')
		if(post.find('i') is not -1):
			post, info = post.split('i')
		if(post.find('c') is not -1):			
			post, category = post.split('c')
		if(post.find('t') is not -1):			
			post, title = post.split('t')
		if(post.find('b') is not -1):	
			post, body = post.split('b')
		print(post + " b - " + str(body) + " t - " + str(title) + " c - " + str(category) + " i - " + str(info) + " l - " + str(links) + " r - " + str(ref))
	# print(posting)


