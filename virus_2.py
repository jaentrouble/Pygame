import pygame
import random
import os
import math
import particles_2 as particle
import functions_2 as tool
import cells_2 as cell
import pathogen_2 as pathogen
import viralparticles_2 as vp
import cellreceptors_2 as creceptor
IMGDICT = {}
LAYERDICT = {}
PATHOGENLAYER = pathogen.PATHOGENLAYER

# for clarity never use self for injecting genes

class HIV (pathogen.Virus) :
    IMGDICT['HIV'] = cell.Cell.imgs[pathogen.Virus.img_idx[0]]
    LAYERDICT['HIV'] = PATHOGENLAYER
    def __init__ (self, startpos : list, speed : list) :
        pathogen.Virus.__init__(self, startpos, speed, 0)
        self.host_receptor.extend([creceptor.CD4])
        self.eject_gene.extend([HIV.replicate, HIV.make_particle])

    def make_particle (host : cell.Eukaryote) :
        host.ribosome.mrna(vp.HIVCapsid, 1000)

    def replicate (host : cell.Eukaryote) :
        if host.cytosol.get(vp.HIVCapsid,False) :
            host.cytosol[vp.HIVCapsid] -= 1
            drt = random.randint(1,4)
            if drt < 3 :
                if drt == 1 :
                    HIV((host.get_rect().centerx,host.get_rect().top-10), tool.rand_2D(1,1))
                else :
                    HIV((host.get_rect().centerx,host.get_rect().bottom+10), tool.rand_2D(1,2))
            else :
                if drt == 3 :
                    HIV((host.get_rect().left-10,host.get_rect().centery), tool.rand_2D(1,3))
                else :
                    HIV((host.get_rect().right+10,host.get_rect().centery), tool.rand_2D(1,4))

class Epi_virus (pathogen.Virus) :
    IMGDICT['Epi_virus'] = cell.Cell.imgs[pathogen.Virus.img_idx[0]]
    LAYERDICT['Epi_virus'] = PATHOGENLAYER
    repnum = 10
    def __init__ (self, startpos : list, speed : list) :
        pathogen.Virus.__init__(self, startpos, speed, 0)
        self.host_receptor.extend([creceptor.Heparansulfate])
        self.eject_gene.extend([Epi_virus.make_particle,Epi_virus.replicate])
        self.gene_type = vp.ViralDNA

    def make_particle (host : cell.Eukaryote) :
        host.ribosome.mrna(vp.EpiCapsid, 300)

    def replicate (host : cell.Eukaryote) :
        if host.cytosol.get(vp.EpiCapsid, False) :
            if host.cytosol[vp.EpiCapsid] > Epi_virus.repnum :
                host.cytosol[vp.EpiCapsid] -= Epi_virus.repnum
                for _ in range(Epi_virus.repnum) :
                    drt = random.randint(1,4)
                    if drt < 3 :
                        if drt == 1 :
                            Epi_virus((host.get_rect().centerx,host.get_rect().top-10), tool.rand_2D(1,1))
                        else :
                            Epi_virus((host.get_rect().centerx,host.get_rect().bottom+10), tool.rand_2D(1,2))
                    else :
                        if drt == 3 :
                            Epi_virus((host.get_rect().left-10,host.get_rect().centery), tool.rand_2D(1,3))
                        else :
                            Epi_virus((host.get_rect().right+10,host.get_rect().centery), tool.rand_2D(1,4))
                host.necrosis()