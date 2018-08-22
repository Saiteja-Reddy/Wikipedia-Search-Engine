from lxml import etree
import re
import string

# from nltk.corpus import stopwords
s_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


import Stemmer
stemmer = Stemmer.Stemmer('english')

from collections import Counter
inverted_index = {}

from unidecode import unidecode
def remove_non_ascii(text):
    return unidecode(str(text))


page_cat_match = re.compile('\[\[category:([^\]}]+)\]\]')
cit = re.compile("{{cite?(?:ation)?(.*?)}}")
ref1 = re.compile("<ref((?:[^<])*?)\/>")
ref2 = re.compile("<ref((?:[^<])*?)<\/ref>")
infobox = re.compile("{{infobox((?:.|\\n)*?)\n}}")
notes_and_refs_match = re.compile("==\s?notes and references\s?==.*?\n\n", re.DOTALL)
ext_links_match = re.compile("==\s?external links\s?==.*?\n\n", re.DOTALL)
further_read_match = re.compile("==\s?further reading\s?==.*?\n\n", re.DOTALL)
see_also_match = re.compile("==\s?see also\s?==.*?\n\n", re.DOTALL)

# translator = string.maketrans(string.punctuation, ' '*len(string.punctuation))

translator = {}
for ele in string.punctuation:
    translator[ord(ele)] = ' '


def process_body(fin):
    fin = re.sub("<blockquote.*?>(.*?)</blockquote>", r"\1 ", fin)
    fin = fin.rstrip()
    fin = re.sub("{{verify.*?}}", " ", fin, re.DOTALL)
    # fin = re.sub("{{citation.*?}}", " ", fin, )
    fin = re.sub("{{failed.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{page.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{lang.*?fa.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{spaced ndash}}", " ", fin, re.DOTALL)
    fin = re.sub("{{quote.*?\|(.*?)}}", r"\1 ", fin, re.DOTALL)
    fin = re.sub("{{main.*?\|(.*?)}}", r"\1 ", fin, re.DOTALL)
    fin = re.sub("file:.*?\|", " ", fin, re.DOTALL)
    fin = re.sub("<!-*(.*?)-*>", r"\1 ", fin ,re.DOTALL)

    fin = fin.translate(translator)
    return fin


def process(page_text, page_title, page_id):
    page_text = remove_non_ascii(page_text)
    f = open('text_orig.txt', 'w')
    f.write(page_text)
    f.close()   

    page_text = page_text.lower()

    cites = cit.findall(page_text)
    page_text = re.sub(cit, "", page_text)

    references = ref1.findall(page_text)
    page_text = re.sub(ref1, "", page_text)

    references += ref2.findall(page_text)
    page_text = re.sub(ref2, "", page_text)
    
    page_text = re.sub('https?:\/\/[^\s\|]+', ' ', page_text)

    infoboxes = infobox.findall(page_text)
    page_text = re.sub(infobox, "", page_text)

    category = page_cat_match.findall(page_text)
    page_text = re.sub(page_cat_match, ' ', page_text)

    notes_and_refs = notes_and_refs_match.findall(page_text, re.DOTALL)
    page_text = re.sub(notes_and_refs_match, ' ', page_text)

    ext_links = ext_links_match.findall(page_text, re.DOTALL)
    page_text = re.sub(ext_links_match, ' ', page_text)

    further_read = further_read_match.findall(page_text, re.DOTALL)
    page_text = re.sub(further_read_match, ' ', page_text)

    see_also = see_also_match.findall(page_text, re.DOTALL)
    page_text = re.sub(see_also_match, ' ', page_text)

    f = open('text_other.txt', 'w')
    f.write("cites\n")
    f.write("\n".join(cites))
    f.write("\n\ninfoboxes\n")
    f.write("\n".join(infoboxes))
    f.write("\n\ncategory\n")
    f.write("\n".join(category))
    f.write("\n\nnotes_and_refs\n")
    if(notes_and_refs):
        f.write("\n".join(notes_and_refs))
    f.write("\n\next_links\n")
    if(ext_links):
        f.write("\n".join(ext_links))
    f.write("\n\nfurther_read\n") 
    if(further_read): 
        f.write("\n".join(further_read))
    f.write("\n\nsee_also\n")  
    if(see_also):
        f.write("\n".join(see_also))
    f.write("\n\nreferences\n")  
    f.write("\n".join(references))
    f.write("\n\n")               
    f.close()                                                                     


    f = open('text_bp.txt', 'w')
    f.write(page_text)
    f.close()

    page_text = process_body(page_text)
    print("Heere")
    f = open('text.txt', 'w')
    f.write(page_text)
    f.close() 

    page_text = re.sub("\n", "", page_text)
    tokens = page_text.split()

    tokens = [token for token in tokens if token not in s_words]
    stemmed_tokens = stemmer.stemWords(tokens)
    counts = Counter(stemmed_tokens)
    print("Tokens =  " + str(len(counts)))
    for k in counts.keys():
        if(k in inverted_index):
            inverted_index[k] += str(page_id) + "-" +  str(counts.get(k)) + ","
        else:
            inverted_index[k] =  str(page_id) + "-" +  str(counts.get(k)) + ","


infile = "wiki-search-small.xml"
 
count = 0

context = etree.iterparse(infile, events=('end',), tag='{http://www.mediawiki.org/xml/export-0.8/}page')
 
for event, elem in context:
    count += 1
    # if count >= 19: #1175 for ahmad
        # break
    page_title = ""
    page_id = ""
    page_text = ""
    for child in elem:
        if child.tag == "{http://www.mediawiki.org/xml/export-0.8/}title":
            page_title = child.text
            print(str(count) + " " + page_title + "\n")
        elif child.tag == "{http://www.mediawiki.org/xml/export-0.8/}id":
            page_id = child.text
        elif child.tag == "{http://www.mediawiki.org/xml/export-0.8/}revision":
            for sub in child:
                if sub.tag == "{http://www.mediawiki.org/xml/export-0.8/}text":
                    page_text = sub.text
    if(page_text != None):
        # page_text = page_text.replace(u"\u8211", "-")
        # page_text = page_text.encode('ascii', 'ignore')
        process(page_text , page_title, page_id)
    elem.clear()

import json
with open("json_inverted", 'w') as f:
    json.dump(inverted_index, f)

