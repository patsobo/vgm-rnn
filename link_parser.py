from HTMLParser import HTMLParser
import sys
import requests # for downloading stuff

# Get the page to find links for
# create the url using the first argument.  Has to be nintendo for now
url = 'http://www.vgmusic.com/music/console/nintendo/' + sys.argv[1]
# create the request for the web page
r = requests.get(url)
# get the page contents
html_page = r.content
# turn it into a file
html_file = open("music_page.html", "w+")
html_file.write(html_page)
html_file.close()
html_file = open("music_page.html")

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
					print "MIDI file name:", attr[1]
		

	def handle_endtag(self, tag):
		pass
		#print "Encountered an end tag :", tag
	
	def handle_data(self, data):
		pass
		#print "Encountered some data  :", data

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

print "Starting parser for", url 

#html_file = open(html_page)
html = html_file.read()

parser.feed(html)

#html_file.close()
