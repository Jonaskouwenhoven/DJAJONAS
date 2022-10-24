""" 
This file contains the Drum class
"""
import random
import mido
import neat
import neat.nn
from midiutil import MIDIFile
from mido import MidiFile
from util import *

CONFIGDRUMS = neat.config.Config(neat.genome.DefaultGenome, neat.reproduction.DefaultReproduction,
							neat.species.DefaultSpeciesSet, neat.stagnation.DefaultStagnation,
							'config/config_cppn')

class Drum:
    def __init__(self, config, input, tracknumber, gens = 10):
        self.config = config
        self.gens = gens
        self.input = input
        self.tracknumber = tracknumber
        self.t1 = input[0]
        self.t2 = input[1]
        self.t3 = input[2]
        self.t4 = input[3]
        self.FinalSong = None
        self.FinalTrack = None
        self.winner = None
        self.gen = 0
        
        
    def eval_drums(self, genomes, config):
        """
        Fitness function.
        For each genome evaluate its fitness, in this case, as the mean squared error.
        """
        
        newgenprint(self.gen, "Drums")
        for i, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            track1, track2, track3 = [],[], []
            for i, input in enumerate(zip(self.t1, self.t2, self.t3, self.t4)):
                input1, input2, input3, input4 = input

                hihat, tom, snare = net.activate([input1, input2, input3, input4])
                track1.append(map(abs(hihat), [0,1], [36, 55]))
                track2.append(map(abs(tom), [0,1], [36, 55]))
                track3.append(map(abs(snare), [0,1], [36, 55]))
                # track1.append(mapDrums(hihat, "hihat"))
                # track2.append(mapDrums(tom, "tom"))
                # track3.append(mapDrums(snare, "snare"))

            extraRating = random.uniform(0.001, 0.01)
            rating = create_midi([track1, track2, track3], self.tracknumber, channel= 9)
            genome.fitness = abs(rating-extraRating)
            
        self.gen += 1

    def runDrums(self):
        """
        Create the population and run the XOR task by providing eval_fitness as the fitness function.
        Returns the winning genome and the statistics of the run.
        """
        pop = neat.population.Population(self.config)
        stats = neat.statistics.StatisticsReporter()
        # pop.add_reporter(stats)
        # pop.add_reporter(neat.reporting.StdOutReporter(True))
        winner = pop.run(self.eval_drums, self.gens)

        self.winner = [winner, stats]
        # return winner, stats

    def drumTracks(self):
        """Summary
        This function evolves the drum tracks for the new song
        """
        self.runDrums()
        WINNER = self.winner[0]
        WINNER_NET = neat.nn.FeedForwardNetwork.create(WINNER, self.config)
        track1, track2, track3 = [],[], []
        for i, input in enumerate(zip(self.t1, self.t2, self.t3, self.t4)):
            input1, input2, input3, input4 = input
            hihat, tom, snare = WINNER_NET.activate([input1, input2, input3, input4])
            track1.append(map(abs(hihat), [0,1], [36, 82]))
            track2.append(map(abs(tom), [0,1], [36, 82]))
            track3.append(map(abs(snare), [0,1], [36, 82]))

            # track1.append(mapDrums(hihat, "hihat"))
            # track2.append(mapDrums(tom, "tom"))
            # track3.append(mapDrums(snare, "snare"))

        create_midi([track1, track2, track3], self.tracknumber, channel =9, rating=False)
        # self.FinalSong = song
        # track1 = mapDrumsBack(track1)
        # track2 = mapDrumsBack(track2)
        # track3 = mapDrumsBack(track3)
        self.FinalTrack = [track1, track2, track3]



if __name__ == "__main__":
    inputtest = read(10)
    drum = Drum(CONFIGDRUMS, inputtest)
    drum.drumTracks()