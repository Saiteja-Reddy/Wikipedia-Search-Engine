import xml.sax
import re
import string

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

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

    # translation = {}
    # for ele in string.punctuation:
    #     translation[ord(ele)] = ' '
    # fin = fin.translate(translation)

    return fin

class PageHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.title = ""
        self.id = ""
        self.count = 0
        self.net = 0
        self.text = ""
        self.cat_match = re.compile('\[\[category:([^\]}]+)\]\]')

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "page":
            print("*****Page*****")
            self.title = ""
            self.id = ""
            self.count = 0
            self.text = ""
            self.net += 1

    def endElement(self, tag):
        if self.CurrentData == "title":
            print("Title:", self.title)

        elif self.CurrentData == "id":
            if (self.count == 0):
                print("ID :", self.id)
                self.count = self.count + 1
                if int(self.id) == 2178: # 2178 - for ahmad shah massoud, 1166 - for AI
                    print("yes", type(self.id))
                    raise xml.sax.SAXException('Stop Parsing')

        if tag == "text":

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

        self.CurrentData = ""
        if tag == "page":
            print("Now:", self.net)

    def characters(self, content):
        if self.CurrentData == "title":
            self.title += content
        elif self.CurrentData == "id":
            self.id += content
        elif self.CurrentData == "text":
            self.text += content


parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = PageHandler()
parser.setContentHandler( Handler )
parser.parse("wiki-search-small.xml")
