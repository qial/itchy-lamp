#!/bin/python
# pimusic.py
# Music selection on raspberry pi

from os import walk

# Get list of m3u files
def getM3uFiles( m3udir ):
	f = []
	for (dirpath, dirnames, filenames) in walk(m3udir):
		for filename in filenames:
			f.append('{}/{}'.format(m3udir,filename)
		break
	return f

# Parse an m3u file to get title and http server
# Returns: array of ( name, url )
# Example EXTINF
# #EXTINF:-1,(#1 - 12/5000) Deep Space One: Deep ambient electronic and space music. [SomaFM]
def getInfo( m3ufile ):
	streams = []		
	with open(m3ufile) as f:
		name = None
		url = None
		for line in f.readlines():
			if line.startswith('#EXTINF:'):
				if(name )
				name = line[8:]
			else if line.startswith('http://'):
				url = line
				if name is None:
					name = url
				# finish this stream
				streams.append((name,url))
	return streams


# Import files in m3u directory
# 
m3udir = '../m3u'

files = getM3uFiles(m3udir)
for f in files:
	print f
	streams = getInfo(f)
	for stream in streams:
		print 'Name: ' + stream[0]
		print ' URL: ' + stream[1]

# Donezel washington
