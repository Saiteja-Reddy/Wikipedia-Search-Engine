f = open('test.txt', 'r')

b = open('indexes/index_body.txt', 'w')
t = open('indexes/index_title.txt', 'w')
c = open('indexes/index_category.txt', 'w')
i = open('indexes/index_infobox.txt', 'w')
l = open('indexes/index_links.txt', 'w')
r = open('indexes/index_references.txt', 'w')
a = open('indexes/index_all.txt', 'w')

line = f.readline()
while line:
	token, occur, posting = line.split(" ")
	posting = posting.split("\n")[0]
	posting = posting.split(",")[:-1]
	ref_count, links_count, info_count, category_count, title_count, body_count = [1 for _ in range(6)]
	len_posting = len(posting)
	a.write("\n" + token + " ")	
	for post in posting:
		ref, links, info, category, title, body = [0 for _ in range(6)]
		if(post.find('r') is not -1):
			post, ref = post.split('r')
			ref_count = ref_count + 1
			if ref_count == 2:
				r.write("\n" + token + " ")
		if(post.find('l') is not -1):
			post, links = post.split('l')
			links_count = links_count + 1
			if links_count == 2:
				l.write("\n" + token + " ")			
		if(post.find('i') is not -1):
			post, info = post.split('i')
			info_count = info_count + 1
			if info_count == 2:
				i.write("\n" + token + " ")			
		if(post.find('c') is not -1):			
			post, category = post.split('c')
			category_count = category_count + 1
			if category_count == 2:
				c.write("\n" + token + " ")			
		if(post.find('t') is not -1):			
			post, title = post.split('t')
			title_count = title_count + 1
			if title_count == 2:
				t.write("\n" + token + " ")			
		if(post.find('b') is not -1):	
			post, body = post.split('b')
			body_count = body_count + 1
			if body_count == 2:
				b.write("\n" + token + " ")			

		net = int(body) + int(title) + int(category) + int(info) + int(links) + int(ref)

		if int(body) > 0:
			b.write("," + post + "b" + body)
		if int(title) > 0:
			t.write("," + post + "t" + title)
		if int(category) > 0:
			c.write("," + post + "c" + category)
		if int(info) > 0:
			i.write("," + post + "i" + info)
		if int(links) > 0:
			l.write("," + post + "l" + links)
		if int(ref) > 0:
			r.write("," + post + "r" + ref)	
		if net > 0:
			a.write("," + post + "a" + str(net))

	line = f.readline()														

b.close()
t.close()
c.close()
i.close()
l.close()
r.close()
a.close()
f.close()