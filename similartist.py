#!/usr/bin/python

#
#	A script for quering a number of artists,
#	printing their biographies and similar
#	artists in a simple html page.
#
#	Author: Thiago Lima
#
#	PyEchoNest API by Echo Nest (http://echonest.com/)

import sys
import codecs
from pyechonest import artist

def queryArtist(name):
	artResult = artist.search(name)
	return artResult[0]	# First result (most relevant)

def printHTML(artists, similar):
	print "<html><head><title>Biographies</title></head><body>"
	print "Content:<ul>"
	for i in range(len(artists)):
		art = artists[i]
		print "<li><a href='#%s'>%s<a>" % (art.name,art.name)
	print "<li><a href='#similar'>Similar Artists</a></ul>"
	for i in range(len(artists)):
		art = artists[i]
		bios = art.biographies
		largest = 0
		# Uses longest biography 
		for b in range(len(bios)):
			if len(bios[b]['text']) > len(bios[largest]['text']):
				largest = b
		bio = bios[largest]['text']
		img = art.images[2]['url']
		print "<br><a id='%s'><br><h1>%s</h1>" % (art.name,art.name)
		print "</h1><img src='%s' style='height:300px'>" % img.encode('utf-8')
		print bio.encode('utf-8')
	print "<br><a id='similar'><br><h1>Similar Artists</h1><ul>"
	for s in similar:
		print "<li>%s" % s
	print "</ul>"
	print "</body></html>"

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Usage:\n\t$ python %s [artist1] [artist2] [artist3] [...] > output.html" % sys.argv[0]
	else:
		artists = []
		for i in range(1,len(sys.argv)):
			artists.append(queryArtist(sys.argv[i]))
		similar = artist.similar(names=artists)
		printHTML(artists,similar)
