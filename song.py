
# import pygame
import neat
import neat.nn
from util import *
from instrument import Instrument

INSTRUMENTDICT = {9:"Drum", 4:"Orgel", 2:"Bass", 8:"Synth", 3:"Guitar"}
INSTRUMENTOUTPUT = {9:3, 8:3, 4:2, 3:2, 2:1}
class Song:
    def __init__(self, songlength = 5, generations = 5, pattern = [3,2,9]):
        self.CONFIG =  neat.config.Config(neat.genome.DefaultGenome, 
                                            neat.reproduction.DefaultReproduction,
							                neat.species.DefaultSpeciesSet,
                                            neat.stagnation.DefaultStagnation,
							                'config/config_original')
        self.songlength = songlength
        self.input = read(self.songlength)
        self.generations = generations
        self.drumTrack = None
        self.bassLine = None
        self.orgelLine = None
        self.pattern = pattern
        self.line = None
        self.winnerDrum = None
        self.winnerBass = None
        self.winnerOrgel = None
        self.winners = []
        self.tracks = []
        
    def getTrack(self, channel, tracknumber, input):

        instrument =  Instrument(self.CONFIG, input,tracknumber, channel, INSTRUMENTOUTPUT[channel], self.generations)
        instrument.instrumenttrack()
        self.line = instrument.FinalTrack
        self.winners.append(instrument.winner[0])
        self.tracks.extend(instrument.FinalTrack)
        
    def main(self):
        for i, el in enumerate(self.pattern):
            print(f"\n\nNow we are going to evolve the {INSTRUMENTDICT[el]} line")
            self.getTrack(el, i, self.input)
            self.input = self.tracks
        
        
    
if __name__ == "__main__":
    song = Song(10, 2)
    song.main()