import re

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

f = open('text.txt')
t = f.read()
f.close()


## make lower case
fin = t.lower()
fin = re.sub("<ref.*?>.*?</ref>", "", fin)
fin = re.sub("<ref.*?\/>", "", fin)
fin = re.sub("<ref.*?>", "", fin)
fin = re.sub("</ref>", "", fin)
fin = re.sub("<blockquote.*?>", "", fin)
fin = re.sub("</blockquote>", "", fin)
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



f = open('res.txt', 'w')
f.write(fin)
f.close()