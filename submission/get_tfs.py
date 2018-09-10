from __future__ import division
import os
import heapq
from math import log10
import time
import string
from operator import itemgetter


total_docs = 17700000

b = open('indexes/index_body.txt', 'r')
t = open('indexes/index_title.txt', 'r')
c = open('indexes/index_category.txt', 'r')
i = open('indexes/index_infobox.txt', 'r')
l = open('indexes/index_links.txt', 'r')
r = open('indexes/index_references.txt', 'r')
a = open('indexes/index_all.txt', 'r')

b1 = open('indexes/tf_index_body.txt', 'w')
t1 = open('indexes/tf_index_title.txt', 'w')
c1 = open('indexes/tf_index_category.txt', 'w')
i1 = open('indexes/tf_index_infobox.txt', 'w')
l1 = open('indexes/tf_index_links.txt', 'w')
r1 = open('indexes/tf_index_references.txt', 'w')
a1 = open('indexes/tf_index_all.txt', 'w')


line = t.readline()
line = t.readline()
while line:
	token, posting = line.split(" ")
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	len_posting = len(posting)
	idf = log10(total_docs/ len_posting)
	t_count = 1
	posts = []
	for post in posting:
		post, t_val = post.split('t')
		t_count += 1
		if t_count == 2:
			t1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10(1 + int(t_val)) * idf
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
	idf = log10(total_docs/ len_posting)
	c_count = 1
	posts = []
	for post in posting:
		post, c_val = post.split('c')
		c_count += 1
		if c_count == 2:
			c1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10(1 + int(c_val)) * idf
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
	idf = log10(total_docs/ len_posting)
	i_count = 1
	posts = []
	for post in posting:
		post, i_val = post.split('i')
		i_count += 1
		if i_count == 2:
			i1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10(1 + int(i_val)) * idf
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
	idf = log10(total_docs/ len_posting)
	l_count = 1
	posts = []
	for post in posting:
		post, l_val = post.split('l')
		l_count += 1
		if l_count == 2:
			l1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10(1 + int(l_val)) * idf
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
	idf = log10(total_docs/ len_posting)
	r_count = 1
	posts = []
	for post in posting:
		post, r_val = post.split('r')
		r_count += 1
		if r_count == 2:
			r1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10(1 + int(r_val)) * idf
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
	idf = log10(total_docs/ len_posting)
	b_count = 1
	posts = []
	for post in posting:
		post, b_val = post.split('b')
		b_count += 1
		if b_count == 2:
			b1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10(1 + int(b_val)) * idf
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
	idf = log10(total_docs/ len_posting)
	a_count = 1
	posts = []
	for post in posting:
		post, a_val = post.split('a')
		a_count += 1
		if a_count == 2:
			a1.write("\n" + token + " " + str(round(idf,2)) + " ")
		tf_idf_val = log10(1 + int(a_val)) * idf
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
