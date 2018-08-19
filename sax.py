import xml.sax
import re

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def process_body(t):
    fin = t.lower()
    fin = re.sub("<blockquote.*?>(.*?)</blockquote>", r"\1", fin)
    fin = fin.rstrip()
    fin = strip_non_ascii(fin)
    fin = re.sub("{{verify.*?}}", "", fin)
    fin = re.sub("{{citation.*?}}", "", fin)
    fin = re.sub("{{failed.*?}}", "", fin)
    fin = re.sub("{{page.*?}}", "", fin)
    fin = re.sub("{{lang.*?fa.*?}}", "", fin)
    fin = re.sub("{{spaced ndash}}", "", fin)
    fin = re.sub("{{quote.*?\|(.*?)}}", r"\1", fin)
    fin = re.sub("{{main.*?\|(.*?)}}", r"\1", fin)
    return fin

class PageHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.title = ""
        self.id = ""
        self.count = 0
        self.net = 0
        self.text = ""
        self.cat_match = re.compile('\[\[Category:([^\]}]+)\]\]')

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
                if int(self.id) == 2178:
                    print("yes", type(self.id))
                    raise xml.sax.SAXException('Stop Parsing')

        if tag == "text":

            cites = []
            positions = []
            for match in re.finditer("{{[Cc]ite", self.text):
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

            self.text = re.sub('<ref.*?\/>', '', self.text)
            self.text = re.sub('<ref.*?>.*?</ref>', '', self.text)
            self.text = re.sub('https?:\/\/[^\s\|]+', '', self.text)
            infoboxes = []
            positions = []
            for match in re.finditer("{{Infobox", self.text):
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
            self.text = re.sub('\[\[Category:([^\]}]+)\]\]', '', self.text)

            notes_and_refs = re.search("==Notes and references==[^=]*?[*?][^=]*?\n\n", self.text, re.DOTALL)
            if notes_and_refs:
                start, end = notes_and_refs.span()
                self.text = self.text[:start] + self.text[end:]
                notes_and_refs = notes_and_refs.group()[24:]

            ext_links = re.search("==External links==[^=]*?[*?][^=]*?\n\n", self.text, re.DOTALL)
            if ext_links:
                start, end = ext_links.span()
                self.text = self.text[:start] + self.text[end:]
                ext_links = ext_links.group()[18:]

            further_read = re.search("==Further reading==[^=]*?[*?][^=]*?\n\n", self.text, re.DOTALL)
            if further_read:
                start, end = further_read.span()
                self.text = self.text[:start] + self.text[end:]
                further_read = further_read.group()[19:]

            see_also = re.search("==See also==[^=]*?[*?][^=]*?\n\n", self.text, re.DOTALL)
            if see_also:
                start, end = see_also.span()
                self.text = self.text[:start] + self.text[end:]
                see_also = see_also.group()[12:]

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
