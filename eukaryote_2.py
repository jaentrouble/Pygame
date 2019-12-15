import pygame
import random
import os
import math
import particles_2 as particle
import cytokines_2 as cytokine
import functions_2 as tool
import cells_2 as cell
import viralparticles_2 as vp
IMGDICT = {}
DEFAULTLAYER = cell.DEFAULTLAYER
LAYERDICT = {}

class HumanCell(cell.Eukaryote) :
    def __init__(self, startpos : list, speed : list, imgnum : int = 0) :
        cell.Eukaryote.__init__(self,startpos,speed,imgnum)
        self.c_pamp_list = [vp.Capsid,          # recog by cytoplasmic prr
                            vp.ViralNucleicAcid]
        self.gene.extend([HumanCell.cyto_prr])

    def cyto_prr(self) :
        for something in self.cytosol :
            for cpmp in self.c_pamp_list :
                if issubclass(something, cpmp):
                    if not cytokine.IFN1 in self.cytokine : self.cytokine.append(cytokine.IFN1)


class Th2 (HumanCell) :
    rect = cell.Cell.imgs[2].get_rect()
    IMGDICT['Th2'] = cell.Cell.imgs[2]
    LAYERDICT['Th2'] = DEFAULTLAYER
    def __init__(self, startpos : list, speed : list) :
        HumanCell.__init__(self, startpos, speed, 2)
        self.receptor.extend(['CD4'])

class Macrophage (HumanCell) :
    rect = cell.Cell.imgs[3].get_rect()
    IMGDICT['Macrophage'] = cell.Cell.imgs[3]
    LAYERDICT['Macrophage'] = DEFAULTLAYER
    def __init__(self, startpos : list, speed : list) :
        HumanCell.__init__(self, startpos, speed, 3)
        self.receptor.extend(['MHC2'])
        self.phagosome = []
        self.gene.extend([Macrophage.phagocytosis,Macrophage.lysosome, Macrophage.update_phagosome, \
            Macrophage.attracted])
        self.attractant = ['Nb']

    def phagocytosis (self) :
        for crsh in self.crashed :
            if isinstance(crsh, particle.NecroticBody) :
                crsh.set_speed(0,0)
                self.phagosome.append(crsh)
                    
    def attracted (self) :
        for crsh in self.crashed :
            if isinstance(crsh, particle.Cytokine):
                if self.attractant.count(crsh.name) :
                    newvector = tool.turn_vector(self.speed, [crsh.pos[0]-self.pos[0],crsh.pos[1]-self.pos[1]])
                    self.set_speed(newvector[0],newvector[1])
                    crsh.lysis()

    def lysosome(self) :
        self.phagosome[:] = [ph for ph in self.phagosome if not ph.lysis()]

    def update_phagosome (self) :
        for ph in self.phagosome :
            ph.set_pos(self.pos)

class Epithelium (HumanCell) :
    epithelium_list = []
    rect = cell.Cell.imgs[4].get_rect()
    IMGDICT['Epithelium'] = cell.Cell.imgs[4]
    LAYERDICT['Epithelium'] = DEFAULTLAYER
    def __init__(self, startpos: list, speed : list) :
        HumanCell.__init__(self, startpos, speed, 4)
        self.receptor.extend(['heparansulfate'])
        self.gene.extend([Epithelium.meet_particle])
        Epithelium.epithelium_list.append(self)

    def kill(self) :
        HumanCell.kill(self)
        Epithelium.epithelium_list.remove(self)
        
    def meet_particle (self):
        """
        function to control what to do when collided with some particles
        """
        for crsh in self.crashed :
            if isinstance(crsh,particle.NecroticBody) :
                if not cytokine.Nb in self.cytokine : self.cytokine.append(cytokine.Nb)
        #ptl = []
        #for ptc in particle.Particle.particle_list :
        #    ptl.append(ptc.rect)
        #collided = tool.multi_collide(ptl, self.get_rect())
        #if len(collided)>0 :
        #    for idx in collided :
        #        if type(particle.Particle.particle_list[idx]).__name__ == 'NecroticBody' :
        #            if not 'nb' in self.cytokine : self.cytokine.append('nb')

