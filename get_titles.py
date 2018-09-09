from lxml import etree
import re
import string
import io


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

import sys
program_name = sys.argv[0]
arguments = sys.argv[1:]
print(arguments)
count = len(arguments)

infile = arguments[0]
print("using file " + infile)
 
count = 0

context = etree.iterparse(infile, events=('end',))

outfile = open(arguments[1], 'w')

# print(file_counter*docs_interval)
for event, elem in context:
    elem_name = etree.QName(elem.tag)
    if (elem_name.localname == "page"):

        count += 1

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

        if(page_text != None):
            page_title = page_title.encode("utf-8", "ignore")  
            page_title = remove_non_ascii(page_title)  
            outfile.write(str(page_id) + "," + page_title + "\n");
        elem.clear()
        # if(page_id == "1928"):
            # print(page_text)

outfile.close()
