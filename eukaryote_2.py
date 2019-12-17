import pygame
import random
import os
import math
import particles_2 as particle
import cytokines_2 as cytokine
import functions_2 as tool
import cells_2 as cell
import viralparticles_2 as vp
import cellreceptors_2 as creceptor
IMGDICT = {}
DEFAULTLAYER = cell.DEFAULTLAYER
LAYERDICT = {}

class HumanCell(cell.Eukaryote) :
    def __init__(self, startpos : list, speed : list, imgnum : int = 0) :
        cell.Eukaryote.__init__(self,startpos,speed,imgnum)
        self.c_pamp_list = [vp.ViralProtein,          # recog by cytoplasmic prr
                            vp.ViralNucleicAcid]
        self.gene.extend([HumanCell.cyto_prr])
        self.receptor.extend([creceptor.MHC1()])

    def cyto_prr(self) :
        mhc = any(isinstance(r, creceptor.MHC1) for r in self.receptor) #check if it has MHC1
        for something in self.cytosol :
            for cpmp in self.c_pamp_list :
                if issubclass(something, cpmp):
                    if not cytokine.IFN1 in self.cytokine :    #releases IFN type 1
                        self.cytokine.append(cytokine.IFN1)
                    if mhc :
                        for re in self.receptor :
                            if isinstance(re, creceptor.MHC1): # puts foreign object to MHC1
                                if not something in re.antigen:
                                    re.antigen.append(something)
                                break
                    break


class CD4Tcell (HumanCell) :
    rect = cell.Cell.imgs[2].get_rect()
    IMGDICT['CD4Tcell'] = cell.Cell.imgs[2]
    LAYERDICT['CD4Tcell'] = DEFAULTLAYER
    def __init__(self, startpos : list, speed : list) :
        HumanCell.__init__(self, startpos, speed, 2)
        self.receptor.extend([creceptor.CD4()])

class Macrophage (HumanCell) :
    rect = cell.Cell.imgs[3].get_rect()
    IMGDICT['Macrophage'] = cell.Cell.imgs[3]
    LAYERDICT['Macrophage'] = DEFAULTLAYER
    def __init__(self, startpos : list, speed : list) :
        HumanCell.__init__(self, startpos, speed, 3)
        self.receptor.extend([creceptor.MHC2()])
        self.phagosome = []
        self.gene.extend([Macrophage.phagocytosis,Macrophage.lysosome, Macrophage.update_phagosome, \
            Macrophage.attracted])
        self.attractant = [cytokine.Nb, cytokine.IFN1, cytokine.Ab]
        self.phagosis = [particle.NecroticBody, particle.ApoptoticBody]

    def phagocytosis (self) :
        for crsh in self.crashed :
            if any(isinstance(crsh, p) for p in self.phagosis) :
                crsh.set_speed(0,0)
                self.phagosome.append(crsh)
                    
    def attracted (self) :
        for crsh in self.crashed :
            if any(isinstance(crsh, a) for a in self.attractant):
                newvector = tool.turn_vector(self.speed, [crsh.pos[0]-self.pos[0],crsh.pos[1]-self.pos[1]])
                self.set_speed(newvector[0],newvector[1])
                crsh.lysis()

    def lysosome(self) :
        """
        try to lysis anything that's in phagosome; if fail, stil in phagosome
        """
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
        self.receptor.extend([creceptor.Heparansulfate()])
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

class CD8Tcell(HumanCell) :
    rect = cell.Cell.imgs[5].get_rect()
    IMGDICT['CD8Tcell'] = cell.Cell.imgs[5]
    LAYERDICT['CD8Tcell'] = DEFAULTLAYER
    def __init__(self, startpos : list, speed : list) :
        HumanCell.__init__(self, startpos, speed, 5)
        self.receptor.extend([creceptor.CD8()])
        self.gene.extend([CD8Tcell.cytotoxic, CD8Tcell.attracted])
        self.selfantigen = [creceptor.CellReceptor]
        self.attractant = [cytokine.IFN1]

    def cytotoxic(self):
        for crsh in self.crashed :
            if isinstance(crsh, HumanCell) :
                if self.MHC1check(crsh) :
                    crsh.apoptosis()

    def MHC1check(self, crsh : cell.Cell):
        if not len(self.selfantigen) :
            return True
        for r in crsh.receptor :
            if isinstance(r,creceptor.MHC1) :
                for ag in r.antigen :
                    for sa in self.selfantigen :
                        if not issubclass(ag, sa):
                            return True
        return False

    def attracted (self) :
        for crsh in self.crashed :
            if any(isinstance(crsh, a) for a in self.attractant):
                newvector = tool.turn_vector(self.speed, [crsh.pos[0]-self.pos[0],crsh.pos[1]-self.pos[1]])
                self.set_speed(newvector[0],newvector[1])
                crsh.lysis()