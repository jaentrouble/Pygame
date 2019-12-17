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

class IFN1(particle.Cytokine) :
    color = (50,50,235)
    IMGDICT['IFN1'] = particle.Particle.imgs[3].copy()
    IMGDICT['IFN1'].fill(color)
    LAYERDICT['IFN1'] = PARTICLELAYER

    def __init__(self, startpos : list, speed : list) :
        particle.Cytokine.__init__(self, startpos, speed, type(self).__name__, IFN1.color)

class Ab (particle.Cytokine) :
    color = (0,255,0)
    IMGDICT['Ab'] = particle.Particle.imgs[3].copy()
    IMGDICT['Ab'].fill(color)
    LAYERDICT['Ab'] = PARTICLELAYER

    def __init__(self, startpos : list, speed : list) :
        particle.Cytokine.__init__(self, startpos, speed, type(self).__name__, Ab.color)
