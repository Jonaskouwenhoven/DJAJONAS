""" 
This file contains the orgel class
"""
import random
import configparser
# from this import s
import mido
import neat
import neat.nn
from midiutil import MIDIFile
from mido import MidiFile
from util import *

INSTRUMENTDICT = {9:"Drum", 4:"Orgel", 2:"Bass", 8:"Synth", 3:"Guitar"}

CONFIGINSTRUMENT = neat.config.Config(neat.genome.DefaultGenome, neat.reproduction.DefaultReproduction,
							neat.species.DefaultSpeciesSet, neat.stagnation.DefaultStagnation,
							'config/config_original')

def readConfig(Filename):
		return neat.config.Config(neat.genome.DefaultGenome, neat.reproduction.DefaultReproduction,
							neat.species.DefaultSpeciesSet, neat.stagnation.DefaultStagnation,
							Filename)
class Instrument:
	def __init__(self, config, input, tracknumber, instrumentChannel, outputs, gens = 10):
		"""_summary_

		Args:
			config (config): The classic config file, gets adjusted based on lenght inputs and outputs
			input (track): the input pitches
			tracknumber (int): when is this track created? first (1), second (2), ...
			instrumentChannel (int): the channel corresponding to the insturment
			outputs (int): how mant items are outputted
			gens (int, optional): number of generations, Defaults to 10.
		"""
		self.config = config
		self.input = input
		self.FinalSong = None
		self.FinalTrack = None
		self.tracknumber = tracknumber
		self.outputs = outputs
		self.instrument = instrumentChannel
		self.gens = gens
		self.winner = None
		self.gen = 0

	
	
	def eval_instrument(self, genomes, config):
		"""
		Fitness function.
		For each genome evaluate its fitness, in this case, as the mean squared error.
		"""
		newgenprint(self.gen, INSTRUMENTDICT[self.instrument])
		for i, genome in genomes:
			net = neat.nn.FeedForwardNetwork.create(genome, config)
			outputs = []
			for input in np.asarray(self.input, dtype=object).T:
				output = net.activate(input)
				outputs.append(output)

			tracks = parseoutputs(outputs, self.outputs)
			extraRating = random.uniform(0.001, 0.01)
			rating = create_midi(tracks, self.tracknumber, channel = self.instrument)
			genome.fitness = abs(rating-extraRating)
		self.gen+= 1
  
	def adjustConfig(self):
		print(self.input)
		config = configparser.ConfigParser()
		config.read("config/config_original")

		config['DefaultGenome']['num_inputs'] = str(len(self.input))
		config['DefaultGenome']['num_outputs'] = str((self.outputs))
		# print(self.input)
		# print(config['DefaultGenome']['num_inputs'])
		# self.config = config
		with open('config/testconfig', 'w') as configfile:
			config.write(configfile)
		self.config = readConfig("config/testconfig")



	def runinstrument(self):
		self.adjustConfig()
		pop = neat.population.Population(self.config)
		stats = neat.statistics.StatisticsReporter()
		# pop.add_reporter(stats)
		# pop.add_reporter(neat.reporting.StdOutReporter(True))

		winner = pop.run(self.eval_instrument, self.gens)
		self.winner = [winner, stats]

	def instrumenttrack(self):
		self.runinstrument()
		WINNER = self.winner[0]
		WINNER_NET = neat.nn.FeedForwardNetwork.create(WINNER, self.config)
		outputs = []
		for input in np.asarray(self.input).T:

			output = WINNER_NET.activate(input)
			outputs.append(output)
		track = parseoutputs(outputs, self.outputs)
		create_midi(track, self.tracknumber, channel = self.instrument, rating = False)
  

		# self.FinalSong = song
		self.FinalTrack = track

if __name__ == "__main__":
	DRUMTRACK = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 1, 0, 0, 1, 1, 0, 1]]
	g = Instrument(CONFIGINSTRUMENT, DRUMTRACK, 0, 9, 2)
	g.instrumenttrack()