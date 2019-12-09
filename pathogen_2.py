import pygame
import random
import os
import math
import particles_2 as particle
import functions_2 as tool
import cells_2 as cell
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
        self.host_receptor = [] #receptors the virus recognizes of the cell
        Virus.virus_list.append(self)

    def infect(self) :
        for c in cell.Cell.cell_list :
            if self.rect.colliderect(c.rect) :
                for r in self.host_receptor :
                    if c.receptor.count(r) :
                        for g in self.eject_gene :
                            if not c.gene.count(g) :
                                c.gene.append(g)
                        self.kill()
                        break

    def kill(self) :
        pygame.sprite.DirtySprite.kill(self)
        Virus.virus_list.remove(self)
