#!/bin/python
# pimusic.py
# Music selection on raspberry pi

from functools import total_ordering
import re
from os import walk
from subprocess import call

# Define station class
@total_ordering
class Station:
	def __init__(self, name, m3uinfo):
		self.name = name
		self.info = m3uinfo

	def __gt__(self, other):
		if self.name.startswith('http://'):
			if other.name.startswith('http://'):
				return self.name > other.name
			else:
				return true
		elif other.name.startswith('http://'):
			return false
		else:
			return self.name > other.name

	def __eq__(self, other):
		return self.name == other.name

# Get list of m3u files
def getM3uFiles( m3udir ):
	f = []
	for (dirpath, dirnames, filenames) in walk(m3udir):
		for filename in filenames:
			f.append('{}/{}'.format(m3udir,filename))
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
				if re.match(r"#EXTINF:-1,\(#[0-9] - [0-9]+/[0-9]+\) .*", line):
					start = line.find(')')
					name = line[start+1:].strip()
				else:
					name = line[8:].strip()
			elif line.startswith('http://'):
				url = line.strip()
				if name is None:
					name = url
				# finish this stream
				streams.append((name,url))
	return streams

# Given a directory of M3U files, give list of all streams
def getStations( m3udir ):
	stations = []
	files = getM3uFiles(m3udir)
	for f in files:
		#print f
		streams = getInfo(f)
		station = Station(streams[0][0], streams)
		stations.append(station)
		#for stream in streams:
			#print 'Name: ' + stream[0]
			#print ' URL: ' + stream[1]
	return stations

# 
# Menu functions
#

# Show welcome and list of streams
def printStations( stations ):
	print('----------------------------------------------------')
	print('\tItchy Lamp Music Selection')
	print('----------------------------------------------------')
	print('\nPlease choose a station:\n')
	for i, station in enumerate(stations):
		print('{}) {}'.format(i, station.name))
	

# Import files in m3u directory
# 
m3udir = '../m3u'
stations = getStations(m3udir)
stations.sort()
printStations(stations)

# get user input
i = input('Choose a station: ')

# play station
call(['mplayer', stations[int(i)].info[0][1]])

# Donezel washington
