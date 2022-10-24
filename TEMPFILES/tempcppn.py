"""
An experiment using NEAT to perform the simple XOR task.
Fitness threshold set in config
- by default very high to show the high possible accuracy of the NEAT library.
"""
import random
import mido
import neat
import neat.nn
from midiutil import MIDIFile
from mido import MidiFile
from util import evaluatePitch, map, read, samePitch, mapDrums

TRACK1, TRACK2, TRACK3 = read(10)

CONFIG = neat.config.Config(neat.genome.DefaultGenome, neat.reproduction.DefaultReproduction,
							neat.species.DefaultSpeciesSet, neat.stagnation.DefaultStagnation,
							'config/config_cppn')


    
def playmido(file):
	mid = MidiFile(file, clip=True)
	# mid = file
 
	port = mido.open_output(name='foo', virtual=True)

	for msg in mid.play():
		# print(msg)
		port.send(msg)

			

def eval_fitness(genomes, config):
	"""
	Fitness function.
	For each genome evaluate its fitness, in this case, as the mean squared error.
	"""

	for i, genome in genomes:
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		track1, track2, track3 = [],[], []
		for i, input in enumerate(zip(TRACK1, TRACK2, TRACK3)):
			input1, input2, input3 = input
			guitar, drums, bass = net.activate([input1, input2, input3, i])
			track1.append(map(abs(guitar)))
			track2.append(map(abs(drums)))
			track3.append(map(abs(bass)))
		extraRating = random.uniform(0.001, 0.01)
		rating = create_midi([track1, track2, track3])
		genome.fitness = abs(rating-extraRating)

  
def eval_drums(genomes, config):
	"""
	Fitness function.
	For each genome evaluate its fitness, in this case, as the mean squared error.
	"""

	for i, genome in genomes:
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		track1, track2, track3 = [],[], []
		for i, input in enumerate(zip(TRACK1, TRACK2, TRACK3)):
			input1, input2, input3 = input
			hihat, tom, snare = net.activate([input1, input2, input3, i])
			track1.append(mapDrums(hihat, "hihat"))
			track2.append(mapDrums(tom, "tom"))
			track3.append(mapDrums(snare, "snare"))
		print(track1, track2, track3)
		extraRating = random.uniform(0.001, 0.01)
		rating = create_midi([track1, track2, track3])
		genome.fitness = abs(rating-extraRating)


def create_midi(tracks):
	if samePitch(tracks[0], tracks[1], tracks[2]):
		return 0.001

	song = MIDIFile(numTracks=3,deinterleave=True)
	song.addTempo(0,0,180)

 
	for i, guitar in enumerate(tracks[0]):
		song.addNote(0, 9, guitar, i, random.randint(1,1), 200)
  
	for i, drums in enumerate(tracks[1]):
		song.addNote(1, 9, drums, i,random.randint(1,1), 200)

	for i, bass in enumerate(tracks[2]):
		song.addNote(2, 9, bass, i,random.randint(1,1), 200)


	with open("track.midi", 'wb') as output_file:
		song.writeFile(output_file)
	
	# song2 = MidiFile("track.midi", clip=True)
	# combined_midi = MidiFile()
	# song2.tracks.append(merge_tracks(combined_midi.tracks))

	playmido("track.midi")


	rating  = evaluatePitch(tracks)/10
	return rating



def run(gens):
	"""
	Create the population and run the XOR task by providing eval_fitness as the fitness function.
	Returns the winning genome and the statistics of the run.
	"""
	pop = neat.population.Population(CONFIG)
	stats = neat.statistics.StatisticsReporter()
	pop.add_reporter(stats)
	pop.add_reporter(neat.reporting.StdOutReporter(True))
	winner = pop.run(eval_drums, gens)
	print("Evolution is done!")
	return winner, stats


if __name__ == '__main__':

	WINNER = run(10)[0]  # Only relevant to look at the winner.

	print('\nOutput:')
	WINNER_NET = neat.nn.FeedForwardNetwork.create(WINNER, CONFIG)
	TRACK1, TRACK2, TRACK3 = read(20)
	track1, track2, track3 = [], [], []
	for i, inputs in enumerate(zip(TRACK1, TRACK2, TRACK3)):
		input1, input2, input3 = inputs
		output = WINNER_NET.activate([input1, input2,input3, i])
		output1, output2, output3 = output
		track1.append(map(abs(output1)))
		track2.append(map(abs(output2)))
		track3.append(map(abs(output3)))
	create_midi([track1, track2, track3])

