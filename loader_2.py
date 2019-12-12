import pygame
import os
import json
import cells_2 as cell
import functions_2 as tool
import particles_2 as particle
import eukaryote_2 as eukaryote
import virus_2 as virus
import cytokines_2 as cytokine
import pathogen_2 as pathogen
import time
import rapidjson

SAVEDIR = 'savefile'

class Loader() :
    def __init__ (self, filename : str, width : int, height : int) :
        pygame.init()
        self.root = os.path.join(SAVEDIR, filename)
        self.imgdict = {}
        self.layerdict = {}
        self.dummies = {}
        self.allgroup = pygame.sprite.LayeredDirty()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.background = pygame.Surface((width, height))
        self.background.fill((255,255,255))
        self.background = self.background.convert()
        
    def run(self) :
        self.load()
        Dummy.groups = self.allgroup
        for name in particle.IMGDICT :
            self.imgdict[name] = particle.IMGDICT[name]
        for name in eukaryote.IMGDICT :
            self.imgdict[name] = eukaryote.IMGDICT[name]
        for name in cytokine.IMGDICT :
            self.imgdict[name] = cytokine.IMGDICT[name]
        for name in virus.IMGDICT :
            self.imgdict[name] = virus.IMGDICT[name]

        for name in particle.LAYERDICT :
            self.layerdict[name] = particle.LAYERDICT[name]
        for name in eukaryote.LAYERDICT :
            self.layerdict[name] = eukaryote.LAYERDICT[name]
        for name in cytokine.LAYERDICT :
            self.layerdict[name] = cytokine.LAYERDICT[name]
        for name in virus.LAYERDICT :
            self.layerdict[name] = virus.LAYERDICT[name]
        mainloop = True
        frame = 0
        frame_max = len(self.sequel)
        self.screen.blit(self.background, (0,0))
        
        while mainloop :
            milliseconds = self.clock.tick(60)
            ##escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 

            ###################
            if frame < frame_max :
                sq = self.sequel[frame]
                for name in sq :
                    if name in self.imgdict :
                        if not name in self.dummies :
                            self.dummies[name] = []
                        sqlen = len(sq[name])
                        dmlen = len(self.dummies[name])
                        if dmlen < sqlen :
                            for _ in range(sqlen - dmlen) :
                                self.dummies[name].append(Dummy(self.imgdict[name], self.layerdict[name]))
                        elif dmlen > sqlen :
                            for _ in range(dmlen-sqlen) :
                                tmp = self.dummies[name].pop()
                                tmp.kill()
                        for n in range(len(self.dummies[name])) :
                            self.dummies[name][n].update(sq[name][n])
            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            frame += 1
            cap = '[FPS] : {0:.1f}, frame : {1}/{2}, sprites : {3}'.format(self.clock.get_fps(), frame, frame_max, len(self.allgroup))
            pygame.display.set_caption(cap)
            pygame.display.flip()

    def load(self) :
        stime = time.time()
        self.sequel = []
        with open(self.root, 'r') as sf :
            for sq in sf :
                self.sequel.append(rapidjson.loads(sq))
        print('load :',time.time()-stime)

class Dummy (pygame.sprite.DirtySprite) :
    def __init__ (self, img, layer) :
        self._layer = layer
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.image = img
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, pos : list) :
        bef = self.rect.copy()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.dirty = 1
        if bef != self.rect :
            self.dirty = 1

if __name__ == '__main__' :
    Loader('1.json', 1000, 300).run()