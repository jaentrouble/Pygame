import pygame
import random
import os
import math
import particles_2 as particle
import functions_2 as tool
import cells_2 as cell
import viralparticles_2 as vp
PATHOGENLAYER = 1

class Virus (cell.Cell) :
    virus_list = []
    img_idx = [] # idx of virus's images in Cell.imgs
    img_idx.append(1) #0 : Base image
    rect = cell.Cell.imgs[1].get_rect()
    def __init__ (self, startpos : list, speed : list, imgnum : int) :
        cell.Cell.__init__(self, startpos, speed, Virus.img_idx[imgnum])
        self.gene.extend([Virus.infect])
        self.eject_gene = []
        self.host_receptor = [] #receptors the virus recognizes of the cell, list of class
        Virus.virus_list.append(self)
        self.gene_type = vp.ViralNucleicAcid

    def infect(self) :
        """
        insert virus' gene to the host gene
        add its gene_type to host's cytosol
        """
        for crsh in self.crashed :
            if isinstance(crsh, cell.Cell) :
                for r in self.host_receptor :
                    for crecep in crsh.receptor :
                        if isinstance(crecep, r) :
                            for g in self.eject_gene :
                                if not g in crsh.gene :
                                    crsh.gene.append(g)
                            if not self.gene_type in crsh.cytosol :
                                crsh.cytosol[self.gene_type] = 1
                            else:
                                crsh.cytosol[self.gene_type] += 1
                            self.kill()
                            return

    def kill(self) :
        pygame.sprite.DirtySprite.kill(self)
        Virus.virus_list.remove(self)
