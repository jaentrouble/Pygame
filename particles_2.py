import pygame
import random
import os
import functions_2 as tool

IMAGE = 'image'
PARTICLELAYER = -1
DEFAULTLAYER = 0
IMGDICT = {}
LAYERDICT = {}

class Particle(pygame.sprite.DirtySprite) :
    imgs = []
    particle_list = []
    try :
        imgs.append(pygame.image.load(os.path.join(IMAGE, "glucose.png")))
        imgs.append(pygame.image.load(os.path.join(IMAGE, "ab.png")))
        imgs.append(pygame.image.load(os.path.join(IMAGE, "nb.png")))
        imgs.append(pygame.Surface((5,5)))
    except:
        raise UserWarning( "Unable to load particle images")

    def __init__ (self, startpos : list, speed : list, imgnum : int) :
        self._layer = PARTICLELAYER
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.image = Particle.imgs[imgnum]
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = list(startpos).copy()       # Need 'pos' value to use real values, refers to centerx, centery
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.speed = list(speed).copy()
        self.acc = [0,0]
        self.name = None
        Particle.particle_list.append(self)
        self.bounced = False
        tool.totalgrid.register(self)
        self.crashed = []

    def get_pos(self) :
        return self.pos.copy()

    def set_speed (self, dx = None, dy = None) :
        """
        sets only the given component.
        """
        if dx != None :
            self.speed[0] = dx
        if dy != None :
            self.speed[1] = dy

    def set_pos(self, newpos : list) :
        """
        sets to newpos (centerx, centery)
        """
        if len(newpos) == 2 :
            self.pos = list(newpos).copy()
        else :
            raise UserWarning('wrong position passed')

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

    def update_pos (self) :
        bef = self.rect.copy()
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
        self.update_pos()

    def lysis(self) :
        """
        when another object tries to kill this object, use this
        default : kill()
        returns True if it kills itself
        """
        self.kill()
        return True

    def kill(self) :
        pygame.sprite.DirtySprite.kill(self)
        Particle.particle_list.remove(self)
        tool.totalgrid.kill(self)

class Glucose(Particle) :

    glucose_list = []
    rect = Particle.imgs[0].get_rect()
    IMGDICT['Glucose'] = Particle.imgs[0]
    LAYERDICT['Glucose'] = PARTICLELAYER

    def __init__ (self, startpos : list, speed : list) :
        Particle.__init__(self, startpos, speed, 0)
        Glucose.glucose_list.append(self)
        self.amount = 100 # How many glucose will the cell get if it collides with this glucose.

    def kill(self) :
        Particle.kill(self)
        Glucose.glucose_list.remove(self)

    def set_amount (self, num) :
        """
        set self.amount
        """
        self.amount = num

    def get_amount (self) :
        return self.amount

    def update (self) :
        Particle.update(self)

class ApoptoticBody(Particle) :
    apoptoticbody_list = []
    IMGDICT['ApoptoticBody'] = Particle.imgs[1]
    LAYERDICT['ApoptoticBody'] = PARTICLELAYER

    def __init__(self, startpos : list, speed : list):
        Particle.__init__(self, startpos, speed, 1)
        ApoptoticBody.apoptoticbody_list.append(self)

    def kill(self) :
        Particle.kill(self)
        ApoptoticBody.apoptoticbody_list.remove(self)

class NecroticBody(Particle) :
    necroticbody_list = []
    IMGDICT['NecroticBody'] = Particle.imgs[2]
    LAYERDICT['NecroticBody'] = PARTICLELAYER

    def __init__(self, startpos : list, speed : list) :
        Particle.__init__(self, startpos, speed, 2)
        NecroticBody.necroticbody_list.append(self)

    def kill(self) :
        Particle.kill(self)
        NecroticBody.necroticbody_list.remove(self)

class Cytokine(Particle) :
    surface_dict = {}

    def __init__ (self, startpos : list, speed : list, name : str, color : tuple) :
        Particle.__init__(self, startpos, speed, 3)
        self.name = name
        if not name in Cytokine.surface_dict :
            newcolor = color
            Cytokine.surface_dict[self.name] = self.image.copy()
            Cytokine.surface_dict[self.name].fill(newcolor)
        self.image = Cytokine.surface_dict[self.name]

