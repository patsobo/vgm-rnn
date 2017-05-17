# get console.  Must be nintendo for now
console=$1

wget http://www.vgmusic.com/music/console/nintendo/${console} -O music_page.html

python link_parser.py music_page.html
