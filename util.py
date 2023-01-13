import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from mido import MidiFile, merge_tracks
# import pygame
import os
import mido
from midiutil import MIDIFile
from mido import MidiFile
import random


'''
Channel list GarageBand
0 - Steinway classic piano (Piano)
1 - Epic Cloud Formation (synth)
3 - Classic Clean (Electric Guitar)
4 - String Ensemble 
5 - String Ensemble 
6 - Full Brass
7 - Trumpets
8 - boutique tunes (VET)
9 - Drum
10 - Funky orgel! (VET)

Drum Pitchs:

high hat :
42 - Closed high hat
44 - padel high hat
46 - Open High hat
56 - Cowbell
80 - silent

tom:
43 - High Floor Tom
41 - low Floor tom
45 - Low tom

snare:
38 - aucustic
'''


def combinemidi(mid1, mid2):
	midi1 = MidiFile(mid1, clip=True)
	midi2 = MidiFile(mid2, clip=True)

	mMid = MidiFile()

	mMid.ticks_per_beat = midi1.ticks_per_beat
	mMid.tracks = midi1.tracks + midi2.tracks
	mMid.save('FinalMidi.mid')
	return True


def combinemidis(midis, i):
	midi1 = MidiFile(midis[0], clip=True)
	midi2 = MidiFile(midis[1], clip=True)
	midi3 = MidiFile(midis[2], clip=True)

	mMid = MidiFile()

	mMid.ticks_per_beat = midi1.ticks_per_beat
	mMid.tracks = midi1.tracks + midi2.tracks
 
	mFinal = MidiFile()
	mFinal.ticks_per_bet = mMid.ticks_per_beat
	mFinal.tracks = midi3.tracks+mMid.tracks
	trackName = "MIDIFILES/augment/TempMidi_"+str(i)+".midi"
	mFinal.save(trackName)
	return True


def read(length):
	'''
	This function reads the midi file and returns the pitch and velocity of the first track
	'''
	songDf = pd.read_csv("Assets/Song.csv", index_col=0)
	times = songDf['time'].to_list()
	maxLength = max([len(songDf.loc[songDf['time'] == el]) for el in np.unique(times)])
	tunes = []
	for el in np.unique(times):
		tempTrack = [0 for i in range(maxLength)]
		temp_df = songDf.loc[songDf['time'] == el]
		pitches = temp_df['pitch'].to_list()
		for i, pitch in enumerate(pitches):
			tempTrack[i] = pitch
			
		tunes.append(tempTrack)
	tunes = tunes[:length]
	
	return np.asarray(tunes).T
		# print(temp_df)
		# print(len(temp_df))

def read2(x = 10):
	'''
	Just read the first track as input variables Old
	'''
	song  = pd.read_csv("Assets/Song.csv", index_col=0)


	track1 = song.loc[song['track'] == 0]['pitch'].to_list()[:x]
	track2 = song.loc[song['track'] == 1]['pitch'].to_list()[:x]
	track3 = song.loc[song['track'] == 2]['pitch'].to_list()[:x]
	# print(new_song)
	return track1, track2, track3

def evaluatePitch(tracks):
	options = [1,2,3,4,5,6,7,8,9,10]
	if samePitch(tracks):
		# print("BORING!")
		return 0
	ding = True
	while ding:
		try:
			rating = int(input(f"\nHow do you evaluate this track? {tracks} (1 - 10)?	 "))
		except:
			rating = int(input(f"\nINVALID!: How do you evaluate this track? {tracks} (1 - 10)?	 "))
		if rating in options:
			ding = False
		else:
			print("Not a possible Answer!")
			ding = True
			
	return int(rating)

def samePitch(tracks):
	
	templs = [len(np.unique(track)) for track in tracks]
	test = sum(templs)/len(templs)
	if test == 1:
		# print("BORING!")
		return True
	else:
		return False


def mapDrumsBack(track):
	
	return ([1 if x != 0 else 0 for x in track])


def mapDrums(value, note):

	binValue  = round(abs(value)) 
	if binValue  == 1:
		if note == "tom":
			return 41
		if note == "hihat":
			return 46
		if note == "snare":
			return 38
		
	else:
		return 0
	

def map(x, min = [0,1], max = [36,82]):
	
	m = interp1d(min,max)
	return int(m(x))

def newgenprint(gen, instrument):
		print("\n")
		print("############################")
		print(f"##### {instrument} generation {gen}")
		print("############################")
		print("\n")

def playmido(file):
	mid = MidiFile(file, clip=True)
	port = mido.open_output(name='foo', virtual=True)
	for msg in mid.play():
		port.send(msg)
  
  
def combineTracks(track1_name, track2_name, output):
	track1 = MidiFile(track1_name, clip=True)
	track2 = MidiFile(track2_name, clip=True)
	
	combined = MidiFile()
	combined.ticks_per_beat = track1.ticks_per_beat
	combined.tracks = track2.tracks + track1.tracks
	combined.save(output)
	return combined

def parseDrums(outputs, length):
	print(outputs, length)
	total = []
	for output in outputs:
		templist = []

		hihat = map(abs(output[0]), [0,1], [0,1])
		if hihat == 0:
			templist.append(0)
		else:
			templist.append(42)
		tom = map(abs(output[1]), [0,1], [0,1])
		if tom == 0:
			templist.append(0)
		else:
			templist.append(41)
		snare = map(abs(output[2]), [0,1], [0,1])
		if snare == 0:
			templist.append(0)
		else:
			templist.append(38)
		total.append(templist)
	return total
		# print(output)
  
  
  
def parseoutputs(output, length, channel):
	# if channel == 9:
	# 	# return parseDrums(output, length)


	lists = []

	pitchRange = [36, 82]
	if channel == 9:
		pitchRange = [30,47]
	if channel == 2:
		pitchRange = [35, 48]
	for i in range(length):
		ding = [map(abs(out), [0,1], pitchRange) for out in np.asarray(output).T[i]]
		lists.append(ding)
	return lists
  
  
def create_midi(tracks, tracknumber, channel = 9, length = 1, rating = True):
	if samePitch(tracks):
		return 0.0

	song = MIDIFile(numTracks=3,deinterleave=True)
	song.addTempo(0,0,200)

	for track in tracks:
		for i, pitch in enumerate(track):
			song.addNote(0, channel, pitch, i, random.randint(1,length), 200)


	trackName = "MIDIFILES/Track_"+str(tracknumber)+".midi"
		
	with open(trackName, 'wb') as output_file:
		song.writeFile(output_file)
	if tracknumber == 0:
		combined = MidiFile("MIDIFILES/Track_0.midi", clip=True)
  
	elif tracknumber == 1:
		combined = combineTracks("MIDIFILES/Track_0.midi", "MIDIFILES/Track_1.midi", "MIDIFILES/DrummNBass.midi")
		trackName = "MIDIFILES/DrummNBass.midi"
	elif tracknumber  == 2:
		combined =  combineTracks("MIDIFILES/DrummNBass.midi", "MIDIFILES/Track_2.midi", "MIDIFILES/FinalSong.midi")
		trackName = "MIDIFILES/FinalSong.midi"
	combined.save("MIDIFILES/Tempofile.midi")
	if rating:
		# playmido(trackName)
		os.system("osascript osascript/runMIDI.scpt")

		rating  = evaluatePitch(tracks)/10

		return rating
	else:
		return True


def create_final_midi(songs, tracknumber):
	'''
	This function creates a midi file from a list of lists of lists of notes
 	'''
	trackNames = []

	for songfile in songs:
		channels, instrument = list(songfile.keys()), list(songfile.values())
		for j, input in enumerate(zip(channels, instrument)):
			channel, trackers = input

			# print(channel, )
			song = MIDIFile(numTracks=3,deinterleave=True)
			song.addTempo(0,0,200)
			for track in trackers:
				for i, pitch in enumerate(track):
					song.addNote(0, channel, int(pitch), i, 1, 200)
	
			trackname = "MIDIFILES/augment/temp/Track_"+str(tracknumber+i+j+random.randint(0, 10000))+".midi"
			trackNames.append(trackname)
			with open(trackname, 'wb') as output_file:
				song.writeFile(output_file)
	print(trackNames)
	combinemidis(trackNames, random.randint(0, 1000))

def augment(array):
	'''
	This function takes in an array of midi files and augments them by adding a random number of tracks
	'''
	augmented = []
	augmented.append(np.flipud(array))
	rotim = np.rot90(array, k = 2)
	augmented.append(rotim)
	augmented.append(np.flipud(rotim))
	return augmented
	