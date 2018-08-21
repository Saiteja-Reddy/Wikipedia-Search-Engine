from lxml import etree
import re
import string

def process_body(t):
    fin = t
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

    translation = {}
    for ele in string.punctuation:
        translation[ord(ele)] = ' '
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
        f = open('text_orig.txt', 'w')
        f.write(self.text)
        f.close()   

        self.text = self.text.lower()

        cites = []
        positions = []
        for match in re.finditer("{{cite", self.text):
            start = match.span()[0]
            end = start + 6
            flag = 1
            cite = ""
            for character in self.text[start + 6:]:
                end = end + 1
                if flag == 0:
                    break
                if character == "{":
                    flag = flag + 1
                elif character == "}":
                    flag = flag - 1
                else:
                    cite = cite + character
            positions.append((start, end))
            cites.append(cite)
        for i in reversed(positions):
            self.text = self.text[:i[0]] + self.text[i[1]:] 
            
        # self.text = re.sub('<ref.*?\/>', ' ', self.text)
        references = []
        positions = []
        for match in re.finditer('<ref(.*?)\/>', self.text):
            start = match.span()[0]
            end = match.span()[1]
            positions.append((start, end))
            references.append(match.group())
        for i in reversed(positions):
            self.text = self.text[:i[0]] + self.text[i[1]:]

        # self.text = re.sub('<ref.*?>(.|\\n)*?</ref>', ' ', self.text)
        positions = []
        for match in re.finditer('<ref.*?>(.|\\n)*?</ref>', self.text):
            start = match.span()[0]
            end = match.span()[1]
            positions.append((start, end))
            references.append(match.group())
        for i in reversed(positions):
            self.text = self.text[:i[0]] + self.text[i[1]:]            

        # print(references)   
        
        self.text = re.sub('https?:\/\/[^\s\|]+', ' ', self.text)

        infoboxes = []
        positions = []
        for match in re.finditer("{{infobox", self.text):
            start = match.span()[0]
            end = start + 9
            flag = 1
            infobox = ""
            for character in self.text[start + 9:]:
                end = end + 1
                if flag == 0:
                    break
                if character == "{":
                    flag = flag + 1
                elif character == "}":
                    flag = flag - 1
                else:
                    infobox = infobox + character

            positions.append((start, end))
            infoboxes.append(infobox)
        for i in reversed(positions):
            self.text = self.text[:i[0]] + self.text[i[1]:]

        category = self.cat_match.findall(self.text)
        self.text = re.sub('\[\[category:([^\]}]+)\]\]', ' ', self.text)
        # print(category)                    

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

        f = open('text_other.txt', 'w')
        f.write("cites\n")
        f.write("\n".join(cites))
        f.write("\n\ninfoboxes\n")
        f.write("\n".join(infoboxes))
        f.write("\n\ncategory\n")
        f.write("\n".join(category))
        f.write("\n\nnotes_and_refs\n")
        if(notes_and_refs):
            f.write(notes_and_refs)
        f.write("\n\next_links\n")
        if(ext_links):
            f.write(ext_links)
        f.write("\n\nfurther_read\n") 
        if(further_read): 
            f.write(further_read)
        f.write("\n\nsee_also\n")  
        if(see_also):
            f.write(see_also)
        f.write("\n\nreferences\n")  
        f.write("\n".join(references))
        f.write("\n\n")               
        f.close()                                                                     


        f = open('text_bp.txt', 'w')
        f.write(self.text)
        f.close()

        self.text = process_body(self.text)
        f = open('text.txt', 'w')
        f.write(self.text)
        f.close()        



infile = "wiki-search-small.xml"
 
count = 0

context = etree.iterparse(infile, events=('end',), tag='{http://www.mediawiki.org/xml/export-0.8/}page')
 
for event, elem in context:
    count += 1
    # print(count)
    if count >= 447: #1175 for ahmad
        break
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