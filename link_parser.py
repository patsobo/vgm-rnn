from HTMLParser import HTMLParser
import sys

html_page = sys.argv[1]

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		print "Encountered a start tag:", tag

	def handle_endtag(self, tag):
		print "Encountered an end tag :", tag
	
	def handle_data(self, data):
		print "Encountered some data  :", data

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

print "Starting parser for", html_page

html_file = open(html_page)
html = html_file.read()

parser.feed(html)
