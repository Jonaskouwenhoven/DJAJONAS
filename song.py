
# import pygame
import neat
import neat.nn
from util import *
from instrument import Instrument

INSTRUMENTDICT = {9:"Drum", 10:"Orgel", 2:"Bass", 8:"Synth", 3:"Guitar", 7:"Jazz"}
INSTRUMENTOUTPUT = {9:3, 8:3, 4:2, 3:1, 2:1, 7:1, 10:1}
class Song:
    def __init__(self, songlength = 5, generations = 5, pattern = [9, 2, 10]):
        self.CONFIG =  neat.config.Config(neat.genome.DefaultGenome, 
                                            neat.reproduction.DefaultReproduction,
							                neat.species.DefaultSpeciesSet,
                                            neat.stagnation.DefaultStagnation,
							                'config/config_original')
        self.songlength = songlength
        self.input = read2(self.songlength)
        self.testInput = list(self.input)
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
        self.trackNO = 0
        self.ratings = []
        
    def saveRatings(self):
        pass
        
    def getTrack(self, channel, tracknumber, input):

        instrument =  Instrument(self.CONFIG, input,tracknumber, channel, INSTRUMENTOUTPUT[channel], self.generations)
        instrument.instrumenttrack()
        self.line = instrument.FinalTrack
        self.winners.append(instrument.winner[0])
        self.tracks.append(instrument.FinalTrack)

        self.testInput.extend(instrument.FinalTrack)
        self.ratings.append(instrument.bestRatings)
        # saveRatings( )
        print("These are the ratings")
        print(self.tracks)
    
    def updateInput(self):
            inputVar = self.input
            index = -1*(self.trackNO + 1)
            # inputVar[index] = 
            
            pass
        
    def main(self):
        for i, el in enumerate(self.pattern):
            print(f"\n\nNow we are going to evolve the {INSTRUMENTDICT[el]} line")
            self.getTrack(el, i, self.testInput)
            self.trackNO += 1
            # self.updateInput()
            
            self.input = self.tracks
        
        df = pd.DataFrame({"Instrument1":self.ratings[0], "Inst2":self.ratings[1], "Inst3":self.ratings[2]})
        df.to_csv("Assets/Ratings.csv")
        
        tracks = pd.DataFrame({"Instrument1":[self.tracks[0]], "Instrument2":[self.tracks[1]], "Instrument3":[self.tracks[2]]})
        tracks.to_csv("Assets/Tracks.csv")

        
        
    
if __name__ == "__main__":
    song = Song(200, 10 )
    song.main()