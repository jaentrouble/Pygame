import pygame
import random
import os
import math
import particles_2 as particle
import cytokines_2 as cytokine
import functions_2 as tool
import cells_2 as cell
IMGDICT = {}
DEFAULTLAYER = cell.DEFAULTLAYER
LAYERDICT = {}

class Th2 (cell.Eukaryote) :
    rect = cell.Cell.imgs[2].get_rect()
    IMGDICT['Th2'] = cell.Cell.imgs[2]
    LAYERDICT['Th2'] = DEFAULTLAYER
    def __init__(self, startpos : list, speed : list) :
        cell.Eukaryote.__init__(self, startpos, speed, 2)
        self.receptor.extend(['CD4'])

class Macrophage (cell.Eukaryote) :
    rect = cell.Cell.imgs[3].get_rect()
    IMGDICT['Macrophage'] = cell.Cell.imgs[3]
    LAYERDICT['Macrophage'] = DEFAULTLAYER
    def __init__(self, startpos : list, speed : list) :
        cell.Eukaryote.__init__(self, startpos, speed, 3)
        self.receptor.extend(['MHC2'])
        self.phagosome = []
        self.gene.extend([Macrophage.phagocytosis,Macrophage.lysosome, Macrophage.update_phagosome, \
            Macrophage.attracted])
        self.attractant = ['Nb']

    def phagocytosis (self) :
        for ptc in particle.Particle.particle_list :
            if self.rect.colliderect(ptc.rect) :
                if type(ptc).__name__ == 'NecroticBody' :
                    ptc.set_speed(0,0)
                    self.phagosome.append(ptc)
                    
    def attracted (self) :
        for ptc in particle.Particle.particle_list :
            if self.rect.colliderect(ptc.rect) :
                if self.attractant.count(ptc.name) :
                    newvector = tool.turn_vector(self.speed, [ptc.pos[0]-self.pos[0],ptc.pos[1]-self.pos[1]])
                    self.set_speed(newvector[0],newvector[1])
                    ptc.lysis()

    def lysosome(self) :
        self.phagosome[:] = [ph for ph in self.phagosome if not ph.lysis()]

    def update_phagosome (self) :
        for ph in self.phagosome :
            ph.set_pos(self.pos)

class Epithelium (cell.Eukaryote) :
    epithelium_list = []
    rect = cell.Cell.imgs[4].get_rect()
    IMGDICT['Epithelium'] = cell.Cell.imgs[4]
    LAYERDICT['Epithelium'] = DEFAULTLAYER
    def __init__(self, startpos: list, speed : list) :
        cell.Eukaryote.__init__(self, startpos, speed, 4)
        self.receptor.extend(['heparansulfate'])
        self.gene.extend([Epithelium.meet_particle])
        Epithelium.epithelium_list.append(self)

    def kill(self) :
        cell.Eukaryote.kill(self)
        Epithelium.epithelium_list.remove(self)
        
    def meet_particle (self):
        """
        function to control what to do when collided with some particles
        """
        for ptc in particle.Particle.particle_list :
            if self.rect.colliderect(ptc.rect) :
                if type(ptc).__name__ == 'NecroticBody' :
                    if not cytokine.Nb in self.cytokine : self.cytokine.append(cytokine.Nb)
        #ptl = []
        #for ptc in particle.Particle.particle_list :
        #    ptl.append(ptc.rect)
        #collided = tool.multi_collide(ptl, self.get_rect())
        #if len(collided)>0 :
        #    for idx in collided :
        #        if type(particle.Particle.particle_list[idx]).__name__ == 'NecroticBody' :
        #            if not 'nb' in self.cytokine : self.cytokine.append('nb')