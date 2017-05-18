from HTMLParser import HTMLParser
import sys

html_page = sys.argv[1]

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		#print "Encountered a start tag:", tag
		for attr in attrs:
			# make sure you're reading a link
			if attr[0] == 'href':
				# check if it's a midi file
				if (attr[1][-4:] == '.mid'):
					# TODO: store in a data structure or file
					print attr[1]
		

	def handle_endtag(self, tag):
		pass
		#print "Encountered an end tag :", tag
	
	def handle_data(self, data):
		pass
		#print "Encountered some data  :", data

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

print "Starting parser for", html_page

html_file = open(html_page)
html = html_file.read()

parser.feed(html)
