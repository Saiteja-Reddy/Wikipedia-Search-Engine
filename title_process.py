import os

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
			f.close()
			return output
			break
		elif(int(output[0]) > t_id):
			r = m-1
		else:
			l = m+1
	f.close()
	return [-1,-1]

print(get_title(1234))