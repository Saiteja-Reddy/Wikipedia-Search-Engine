from __future__ import division

f = open('doc_counts.txt')

line = f.readline()

b,t,c,i,l,r,n = [0 for i in range(7)]
docs = 0

while line:
	line = line.split(" ")
	docs = docs + 1
	if(docs == 10):
		break
	b = b + int(line[1])
	t = t + int(line[2])
	c = c + int(line[3])
	i = i + int(line[4])
	l = l + int(line[5])
	r = r + int(line[6])
	n = n + int(line[7])
	line = f.readline()

f.close()
print("b", b, b/docs)
print("t", t, t/docs)
print("c", c, c/docs)
print("i", i, i/docs)
print("l", l, l/docs)
print("r", r, r/docs)
print("n", n, n/docs)