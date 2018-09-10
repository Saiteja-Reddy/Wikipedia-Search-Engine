import string

translator = string.maketrans(string.punctuation + '|', ' '*(len(string.punctuation)+1))


def preprocess(query):
	# print(query)
	queries = query.split(" ")
	fin = ""
	for query in queries:
		if(":" in query):
			sym = query.split(":")
			query = sym[1]
			query = query.translate(translator)
			query = query.split(" ")
			for a in query:
				fin = fin + sym[0] + ":" + a + " "
				# print((sym[0], a))
		else:
			fin = fin + query
			# print(query)
	return(fin)

preprocess(raw_input("Query-> "))