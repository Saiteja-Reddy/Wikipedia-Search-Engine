import xml.sax
import re

class PageHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.title = ""
      self.id = ""
      self.count = 0
      self.net = 0
      self.text = ""
      self.flag = 0
      self.cat_match = re.compile('Category:([^\]]+)\]')

   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "page":
         print("*****Page*****")
         self.count = 0
         # self.net += 1
         if self.net >= 11:
            raise xml.sax.SAXException('Stop Parsing')

         # title = attributes["title"]
         # print "Title:", title

   # Call when an elements ends
   def endElement(self, tag):
      if self.CurrentData == "title":
         print("Title:", self.title)
      elif self.CurrentData == "id":
      	if(self.count == 0):
         print("ID :", self.id)
         self.count = self.count + 1

      if tag == "text":
      	print("Text sample:", self.text)
      	category = self.cat_match.findall(self.text)
      	if(len(category) >= 1):
      		print(category[0].split('|'))


      self.CurrentData = ""
      if(self.net <= 10):
         if tag == "page":
            print("Now:", self.net)

   # Call when a character is read
   def characters(self, content):
      if self.CurrentData == "title":
         self.title = content
      elif self.CurrentData == "id":
        	self.id = content
        	if int(self.id) == 2178:
        		print("yes", type(self.id))
        		raise xml.sax.SAXException('Stop Parsing')
      elif self.CurrentData == "text":
         self.text = content


parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = PageHandler()
parser.setContentHandler( Handler )
parser.parse("sample.xml")
