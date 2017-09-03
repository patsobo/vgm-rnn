from HTMLParser import HTMLParser
import sys
import os   # for creating the music directory
import requests # for downloading stuff

'''
    Downloads a bunch of video game midi files.  Nice.

    @arg1 The console for music to find (for now, only nintendo consoles like snes and n64)
    @arg2 The search string to search game titles by

'''

# downloads file
def download_file(base_url, local_filename):
    url = base_url + local_filename
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    # "music/" is the directory you want to save music to
    ensure_dir("music/")
    with open("music/" + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return

# makes sure a directory exists, and creates it if not (in this case,
# it's just to ensure the music/ dir exists
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


# Get the page to find links for
# create the url using the first argument.  Has to be nintendo for now
url = 'http://www.vgmusic.com/music/console/nintendo/' + sys.argv[1] + '/'
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
    def __init__(self, the_filter):
        HTMLParser.__init__(self)
        self.filter = the_filter
        self.in_filter = False

    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        for attr in attrs:
            #print "ATTRIBUTE:", attr

            # check for filter
            if attr[0] == 'name':
                if self.filter.lower() in attr[1].lower():
                    self.in_filter = True
                else:
                    self.in_filter = False

            # make sure you're reading a link
            # and that you're inside the filtered music
            if attr[0] == 'href' and self.in_filter:
                # check if it's a midi file
                if (attr[1][-4:] == '.mid'):
                    # TODO: store in a data structure or file
                    print "MIDI file name:", attr[1]
                    download_file(url, attr[1])


    def handle_endtag(self, tag):
        pass
        #print "Encountered an end tag :", tag

    def handle_data(self, data):
        pass
        #print "Encountered some data  :", data

# instantiate the parser and feed it some HTML
parser = MyHTMLParser(sys.argv[2])

print "Starting parser for", url

#html_file = open(html_page)
html = html_file.read()

parser.feed(html)

#html_file.close()
