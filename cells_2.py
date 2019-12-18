import pygame
import random
import os
import math
import particles_2 as particle
import cytokines_2 as cytokine
import functions_2 as tool
import cellorgan_2 as cellorgan
from layerconst_2 import *

IMAGE = 'image'

EASYMITOCHONDRIA = False

class Cell(pygame.sprite.DirtySprite) :
    """
    Any thing that has receptors and genes
    Genes should not have any other parameters than self
    """
    imgs = []
    cell_list = []
    try :
        imgs.append(pygame.image.load(os.path.join(IMAGE, "eukaryote.png")))       #0
        imgs.append(pygame.image.load(os.path.join(IMAGE, "virus.png")))           #1
        imgs.append(pygame.image.load(os.path.join(IMAGE, "CD4.png")))             #2
        imgs.append(pygame.image.load(os.path.join(IMAGE, "macrophage.png")))      #3
        imgs.append(pygame.image.load(os.path.join(IMAGE, "epithelium.png")))      #4
        imgs.append(pygame.image.load(os.path.join(IMAGE, "CD8.png")))             #5
        imgs.append(pygame.image.load(os.path.join(IMAGE, "prokaryote.png")))      #6
        imgs.append(pygame.image.load(os.path.join(IMAGE, "coccus_positive.png"))) #7

    except:
        raise UserWarning( "Unable to load Cell images")

    def __init__ (self, startpos : list, speed : list, imgnum : int) :
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.image = Cell.imgs[imgnum]
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = list(startpos).copy()       # Need 'pos' value to use real values, refers to centerx, centery
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.speed = list(speed).copy()
        self.acc = [0,0]
        self.gene = [Cell.update_pos]    #list of methods to execute every update -> append every functions to this list
                                        # Don't use self.method, use Class.method
        self.receptor = [] #anything that's on the surface, put it in as an object, not class
        self.cytosol = {} # anything to keep, {'class' : 'number of the item'} use issubclass
        self.status = {} # anything to tell about it's state
        Cell.cell_list.append(self)
        self.bounced = False
        tool.totalgrid.register(self)
        self.crashed = []

    def kill(self) :
        pygame.sprite.DirtySprite.kill(self)
        Cell.cell_list.remove(self)
        tool.totalgrid.kill(self)

    def lysis(self) :
        """
        when another object tries to kill this object.
        default : kill()
        returns True if it kills itself
        """
        self.kill()
        return True

    def set_speed (self, dx = None, dy = None) :
        """
        sets only the given component.
        """
        if dx != None :
            self.speed[0] = dx
        if dy != None :
            self.speed[1] = dy

    def get_pos (self) :
        return self.pos.copy()

    def set_pos(self, newpos : list) :
        """
        sets to newpos (centerx, centery)
        """
        if len(newpos) == 2 :
            self.pos = list(newpos).copy()
        else :
            raise UserWarning('wrong position passed')

    def update_pos (self) :
        bef = self.rect.copy()
        self.speed[0] += self.acc[0]
        self.speed[1] += self.acc[0]
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.bounced = False
        if bef != self.rect :
            self.dirty = 1
            self.crashed = tool.totalgrid.update(self,False,bef)
        else :
            self.crashed = tool.totalgrid.update(self)

    def update (self) :
        """
        executes every methods in self.gene
        every methods should not take any other parameter than self
        """
        for met in self.gene :
            met(self)

    def bounce (self, vertical = True) :
        """
        vertical : if vertical, True, if horizontal, False
        """
        if self.bounced == False :
            if vertical :
                self.speed[0] = -self.speed[0]
            elif not vertical :
                self.speed[1] = -self.speed[1]
            self.bounced = True

    def get_rect (self) :
        """
        returns a copy of self.rect
        """
        return self.rect.copy()


class Eukaryote(Cell) :
    def __init__ (self, startpos : list, speed : list, imgnum : int = 0) :
        Cell.__init__(self, startpos, speed, imgnum)
        self.atp = 900
        self.glucose = 200
        self.glucose_max = 1000
        self.adp = 100
        self.pyruvate = 10
        self.nadh = 100
        self.nad = 10000
        if EASYMITOCHONDRIA :
            self.mitochondria = cellorgan.Mitochondria_easy()
        else :
            self.mitochondria = cellorgan.Mitochondria()
        self.glycolysis_rate = 1
        self.replicate_now = False
        self.gene.extend([Eukaryote.update_metabolism, Eukaryote.eat_glucose, Eukaryote.replicate, Eukaryote.update_ribosome,\
            Eukaryote.release_cytokine])
        self.ribosome = cellorgan.Ribosome(self.cytosol)
        self.cytokine = []  #cytokines that should be released / list of cytokine classes

    def release_cytokine(self) :
        """
        releases cytokine and resets the list
        """
        for cy in self.cytokine :
            if self.cytosol.get(cy, False) and self.cytosol[cy] > 0:
                cy(self.pos, tool.rand_2D(1.2))
                self.cytosol[cy] -= 1
            else : 
                self.ribosome.mrna(cy, 100)
        self.cytokine.clear()

    def update_ribosome (self) :
        if self.atp > 500 :
            self.adp_to_atp(-self.ribosome.give_atp(10))
        self.ribosome.update()

    def replicate (self) :
        if self.replicate_now :
            new = Eukaryote(self.pos, tool.rand_2D())
            new.gene = self.gene.copy()
            self.replicate_now = False

    def eat_glucose (self) :
        if self.glucose < self.glucose_max :
            for crsh in self.crashed :
                if type(crsh).__name__ == 'Glucose' :
                    crsh.lysis()
                    self.glucose += crsh.amount

    def get_atp_level (self) :
        return self.atp

    def set_glucose_max (self, num) :
        self.glucose_max = num

    def get_glucose_max (self) :
        return self.glucose_max

    def adp_to_atp (self, num) :
        """
        adp -= num
        atp += num
        can be negative
        DOES NOT CHECK SUFFICIENCY
        """
        self.adp -= num
        self.atp += num

    def nad_to_nadh (self, num) :
        """
        nad -= num
        nadh += num
        can be negative
        DOES NOT CHECK SUFFICIENCY
        """
        self.nad -= num
        self.nadh += num

    def glycolysis(self, num) :
        """
        consumes num of glucose and change it to 2 * pyruvate
        if glucose or adp or nadh is insufficient, it stops
        """
        if num<0 :
            raise UserWarning('negative num passed to glycolysis of eukaryote')
        for _ in range (num):
            if self.glucose >= 1 and self.adp >= 2 and self.nad >= 2 :
                self.glucose -= 1
                self.adp_to_atp(2)
                self.nad_to_nadh(2)
                self.pyruvate += 2

    def consume_move(self) :
        """
        spending atp for moving
        """
        return math.ceil(math.sqrt(self.speed[0]**2 + self.speed[1]**2))

    def consume_metabolism (self) :
        """
        constantly spending atp
        """
        return random.randint(1,10)

    def consume (self) :
        self.adp_to_atp(-self.consume_move())
        self.adp_to_atp(-self.consume_metabolism())

    def set_glycolysis(self, gly) :
        """
        set glycolysis_rate
        """
        self.glycolysis_rate = gly

    def glycolysis_rate_cal (self) :
        """
        calculating glycolysis rate itself
        """
        x = self.mitochondria.get_atp()
        y = self.mitochondria.get_adp()
        a = self.atp
        b = self.adp
        self.adp_to_atp(self.mitochondria.atp_translocase(math.ceil((x*b - a*y)/(a+b+x+y))))
        if a<1 :
            return
        else :
            self.set_glycolysis(int(5*b/a))

    def update_metabolism(self) :
        self.glycolysis_rate_cal()
        self.glycolysis(self.glycolysis_rate)
        if 700*self.nadh > self.nad :
            self.nad_to_nadh(-self.mitochondria.mashuttle())
        if self.pyruvate > self.mitochondria.get_pyruvate() :
            self.pyruvate -= self.mitochondria.pyruvate_translocase(self.pyruvate - self.mitochondria.get_pyruvate())
        self.mitochondria.update()
        self.consume()

    def update(self) :
        Cell.update(self)
        if self.atp <= 0 : self.necrosis()

    def apoptosis(self) :
        particle.ApoptoticBody(self.pos, (0,0))
        for _ in range(40) :
            cytokine.Ab(self.pos, tool.rand_2D(1.2))
        self.kill()

    def necrosis(self) :
        for _ in range(5) :
            particle.NecroticBody(self.pos, tool.rand_2D(0.03))
        self.kill()

class Prokaryote(Cell) :
    def __init__(self, startpos : list, speed : list, imgnum : int = 6):
        Cell.__init__(self, startpos, speed, imgnum)
        self.properties = {}
        self.ribosome = cellorgan.Ribosome(self.cytosol)