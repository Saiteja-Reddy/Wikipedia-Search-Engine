from lxml import etree
import re
import string
import io


import sys
program_name = sys.argv[0]
arguments = sys.argv[1:]
count = len(arguments)

s_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
s_words.append("name")
s_words.append("br")
s_words.append("nbsp")
# s_words.extend(["nbsp", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
# s_words.extend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

import Stemmer
stemmer = Stemmer.Stemmer('english')

from collections import Counter
inverted_index = {}

docs_interval = 1000
file_counter = 0

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    out = [m.group(0) for m in matches]
    out = ' '.join(out)
    return out.lower()

page_cat_match = re.compile('\[\[category:([^\]}]+)\]\]')
cit = re.compile("{{cite?(?:ation)?(.*?)}}",re.DOTALL )
ref1 = re.compile("<ref((?:[^<])*?)\/>")
ref2 = re.compile("<ref((?:[^<])*?)<\/ref>")
infobox_match = re.compile("{{infobox((?:.|\\n)*?)\n}}")
notes_and_refs_match = re.compile("==\s?notes and references\s?==(.*?)\n\n", re.DOTALL)
ext_links_match = re.compile("==\s?external links\s?==(.*?)\n\n", re.DOTALL)
further_read_match = re.compile("==\s?further reading\s?==(.*?)\n\n", re.DOTALL)
see_also_match = re.compile("==\s?see also\s?==(.*?)\n\n", re.DOTALL)
links_match = re.compile('https?:\/\/[^\s\|]+')

translator = string.maketrans(string.punctuation + '|', ' '*(len(string.punctuation)+1))

def process_body(fin):
    fin = re.sub("\n", "", fin)
    fin = re.sub("<blockquote.*?>(.*?)</blockquote>", r"\1 ", fin)
    fin = fin.rstrip()
    fin = re.sub("{{verify.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{failed.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{page.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{lang.*?fa.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{spaced ndash}}", " ", fin, re.DOTALL)
    fin = re.sub("{{quote.*?\|(.*?)}}", r"\1 ", fin, re.DOTALL)
    fin = re.sub("{{main.*?\|(.*?)}}", r"\1 ", fin, re.DOTALL)
    fin = re.sub("file:.*?\|", " ", fin, re.DOTALL)
    fin = re.sub("<!-*(.*?)-*>", r"\1 ", fin ,re.DOTALL)
    fin = links_match.sub("", fin)
    fin = fin.translate(translator)

    return fin


def process(page_text, page_title, page_id, count):
    global inverted_index
    global file_counter
    global docs_interval

    page_text = page_text.encode("utf-8", "ignore")    
    page_text = remove_non_ascii(page_text)
    page_title = page_title.encode("utf-8", "ignore")    
    page_title = remove_non_ascii(page_title)    

    page_text = page_text.lower()

    cites = cit.findall(page_text)
    page_text = re.sub(cit, "", page_text)

    references = ref1.findall(page_text)
    page_text = re.sub(ref1, "", page_text)

    references += ref2.findall(page_text)
    page_text = re.sub(ref2, "", page_text)
    references = " ".join(references)
    references = links_match.sub("", references)
    references = process_body(references)    

    infoboxes = []
    positions = []
    for match in reversed(list(re.finditer("{{infobox", page_text))):
        start = match.span()[0]
        end = start+2
        flag = 2
        infobox = ""
        for character in page_text[start+2:]:
            end = end + 1
            if flag == 0:
                break
            if character == "{":
                flag = flag + 1
            elif character == "}":
                flag = flag - 1
            else:
                infobox = infobox + character
        page_text = page_text[:start] + page_text[end:] 
        infoboxes.append(infobox)

    infoboxes = " ".join(infoboxes)
    
    spl = infoboxes.split('|')
    infoboxes = ""
    for sp in spl:
        try:
            infoboxes += sp.split("=")[1] + " "
        except:
            infoboxes += sp + " " 
    infoboxes = process_body(infoboxes)    

    page_text = links_match.sub("", page_text)

    category = page_cat_match.findall(page_text)
    page_text = re.sub(page_cat_match, ' ', page_text)
    category = " ".join(category)
    category = process_body(category) ## only translate needed

    notes_and_refs = notes_and_refs_match.findall(page_text, re.DOTALL)
    page_text = re.sub(notes_and_refs_match, ' ', page_text)
    notes_and_refs = " ".join(notes_and_refs)
    notes_and_refs = links_match.sub("", notes_and_refs)
    notes_and_refs = process_body(notes_and_refs)

    ext_links = ext_links_match.findall(page_text, re.DOTALL)
    page_text = re.sub(ext_links_match, ' ', page_text)
    ext_links = " ".join(ext_links)
    ext_links = links_match.sub("", ext_links)
    ext_links = process_body(ext_links)

    further_read = further_read_match.findall(page_text, re.DOTALL)
    page_text = re.sub(further_read_match, ' ', page_text)
    further_read = " ".join(further_read)
    further_read = links_match.sub("", further_read)
    further_read = process_body(further_read)


    see_also = see_also_match.findall(page_text, re.DOTALL)
    page_text = re.sub(see_also_match, ' ', page_text)
    see_also = " ".join(see_also)
    see_also = links_match.sub("", see_also)
    see_also = process_body(see_also)


    now_cites = cites
    cites = ""
    for temp in now_cites:
        a = temp.split('|')
        for b in a:
            if re.search("title", b):
                try:
                    cites += b.split('=')[1] + " "
                except:
                    pass

    cites = links_match.sub("", cites)                    
    cites = process_body(cites)

    references = cites + " " + references + " " + see_also + " " + further_read + " " + notes_and_refs                                                              


    page_text = process_body(page_text)

    page_title = camel_case_split(page_title)
    page_title = page_title.translate(translator)

    
    tokens = page_text.split()
    tokens = [token for token in tokens if token not in s_words]
    stemmed_tokens = stemmer.stemWords(tokens)
    body_counts = Counter(stemmed_tokens)


    tokens = page_title.split()
    tokens = [token for token in tokens if token not in s_words]
    stemmed_tokens = stemmer.stemWords(tokens)
    title_counts = Counter(stemmed_tokens)

    tokens = category.split()
    tokens = [token for token in tokens if token not in s_words]
    stemmed_tokens = stemmer.stemWords(tokens)
    category_counts = Counter(stemmed_tokens)  

    tokens = infoboxes.split()
    tokens = [token for token in tokens if token not in s_words]
    stemmed_tokens = stemmer.stemWords(tokens)
    info_counts = Counter(stemmed_tokens)

    tokens = ext_links.split()
    tokens = [token for token in tokens if token not in s_words]
    stemmed_tokens = stemmer.stemWords(tokens)
    link_counts = Counter(stemmed_tokens)

    tokens = references.split()
    tokens = [token for token in tokens if token not in s_words]
    stemmed_tokens = stemmer.stemWords(tokens)
    ref_counts = Counter(stemmed_tokens)

    all_tokens = set(body_counts.keys())
    all_tokens = all_tokens.union(title_counts.keys())
    all_tokens = all_tokens.union(category_counts.keys())
    all_tokens = all_tokens.union(info_counts.keys())
    all_tokens = all_tokens.union(link_counts.keys())
    all_tokens = all_tokens.union(ref_counts.keys())

    for k in all_tokens:
        counts = str(page_id)
        if k in body_counts:
            counts += "b" +  str(body_counts.get(k))
        if k in title_counts:
            counts += "t" +  str(title_counts.get(k))
        if k in category_counts:
            counts += "c" +  str(category_counts.get(k))
        if k in info_counts:
            counts += "i" +  str(info_counts.get(k))
        if k in link_counts:
            counts += "l" +  str(link_counts.get(k))
        if k in ref_counts:
            counts += "r" +  str(ref_counts.get(k))
        if k in inverted_index:
            inverted_index[k][0] += 1
            inverted_index[k][1] += counts + ","
        else:
            inverted_index[k] = [0 , ""]
            inverted_index[k][0] += 1
            inverted_index[k][1] = counts + ","
        # print(k  + " " + inverted_index[k])

    # print("processed : " + page_title + " " + str(page_id))

    if count ==  docs_interval:
        file_counter = file_counter + 1
        # print(page_title + " writing now")
        # print("writing to " + arguments[1] + str(file_counter))
        filename = "outfiles/" + str(arguments[1]) + str(file_counter)+ ".txt"
        f = open(filename, 'w')
        for key in sorted(inverted_index):
            # if(key == "road"):
                # print(key + " " + inverted_index[key])
                # print(filename)
                # test = open('test.txt', 'w')
                # test.write(key + " " + inverted_index[key] + "\n")
                # test.close()
            f.write(key + " " + str(inverted_index[key][0]) + " " + inverted_index[key][1] + "\n")
        f.close()        
        inverted_index = {}
        count = 0
    return count


infile = arguments[0]
print("using file " + infile)
 
count = 0

context = etree.iterparse(infile, events=('end',))
 
# print(file_counter*docs_interval)
for event, elem in context:
    elem_name = etree.QName(elem.tag)
    if (elem_name.localname == "page"):
        # if file_counter*docs_interval + count > 1000: #1175 for ahmad
           # break
        count += 1
        # print(file_counter*docs_interval + count)
        page_title = ""
        page_id = ""
        page_text = ""
        for child in elem:
            child_name = etree.QName(child.tag)
            if child_name.localname == "title":
                page_title = child.text
                # print(page_title)
            elif child_name.localname == "id":
                page_id = child.text
            elif child_name.localname == "revision":
                for sub in child:
                    sub_name = etree.QName( sub.tag)
                    if sub_name.localname == "text":
                        page_text = sub.text
        # print(str(count) + " " + " " + page_id + " " +  page_title + "\n")                    
        if(page_text != None):
            count = process(page_text , page_title, page_id, count)
        elem.clear()
        # if(page_id == "1928"):
            # print(page_text)

# print(str(inverted_index))
print("final write")
print("writing to " + arguments[1] + str(file_counter+1))
f = open("outfiles/" + str(arguments[1]) + str(file_counter+1)+ ".txt", 'w')
for key in sorted(inverted_index):
    f.write(key + " " + str(inverted_index[key][0]) + " " + inverted_index[key][1] + "\n")
f.close()        
inverted_index = {}


### run initial -  python2 index.py  wiki-search-small.xml outfile

import heapq

fps = []
heap = []

for i in range(1, file_counter + 2):
    curr_file = "outfiles/outfile" + str(i) + ".txt"
    f = open(curr_file, 'r')
    fps.append(f)

for i, fp in enumerate(fps):
    line = fp.readline()
    if(line == ""):
        continue
    line = line.split("\n")[0]
    line = line.split(" ")
    line[1] = int(line[1])
    line.insert(1, i)
    # print(line)
    heapq.heappush(heap, line)
    # print(str(i) + " "  + str(token) + " " + str(postings) )
    # fp.close()

fin_inv = open("outfiles/inv_outfile.txt", "w")

while(len(heap) > 0):
    top = heapq.heappop(heap)
    # print(top , "poptop")
    line = fps[top[1]].readline()
    if line:
        line = line.split("\n")[0]
        line = line.split(" ")
        line[1] = int(line[1])
        line.insert(1, top[1])        
        # print(str(top[1]) + "Here")
        heapq.heappush(heap, line)        
    while(len(heap) > 0 and heap[0][0] == top[0]):
        now = heapq.heappop(heap)
        # print(now)
        top[2] = top[2] +  now[2]
        top[3] = top[3] +  now[3]
        # print (now, "popback")
        line = fps[now[1]].readline()
        if line:
            line = line.split("\n")[0]
            line = line.split(" ")
            line[1] = int(line[1])
            line.insert(1, now[1])        
            # print(str(top[1]) + "Here")
            heapq.heappush(heap, line)       
    # print(top)
    fin_inv.write(top[0] + " " + str(top[2]) + " " + top[3] + "\n")
fin_inv.close()
    # print(top)

for fp in fps:
    fp.close()