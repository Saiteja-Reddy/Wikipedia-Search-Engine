from lxml import etree
import re
import string

# from nltk.corpus import stopwords
s_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


import Stemmer
stemmer = Stemmer.Stemmer('english')

from collections import Counter
inverted_index = {}

translation = {}
for ele in string.punctuation:
    translation[ord(ele)] = ' '

def process_body(fin):
    # fin = t
    fin = re.sub("<blockquote.*?>(.*?)</blockquote>", r"\1 ", fin)
    fin = fin.rstrip()
    # fin = strip_non_ascii(fin)
    fin = re.sub("{{verify.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{citation.*?}}", " ", fin, )
    fin = re.sub("{{failed.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{page.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{lang.*?fa.*?}}", " ", fin, re.DOTALL)
    fin = re.sub("{{spaced ndash}}", " ", fin, re.DOTALL)
    fin = re.sub("{{quote.*?\|(.*?)}}", r"\1 ", fin, re.DOTALL)
    fin = re.sub("{{main.*?\|(.*?)}}", r"\1 ", fin, re.DOTALL)
    fin = re.sub("file:.*?\|", " ", fin, re.DOTALL)
    # fin = re.sub("<\!-*(.*?)-*>", r"\1 ", fin ,re.DOTALL)
    fin = re.sub("<!-*(.*?)-*>", r"\1 ", fin ,re.DOTALL)

    fin = fin.translate(translation)

    return fin

class Page():
    
    def __init__(self, title, text, page_id  ):
        self.title = title
        self.id = page_id
        self.text = text
        self.cat_match = re.compile('\[\[category:([^\]}]+)\]\]')
        # add new elementss here

    def process(self):
        # f = open('text_orig.txt', 'w')
        # f.write(self.text)
        # f.close()   

        self.text = self.text.lower()

        cit = re.compile("{{cite?(?:ation)?(.*?)}}")
        cites = cit.findall(self.text)
        self.text = re.sub(cit, "", self.text)

        ref = re.compile("<ref((?:[^<])*?)\/>")
        references = ref.findall(self.text)
        self.text = re.sub(ref, "", self.text)

        ref = re.compile("<ref((?:[^<])*?)<\/ref>")
        references += ref.findall(self.text)
        self.text = re.sub(ref, "", self.text)
        
        self.text = re.sub('https?:\/\/[^\s\|]+', ' ', self.text)

        infobox = re.compile("{{infobox((?:.|\\n)*?)\n}}")
        infoboxes = infobox.findall(self.text)
        self.text = re.sub(infobox, "", self.text)

        category = self.cat_match.findall(self.text)
        self.text = re.sub(self.cat_match, ' ', self.text)

        notes_and_refs = re.search("==[\s]*?notes and references[\s]*?==.*?(?![=]{2,}).*?\n\n", self.text, re.DOTALL)
        if notes_and_refs:
            start, end = notes_and_refs.span()
            self.text = self.text[:start] + self.text[end:]
            notes_and_refs = notes_and_refs.group()[24:]

        ext_links = re.search("==[\s]*?external links[\s]*?==.*?(?![=]{2,}).*?\n\n", self.text, re.DOTALL)
        if ext_links:
            start, end = ext_links.span()
            self.text = self.text[:start] + self.text[end:]
            ext_links = ext_links.group()[18:]

        further_read = re.search("==[\s]*?further reading[\s]*?==.*?(?![=]{2,}).*?\n\n", self.text, re.DOTALL)
        if further_read:
            start, end = further_read.span()
            self.text = self.text[:start] + self.text[end:]
            further_read = further_read.group()[19:]

        see_also = re.search("==[\s]*?see also[\s]*?==.*?(?![=]{2,}).*?\n\n", self.text, re.DOTALL)
        if see_also:
            start, end = see_also.span()
            self.text = self.text[:start] + self.text[end:]
            see_also = see_also.group()[12:]

        # f = open('text_other.txt', 'w')
        # f.write("cites\n")
        # f.write("\n".join(cites))
        # f.write("\n\ninfoboxes\n")
        # f.write("\n".join(infoboxes))
        # f.write("\n\ncategory\n")
        # f.write("\n".join(category))
        # f.write("\n\nnotes_and_refs\n")
        # if(notes_and_refs):
        #     f.write(notes_and_refs)
        # f.write("\n\next_links\n")
        # if(ext_links):
        #     f.write(ext_links)
        # f.write("\n\nfurther_read\n") 
        # if(further_read): 
        #     f.write(further_read)
        # f.write("\n\nsee_also\n")  
        # if(see_also):
        #     f.write(see_also)
        # f.write("\n\nreferences\n")  
        # f.write("\n".join(references))
        # f.write("\n\n")               
        # f.close()                                                                     


        # f = open('text_bp.txt', 'w')
        # f.write(self.text)
        # f.close()

        self.text = process_body(self.text)
        # print("Heere")
        f = open('text.txt', 'w')
        f.write(self.text)
        f.close() 

        self.text = re.sub("\n", "", self.text)
        tokens = self.text.split()

        tokens = [token for token in tokens if token not in s_words]
        stemmed_tokens = stemmer.stemWords(tokens)
        counts = Counter(stemmed_tokens)
        print("Tokens =  " + str(len(counts)))
        # for k in counts.keys():
        #     if(k in inverted_index):
        #         inverted_index[k] += str(self.id) + "-" +  str(counts.get(k)) + ","
        #     else:
        #         inverted_index[k] =  str(self.id) + "-" +  str(counts.get(k)) + ","


infile = "wiki-search-small.xml"
 
count = 0

context = etree.iterparse(infile, events=('end',), tag='{http://www.mediawiki.org/xml/export-0.8/}page')
 
for event, elem in context:
    count += 1
    # print(count)
    # if count >= 67: #1175 for ahmad
        # break
    # print(elem[0].text)
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
    page = Page(page_title, page_text, page_id)
    if(page_text != None):
        page.process()
    # else:
        # print("None Text\n")
    elem.clear()

import json
with open("json_inverted", 'w') as f:
    json.dump(inverted_index, f)

