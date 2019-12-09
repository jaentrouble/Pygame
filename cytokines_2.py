import pygame
import particles_2 as particle
IMGDICT = {}
LAYERDICT = {}
PARTICLELAYER = particle.PARTICLELAYER

class Nb (particle.Cytokine) :
    color = (255,0,0)
    IMGDICT['Nb'] = particle.Particle.imgs[3].copy()
    IMGDICT['Nb'].fill(color)
    LAYERDICT['Nb'] = PARTICLELAYER

    def __init__ (self, startpos : list, speed : list) :
        particle.Cytokine.__init__(self, startpos, speed, type(self).__name__, Nb.color)
