import xml.sax
import re

class PageHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.title = ""
      self.id = ""
      self.count = 0
      self.net = 0
      self.text = ""
      self.cat_match = re.compile('\[\[Category:([^\]}]+)\]\]')
      # self.infobox_match = re.compile('{{Infobox')

   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "page":
         print("*****Page*****")
         self.title = ""
         self.id = ""
         self.count = 0
         self.text = ""
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
         if int(self.id) == 2178:
         	print("yes", type(self.id))
         	raise xml.sax.SAXException('Stop Parsing')

      if tag == "text":
      	infoboxes = []
      	positions = []
      	for match in re.finditer("{{Infobox", self.text):
      		start = match.span()[0]
      		end = start+9
      		flag = 1
      		infobox = ""
      		for character in self.text[start+9:]:
      			end = end + 1
      			if flag == 0:
      				break
      			if character == "{":
      				flag = flag + 1
      			elif character == "}":
      				flag = flag - 1
      			else:
      				infobox = infobox + character
      		# print(infobox)
      		# print("pos :", start, " - ",  end)
      		positions.append((start, end))
      		infoboxes.append(infobox)
      	for i in reversed(positions):
      		# print(i)
      		# print(len(self.text), " len is ")
      		# print(self.text[:100])
      		self.text = self.text[:i[0]] + self.text[i[1]:]
      		# print(len(self.text))
      		# print(self.text[:100])

      	print(infoboxes)
      	# print(positions)

      	category = self.cat_match.findall(self.text)
      	# print("Replacing ::::::")
      	self.text = re.sub('\[\[Category:([^\]}]+)\]\]', '', self.text)
      	print(category)

      	# if(len(category) >= 1):
      	# 	print(category[0].split('|'))

      	cites = []
      	positions = []
      	for match in re.finditer("{{[Cc]ite", self.text):
      		start = match.span()[0]
      		end = start+6
      		flag = 1
      		cite = ""
      		for character in self.text[start+6:]:
      			end = end + 1
      			if flag == 0:
      				break
      			if character == "{":
      				flag = flag + 1
      			elif character == "}":
      				flag = flag - 1
      			else:
      				cite = cite + character
      		# print(infobox)
      		# print("pos :", start, " - ",  end)
      		positions.append((start, end))
      		cites.append(cite)
      	for i in reversed(positions):
      		# print(i)
      		# print(len(self.text), " len is ")
      		# print(self.text[:100])
      		self.text = self.text[:i[0]] + self.text[i[1]:]
      		# print(len(self.text))
      		# print(self.text[:100])

      	print(cites)      	


      self.CurrentData = ""
      if(self.net <= 10):
         if tag == "page":
            print("Now:", self.net)

   # Call when a character is read
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
