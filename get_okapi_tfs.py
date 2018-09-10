from __future__ import division
import os
import heapq
from math import log10
import time
import string
from operator import itemgetter

main_file = open('doc_counts.txt' , 'r')
ht = {}

line = main_file.readline()
while line:
	line = line.split(" ")
	ht[line[0]] = line[1:]
	line = main_file.readline()

main_file.close()
# print(len(ht))



total_docs = 17700000
# avg_docs_len = 

b = open('indexes/index_body.txt', 'r')
t = open('indexes/index_title.txt', 'r')
c = open('indexes/index_category.txt', 'r')
i = open('indexes/index_infobox.txt', 'r')
l = open('indexes/index_links.txt', 'r')
r = open('indexes/index_references.txt', 'r')
a = open('indexes/index_all.txt', 'r')

b1 = open('indexes/okapi/okapi_tf_index_body.txt', 'w')
t1 = open('indexes/okapi/okapi_tf_index_title.txt', 'w')
c1 = open('indexes/okapi/okapi_tf_index_category.txt', 'w')
i1 = open('indexes/okapi/okapi_tf_index_infobox.txt', 'w')
l1 = open('indexes/okapi/okapi_tf_index_links.txt', 'w')
r1 = open('indexes/okapi/okapi_tf_index_references.txt', 'w')
a1 = open('indexes/okapi/okapi_tf_index_all.txt', 'w')


line = t.readline()
line = t.readline()
while line:
	token, posting = line.split(" ")
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	len_posting = len(posting)
	idf = log10((total_docs-len_posting + 0.5)/(len_posting+0.5))
	t_count = 1
	posts = []
	for post in posting:
		post, t_val = post.split('t')
		t_count += 1
		if t_count == 2:
			t1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10((int(t_val)*2.5)/(int(t_val) + 1.5*(0.25 + 0.75*ht[post][1]/1.94285))) * idf
		posts.append((post, tf_idf_val))

	posts.sort(key=itemgetter(1), reverse=True)
	for post in posts:
		t1.write(post[0] + "t" + str(round(post[1],2)) + ",")
	line = t.readline()


line = c.readline()
line = c.readline()
while line:
	token, posting = line.split(" ")
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	len_posting = len(posting)
	idf = log10((total_docs-len_posting + 0.5)/(len_posting+0.5))
	c_count = 1
	posts = []
	for post in posting:
		post, c_val = post.split('c')
		c_count += 1
		if c_count == 2:
			c1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10((int(c_val)*2.5)/(int(c_val) + 1.5*(0.25 + 0.75*ht[post][2]/6.7555))) * idf
		posts.append((post, tf_idf_val))

	posts.sort(key=itemgetter(1), reverse=True)
	for post in posts:
		c1.write(post[0] + "c" + str(round(post[1],2)) + ",")
	line = c.readline()


line = i.readline()
line = i.readline()
while line:
	token, posting = line.split(" ")
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	len_posting = len(posting)
	idf = log10((total_docs-len_posting + 0.5)/(len_posting+0.5))
	i_count = 1
	posts = []
	for post in posting:
		post, i_val = post.split('i')
		i_count += 1
		if i_count == 2:
			i1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10((int(i_val)*2.5)/(int(i_val) + 1.5*(0.25 + 0.75*ht[post][3]/11.6702))) * idf
		posts.append((post, tf_idf_val))

	posts.sort(key=itemgetter(1), reverse=True)
	for post in posts:
		i1.write(post[0] + "i" + str(round(post[1],2)) + ",")
	line = i.readline()

line = l.readline()
line = l.readline()
while line:
	token, posting = line.split(" ")
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	len_posting = len(posting)
	idf = log10((total_docs-len_posting + 0.5)/(len_posting+0.5))
	l_count = 1
	posts = []
	for post in posting:
		post, l_val = post.split('l')
		l_count += 1
		if l_count == 2:
			l1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10((int(l_val)*2.5)/(int(l_val) + 1.5*(0.25 + 0.75*ht[post][4]/1.94285))) * idf
		posts.append((post, tf_idf_val))

	posts.sort(key=itemgetter(1), reverse=True)
	for post in posts:
		l1.write(post[0] + "l" + str(round(post[1],2)) + ",")
	line = l.readline()

line = r.readline()
line = r.readline()
while line:
	token, posting = line.split(" ")
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	len_posting = len(posting)
	idf = log10((total_docs-len_posting + 0.5)/(len_posting+0.5))
	r_count = 1
	posts = []
	for post in posting:
		post, r_val = post.split('r')
		r_count += 1
		if r_count == 2:
			r1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10((int(r_val)*2.5)/(int(r_val) + 1.5*(0.25 + 0.75*ht[post][5]/21.19083))) * idf
		posts.append((post, tf_idf_val))

	posts.sort(key=itemgetter(1), reverse=True)
	for post in posts:
		r1.write(post[0] + "r" + str(round(post[1],2)) + ",")
	line = r.readline()

line = b.readline()
line = b.readline()
while line:
	token, posting = line.split(" ")
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	len_posting = len(posting)
	idf = log10((total_docs-len_posting + 0.5)/(len_posting+0.5))
	b_count = 1
	posts = []
	for post in posting:
		post, b_val = post.split('b')
		b_count += 1
		if b_count == 2:
			b1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10((int(b_val)*2.5)/(int(b_val) + 1.5*(0.25 + 0.75*ht[post][0]/302.535))) * idf
		posts.append((post, tf_idf_val))

	posts.sort(key=itemgetter(1), reverse=True)
	for post in posts:
		b1.write(post[0] + "b" + str(round(post[1],2)) + ",")
	line = b.readline()

line = a.readline()
line = a.readline()
while line:
	token, posting = line.split(" ")
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	len_posting = len(posting)
	idf = log10((total_docs-len_posting + 0.5)/(len_posting+0.5))
	a_count = 1
	posts = []
	for post in posting:
		post, a_val = post.split('a')
		a_count += 1
		if a_count == 2:
			a1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10((int(a_val)*2.5)/(int(a_val) + 1.5*(0.25 + 0.75*ht[post][6]/347.8481))) * idf
		posts.append((post, tf_idf_val))

	posts.sort(key=itemgetter(1), reverse=True)
	for post in posts:
		a1.write(post[0] + "a" + str(round(post[1],2)) + ",")
	line = a.readline()


b.close()
t.close()
c.close()
i.close()
l.close()
r.close()
a.close()

b1.close()
t1.close()
c1.close()
i1.close()
l1.close()
r1.close()
a1.close()
