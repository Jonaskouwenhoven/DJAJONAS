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

def read(x = 10):
	'''
	Just read the first track as input variables
	'''
	song  = pd.read_csv("Assets/Song.csv", index_col=0)
	# print(song)
	track1 = song.loc[song['track'] == 0]['pitch'].to_list()[:x]
	track2 = song.loc[song['track'] == 1]['pitch'].to_list()[:x]
	track3 = song.loc[song['track'] == 2]['pitch'].to_list()[:x]
	# track4 = song.loc[song['track'] == 4]['pitch'].to_list()[:x]

	# track4 = song.loc[song['track'] == ]

	# print(new_song)
	return track1, track2, track3

def evaluatePitch(tracks):
	options = [1,2,3,4,5,6,7,8,9,10]
	if samePitch(tracks):
		# print("BORING!")
		return 0
	ding = True
	while ding:
		rating = int(input(f"\nHow do you evaluate this track? (1 - 10)?	 "))
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
  
def parseoutputs(output, length):
    # print(output, length)
    lists = []
    for i in range(length):
        ding = [map(abs(out), [0,1], [36, 82]) for out in np.asarray(output).T[i]]
        lists.append(ding)
    return lists
  
  
def create_midi(tracks, tracknumber, channel = 9, length = 1, rating = True):
	if samePitch(tracks):
		return 0.001

	song = MIDIFile(numTracks=3,deinterleave=True)
	song.addTempo(0,0,180)

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
