word = "navconstel1231"

import os

def get_word_posting(index, word):
	f = open(index, 'r')
	index_size = os.path.getsize(index)
	l = 0
	r = index_size
	while l<r:
		m = (l+r)/2
		print(int(m))
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