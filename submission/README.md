* Instructions to run code:

* First, use the index.py script to generate the index from the wikipedia dump. Input format: python2 index.py wikifile.xml test.txt

* Now, process the test.txt, into separate indexes for different fields. Using the process_index file. Input Format: python2 process_index.py

* Now, generate tf-idf values using get_tfs.py.  Input Format: python2 get_tfs.py

* Now, generate BM25 values using get_okapi_tfs.py.  Input Format: python2 get_okapi_tfs.py

* Next, get documentid-title mapping using get_titles.py file. Input format: python2 get_titles.py wikifile.xml

* Next, get lengths of each document used for BM25 scoring using the get_lengths.py file. Input format: python2 get_titles.py wikifile.xml

* Now to query ---
	* Use search.py / query.py to do 'and' kind of search.
		* Input format: python2 search.py /path/of_index_base
	* Use union_query to do 'and' kind of search followed by 'or' kind of search.
		* Input format: python2 union_query.py /path/of_index_base