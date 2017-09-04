from HTMLParser import HTMLParser
import sys
from subprocess import call
import os   # for creating the music directory
import requests # for downloading stuff

'''
    Downloads a bunch of video game midi files.  Nice.

    @arg1 The console for music to find (for now, only nintendo consoles like snes and n64)
    @arg2 The search string to search game titles by

'''

# stitches all the downloaded midi files into one file named input.txt,
# as per the specifications laid out by karpathy's char-rnn
def concat_files(source_dir, dest_dir):
    print "Concatenating files and saving to", dest_dir
    ensure_dir(dest_dir)
    with open(dest_dir + "input.txt", 'w') as outfile:
        for fname in os.listdir(source_dir):
            # convert to a csv format first
            print('midicsv ' + source_dir + fname + ' ' + source_dir + fname + '.txt')
            os.system('midicsv ' + source_dir + fname + ' ' + source_dir + fname + '.txt')
            with open(source_dir + fname + ".txt") as infile:
                for line in infile:
                    outfile.write(line)
            # delete the file we made cause it's useless
            #os.system("rm " + fname + ".txt")

    print "Successfully concatenated files."
    return

# downloads file
def download_file(base_url, local_filename, parent_dir):
    url = base_url + local_filename
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    # "music/" is the directory you want to save music to
    ensure_dir(parent_dir)
    with open(parent_dir + local_filename, 'wb') as f:
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
    def __init__(self, the_filter, midi_dir):
        HTMLParser.__init__(self)
        self.filter = the_filter
        self.file_dir = midi_dir
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
                    download_file(url, attr[1], self.file_dir)


    def handle_endtag(self, tag):
        pass
        #print "Encountered an end tag :", tag

    def handle_data(self, data):
        pass
        #print "Encountered some data  :", data



# set the directories; one to write the downloaded midi files to, and the other
# is the one inside the char-rnn project (the data/ folder)
midi_dir = "music/"
char_rnn_dir = "char-rnn/data/" + sys.argv[2] + "/"

# only re-download if music/ directory does not exist
# instantiate the parser and feed it some HTML
parser = MyHTMLParser(sys.argv[2], midi_dir)

print "Starting parser for", url

#html_file = open(html_page)
html = html_file.read()

parser.feed(html)

#html_file.close()

# stitch files together and send to char-rnn
concat_files(midi_dir, char_rnn_dir)
