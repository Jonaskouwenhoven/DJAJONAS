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
from util import *

TRACK1, TRACK2, TRACK3 = read(10)

CONFIGDRUMS = neat.config.Config(neat.genome.DefaultGenome, neat.reproduction.DefaultReproduction,
							neat.species.DefaultSpeciesSet, neat.stagnation.DefaultStagnation,
							'config/config_cppn')


CONFIGGUITAR = neat.config.Config(neat.genome.DefaultGenome, neat.reproduction.DefaultReproduction,
							neat.species.DefaultSpeciesSet, neat.stagnation.DefaultStagnation,
							'config/config_bass')


""" 
DRUM PART
"""

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
		extraRating = random.uniform(0.001, 0.01)
		rating = create_midi([track1, track2, track3])
		genome.fitness = abs(rating-extraRating)

def runDrums(gens):
	"""
	Create the population and run the XOR task by providing eval_fitness as the fitness function.
	Returns the winning genome and the statistics of the run.
	"""
	pop = neat.population.Population(CONFIGDRUMS)
	stats = neat.statistics.StatisticsReporter()
	pop.add_reporter(stats)
	pop.add_reporter(neat.reporting.StdOutReporter(True))
	winner = pop.run(eval_drums, gens)
	print("Evolution is done!")
	return winner, stats

def drumTracks(gens = 10):
	"""Summary
	This function evolves the drum tracks for the new song
	"""
	print(gens)
	WINNER = runDrums(gens)[0]
	WINNER_NET = neat.nn.FeedForwardNetwork.create(WINNER, CONFIGDRUMS)
	track1, track2, track3 = [],[], []
	for i, input in enumerate(zip(TRACK1, TRACK2, TRACK3)):
		input1, input2, input3 = input
		hihat, tom, snare = WINNER_NET.activate([input1, input2, input3, i])
		track1.append(mapDrums(hihat, "hihat"))
		track2.append(mapDrums(tom, "tom"))
		track3.append(mapDrums(snare, "snare"))
	
	print("This is the final Drum Track!")
	create_midi([track1, track2, track3])
	track1 = mapDrumsBack(track1)
	track2 = mapDrumsBack(track2)
	track3 = mapDrumsBack(track3)

	return [track1, track2, track3]

""" 
GUITAR PART
"""

def eval_guitar(genomes, config):
	"""
	Fitness function.
	For each genome evaluate its fitness, in this case, as the mean squared error.
	"""

	for i, genome in genomes:
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		track1 = []
		hihat, tom, snare = DRUMTRACK
		for i, input in enumerate(zip(hihat, tom, snare)):
			# print(input)
			input1, input2, input3 = input
			output1, output2 = net.activate([input1, input2, input3, i])
			# print(output)
			track1.append(map(abs(output1), [0,1], [36, 82]))
			# track2.append(map(abs(output2)))		


		print(track1)
		extraRating = random.uniform(0.001, 0.01)
		rating = create_midi([track1], channel = 2)
		genome.fitness = abs(rating-extraRating)
  
  
def runGuitar(gens):
	pop = neat.population.Population(CONFIGGUITAR)
	stats = neat.statistics.StatisticsReporter()
	pop.add_reporter(stats)
	pop.add_reporter(neat.reporting.StdOutReporter(True))
	winner = pop.run(eval_guitar, gens)
	print("Evolution is done!")
	return winner, stats

def guitarTrack(gens = 10):
	WINNER = runGuitar(gens)[0]
	WINNER_NET = neat.nn.FeedForwardNetwork.create(WINNER, CONFIGGUITAR)








if __name__ == '__main__':

	# DRUMTRACK = drumTracks(5)
	DRUMTRACK = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 1, 0, 0, 1, 1, 0, 1]]
	guitarTrack(5)
	
	# WINNER = run(10)[0]  # Only relevant to look at the winner.
	# WINNER_NET = neat.nn.FeedForwardNetwork.create(WINNER, CONFIGDRUMS)
 
 
	# print('\nOutput:')
 
	
 
	# TRACK1, TRACK2, TRACK3 = read(20)
	# track1, track2, track3 = [], [], []
	# for i, inputs in enumerate(zip(TRACK1, TRACK2, TRACK3)):
	# 	input1, input2, input3 = inputs
	# 	output = WINNER_NET.activate([input1, input2,input3, i])
	# 	output1, output2, output3 = output
	# 	track1.append(map(abs(output1)))
	# 	track2.append(map(abs(output2)))
	# 	track3.append(map(abs(output3)))
	# create_midi([track1, track2, track3])

