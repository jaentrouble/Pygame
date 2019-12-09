import pygame
import os
import random
import math
import numpy as np
import shelve

dir = "image"
SAVEDIR = 'savefile'
CELLLAYER = 0
MOLECULELAYER = 1
VESSEL = -1
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
HORIZONTAL = 4
VERTICAL = 5

## eukgroup, allgroup, glucosegroup, flowgroup
## flowgroup needs dx, dy
## allgroup is a 'LayeredUpdates' class
## don't forget to assign groups & layer BEFORE calling !!!pygame.sprite.Sprite.__init__!!!!
## always add 'pos' vector in sprites
## don't forget to change the 'rect' object!!!!!!!!!!!! 'pos' object does nothing!!!!!!!!!!!!!!

class Vessel(pygame.sprite.Sprite) :
    color = {'Blue' : (0, 0, 255),
             'Red' : (255, 0, 0)
             }

    def __init__ (self, diameter, length, direction, start, color, speed, force, area, suck = 0) :
        """
        direction: UP, DOWN, LEFT, RIGHT = 0,1,2,3
        start : middle of the starting edge (x,y)
        color : string; check Vessel.color dictionary
                -> Red, Blue
        speed : speed of flow, sets dx or dy of any particle in, depending of the direction
        force : ddv of the contents flowing inside

        vessel will only update self.rect when calling 'update_position' method
        """
        self.groups = Main.allgroup, Main.vesselgroup
        self._layer = VESSEL
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.end_endo = pygame.sprite.Group() #group of endotheliums at the end of the vessel
        self.color_name = color
        self.color = Vessel.color[color]
        self.direction = direction
        self.area = area
        self.pos = [0,0]
        if self.direction == UP :
            self.pos[0] = start[0]
            self.pos[1] = start[1] - length/2
            self.height = length
            self.width = diameter    ## setting center/height/width per direction
        elif self.direction == DOWN :
            self.pos[0] = start[0]
            self.pos[1] = start[1] + length/2
            self.height = length
            self.width = diameter
        elif self.direction == LEFT :
            self.pos[0] = start[0] - length/2
            self.pos[1] = start[1]
            self.height = diameter
            self.width = length
        elif self.direction == RIGHT :
            self.pos[0] = start[0] + length/2
            self.pos[1] = start[1]
            self.height = diameter
            self.width = length
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, self.color, self.rect)
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.image.convert()
        self.speed = speed
        self.force = force
        self.suck = suck
        self.reset_endothelium()
        
    def save_list (self) :
        """
        returns a list of initializing values to create the same vessel right now (but new)
        """
        if self.direction == UP or self.direction == DOWN :
            diameter = self.rect.width
            length = self.rect.height
            if self.direction == UP :
                start = (self.rect.centerx, self.rect.bottom)
            else :
                start = (self.rect.centerx, self.rect.top)
        else :
            diameter = self.rect.height
            length = self.rect.width
            if self.direction == LEFT :
                start = (self.rect.right, self.rect.centery)
            else :
                start = (self.rect.left, self.rect.centery)
        direction = self.direction
        color = self.color_name
        speed = self.speed
        force = self.force
        area = self.area
        suck = self.suck
        return (diameter, length, direction, start, color, speed, force, area, suck)

    def set_suck (self,suck) :
        self.suck = suck

    def update (self) :
        self.flow(self.force, self.speed)

    def update_position(self) :
        """
        vessel will update self.rect only when this function is called
        """
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, self.color, self.rect)
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def reset_endothelium (self) :
        """
        kills all endotheliums 'touching' the vessel
        generates endothelium around the walls only
        """
        unit = Endothelium.length
        collide = pygame.sprite.spritecollide(self, Main.endogroup, False)
        for endo in collide :
            endo.kill()
        if self.direction == UP or self.direction == DOWN :
            ypos = self.rect.top + unit/2
            xpos = self.rect.left + unit/2
            left = self.rect.left
            right = self.rect.right
            while ypos < self.rect.bottom :
                Endothelium((left,ypos), self.area, VERTICAL, self)
                Endothelium((right,ypos), self.area, VERTICAL, self)
                ypos += unit
            if self.direction == UP :
                ypos = self.rect.top
            elif self.direction == DOWN :
                ypos = self.rect.bottom
            while xpos < self.rect.right :
                self.end_endo.add(Endothelium((xpos,ypos), self.area, HORIZONTAL, self))
                xpos += unit


        if self.direction == LEFT or self.direction == RIGHT :
            xpos = self.rect.left + unit/2
            ypos = self.rect.top + unit/2
            top = self.rect.top
            bottom = self.rect.bottom
            while xpos < self.rect.right :
                Endothelium((xpos,top), self.area, HORIZONTAL, self)
                Endothelium((xpos,bottom), self.area, HORIZONTAL, self)
                xpos += unit
            if self.direction == LEFT :
                xpos = self.rect.left
            elif self.direction == RIGHT :
                xpos = self.rect.right
            while ypos < self.rect.bottom :
                self.end_endo.add(Endothelium((xpos,ypos), self.area, VERTICAL, self))
                ypos += unit

    def set_speed(self, speed) :
        """
        refers to the speed of 'flowing' inside the vessel, not vessel itself
        """
        self.speed = speed

    def set_force (self, force) :
        self.force = force

    def flow (self, ddv = 0, max_velocity = 0) :
        """
        adds ddv to particle's dx or dy until max_velocity(in absolute value); per frame
        max_velocity should be 0 or N
        for branches, it sucks up 'self.suck' pixels infront of the vessel
        use set_suck method to change self.suck
        """
        suck = self.suck

        if self.direction == UP:
            flowing_area = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height + suck)
        if self.direction == DOWN:
            flowing_area = pygame.Rect(self.rect.left, self.rect.top - suck, self.rect.width, self.rect.height)
        if self.direction == LEFT:
            flowing_area = pygame.Rect(self.rect.left, self.rect.top, self.rect.width + suck, self.rect.height)
        if self.direction == RIGHT:
            flowing_area = pygame.Rect(self.rect.left - suck, self.rect.top, self.rect.width, self.rect.height)
        
        for particle in Main.flowgroup :
            if flowing_area.contains(particle.rect) :
                if self.direction == UP:
                    if particle.dy > - max_velocity:
                        particle.add_speed(ddy = -ddv)
                if self.direction == DOWN:
                    if particle.dy < max_velocity:
                        particle.add_speed(ddy = ddv)
                if self.direction == LEFT:
                    if particle.dx > - max_velocity:
                        particle.add_speed(ddx = -ddv)
                if self.direction == RIGHT:
                    if particle.dx < max_velocity:
                        particle.add_speed(ddx = ddv)

    def grow_length(self, length: int) :
        """
        length : int, grows endothelium * length to the direction of the vessel
        only until the end of the screen
        """
        unit = Endothelium.length
        if self.direction == UP :
            if self.rect.top - (unit * length) < self.area.top :
                pass
            else :
                self.height += unit * length
                self.pos[1] -= unit/2
                self.update_position()
                for endo in self.end_endo :
                    endo.pos[1] -= unit
                Endothelium((self.rect.left, self.rect.top + unit/2), self.area, VERTICAL, self)
                Endothelium((self.rect.right, self.rect.top + unit/2), self.area, VERTICAL, self)
        elif self.direction == DOWN :
            if self.rect.bottom + (unit * length) > self.area.bottom :
                pass
            else :
                self.height += unit * length
                self.pos[1] += unit/2
                self.update_position()
                for endo in self.end_endo :
                    endo.pos[1] += unit
                Endothelium((self.rect.left, self.rect.bottom - unit/2), self.area, VERTICAL, self)
                Endothelium((self.rect.right, self.rect.bottom - unit/2), self.area, VERTICAL, self)
        elif self.direction == LEFT :
            if self.rect.left - (unit * length) < self.area.left :
                pass
            else :
                self.width += unit * length
                self.pos[0] -= unit/2
                self.update_position()
                for endo in self.end_endo :
                    endo.pos[0] -= unit
                Endothelium((self.rect.left + unit/2, self.rect.top), self.area, HORIZONTAL, self)
                Endothelium((self.rect.left + unit/2, self.rect.bottom), self.area, HORIZONTAL, self)
        elif self.direction == RIGHT :
            if self.rect.right + (unit * length) > self.area.right :
                pass
            else :
                self.width += unit * length
                self.pos[0] += unit/2
                self.update_position()
                for endo in self.end_endo :
                    endo.pos[0] += unit
                Endothelium((self.rect.right - unit/2, self.rect.top), self.area, HORIZONTAL, self)
                Endothelium((self.rect.right - unit/2, self.rect.bottom), self.area, HORIZONTAL, self)


class Artery(Vessel) :
    def __init__(self, diameter, length, direction, start, speed, force, area, suck = 0):
        Vessel.__init__(self, diameter, length, direction, start,'Red', speed, force, area, suck)

class Vein(Vessel) :
    def __init__(self, diameter, length, direction, start, speed, force, area, suck = 0) :
        Vessel.__init__(self, diameter, length, direction, start,'Blue', speed, force, area, suck)

class Glucose(pygame.sprite.Sprite) :
    imgs = []
    ### image list for Glucose
    try :
        imgs.append(pygame.image.load(os.path.join(dir, "glucose.png")))
    except :
        raise UserWarning("Unable to load glucose.png")

    def __init__(self, startpos: tuple = None, area: pygame.Rect = None) :
        """
        area: pygame.Rect(); inside where Glucose should exist
        """
        self.groups = Main.glucosegroup, Main.allgroup, Main.flowgroup
        self._layer = MOLECULELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        if area == None:
            raise UserWarning( "No area transferred(Glucose)")
        self.area = area
        self.image = Glucose.imgs[0]
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        if startpos == None :
            self.pos = [random.randint(int(self.area.left + self.rect.width/2) ,int(self.area.right - self.rect.width/2)),
               random.randint(int(self.area.top + self.rect.height/2), int(self.area.bottom - self.rect.height/2))]
        else :
            self.pos = [round(startpos[0]), round(startpos[1])]
        self.set_speed()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def update(self):
        if not self.area.contains(self.rect) :
            self.hit_edge()
        self.move()
        
    def move(self) :
        self.pos[0] += self.dx
        self.pos[1] += self.dy
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def set_position (self, x :int = None, y :int = None) :
        if x != None :
            self.pos[0] = x
        if y != None :
            self.pos[1] = y
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def bounce(self, wall) :
        """
        wall: HORIZONTAL or VERTICAL
        """
        if wall == HORIZONTAL :
            self.dy = -self.dy
        elif wall == VERTICAL :
            self.dx = -self.dx
        else :
            raise UserWarning("bounce error")

    def set_speed(self, vector = (0,0), **component) :  ### For later use; glucose may move
        """
        vector : (dx, dy)
        component overwrites vector; dx, dy
        """
        self.dx = vector[0]
        self.dy = vector[1]
        for key, value in component :
            if 'dx' in component.keys() :
                self.dx = value
            if 'dy' in component.keys() :
                self.dy = value

    def change_speed(self, dx = None, dy = None) :
        """
        changes only the given component
        """
        if dx != None :
            self.dx = dx
        if dy != None :
            self.dy = dy

    def add_speed (self, ddx = 0, ddy = 0) :
        """
        adds ddx or ddy to dx or dy, respectively
        """
        self.dx += ddx
        self.dy += ddy

    def hit_edge (self) :
        if self.pos[0] + self.rect.width/2 > self.area.right:
            self.pos[0] = self.area.right - self.rect.width/2
            self.bounce(VERTICAL)
        if self.pos[0] - self.rect.width/2 < self.area.left:
            self.pos[0] = self.area.left + self.rect.width/2
            self.bounce(VERTICAL)
        if self.pos[1] + self.rect.height/2 > self.area.bottom:
            self.pos[1] = self.area.bottom - self.rect.height/2
            self.bounce(HORIZONTAL)
        if self.pos[1] - self.rect.height/2 < self.area.top:
            self.pos[1] = self.area.top + self.rect.height/2
            self.bounce(HORIZONTAL)

class Eukaryote(pygame.sprite.Sprite) :
    imgs = []
    ### image list for Eukaryotes
    try :
        imgs.append(pygame.image.load(os.path.join(dir, "eukaryote.png")))
        imgs.append(pygame.image.load(os.path.join(dir, "endothelium.png")))
    except:
        raise UserWarning( "Unable to load eukaryote.png")
    ###
    euks = {}
    number = 0
    metabolism_constant = 0.1   #consumes energy per frame - default

    def __init__(self, startpos : tuple = None, area: pygame.Rect = None, imgnum = 0):
        """
        area: pygame.Rect(); the limit of Eukaryote
        img: image to use in Eukaryote.imgs[]
        """
        self._layer = CELLLAYER
        self.groups = Main.eukgroup, Main.allgroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        if area == None:
            raise UserWarning( "No area transferred(Eukaryote)")
        self.area = area
        self.imgnum = imgnum
        self.image = Eukaryote.imgs[self.imgnum]
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        if startpos == None :
            self.pos = [random.randint(int(self.area.left + self.rect.width/2) ,int(self.area.right - self.rect.width/2)),
               random.randint(int(self.area.top + self.rect.height/2), int(self.area.bottom - self.rect.height/2))]
        else :
            self.pos = [startpos[0], startpos[1]]
        self.set_speed()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.max_energy = 1000.0
        self.energy = 1000.0  ##use as much as distance moved
        self.extra_energy = 0.0 ## left-over energy
        self.glucose_energy = 250.0
        self.div_limit = 1000.0  ## if extra_energy fills up until div_limit, cell devides
        self.number = Eukaryote.number   #### id number
        self.metabolism_constant = Eukaryote.metabolism_constant


        #Eukaryote.euks[self.number] = self
        #Eukaryote.number += 1
        EnergyGauge(self)
        
    def set_speed (self, vector = None) :
        """
        if vector is empty, sets to a random vector
        """
        if vector == None :
            self.dx, self.dy = (0,0)
        else:
            self.dx, self.dy = vector

    def change_speed(self, dx = None, dy = None) :
        """
        changes only the given component
        """
        if dx != None :
            self.dx = dx
        if dy != None :
            self.dy = dy

    def add_speed (self, ddx = 0, ddy = 0) :
        """
        adds ddx or ddy to dx or dy, respectively
        """
        self.dx += ddx
        self.dy += ddy

    def eat_glucose (self) :
        glutouched = pygame.sprite.spritecollide(self, Main.glucosegroup, False)
        for glu in glutouched :
            glu.kill()
            self.energy += self.glucose_energy

    def divide (self) :
        self.image = Eukaryote.imgs[0]
        self.extra_energy = 0.0
        Eukaryote(self.pos, self.area)

    def hit_edge (self) :
        self.set_speed()
        if self.pos[0] + self.rect.width/2 > self.area.right:
            self.pos[0] = self.area.right - self.rect.width/2
        if self.pos[0] - self.rect.width/2 < self.area.left:
            self.pos[0] = self.area.left + self.rect.width/2
        if self.pos[1] + self.rect.height/2 > self.area.bottom:
            self.pos[1] = self.area.bottom - self.rect.height/2
        if self.pos[1] - self.rect.height/2 < self.area.top:
            self.pos[1] = self.area.top + self.rect.height/2

    def spend_energy(self) :
        spdvec = np.array([self.dx, self.dy])

        self.energy -= np.linalg.norm(spdvec)
        self.energy -= self.metabolism_constant

    def move(self) :
        self.pos[0] += self.dx
        self.pos[1] += self.dy
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def update_size(self) :
        self.image = pygame.transform.rotozoom(Eukaryote.imgs[self.imgnum],0,(1 + self.extra_energy/self.div_limit))
        self.image.convert_alpha()

    def update(self):
        if self.energy <= 0 :
            self.kill()
        else :
            self.eat_glucose()
            self.spend_energy()
            if self.energy > self.max_energy :
                self.extra_energy += self.energy - self.max_energy
                self.energy = self.max_energy            
            if not self.area.contains(self.rect):
                self.hit_edge()
            self.update_size()
            self.rect = self.image.get_rect()
            self.move()
            if self.extra_energy > self.div_limit :
                self.divide()

class Endothelium(Eukaryote) :
    length = Eukaryote.imgs[1].get_width()
    width = Eukaryote.imgs[1].get_height()
    def __init__(self, startpos : tuple = None, area: pygame.Rect = None, direction = HORIZONTAL, vessel = None) :
        """
        direction : HORIZONTAL or VERTICAL
        vessel : Vessel object, the vessel this endothelium is in part of
        """
        Eukaryote.__init__(self, startpos, area, imgnum=1)
        self.direction = direction
        if vessel != None :
            self.vessel = vessel
        else :
            raise UserWarning('no vessel assigned! (Endothelium)')
        self.remove(Main.flowgroup) #endothelium should not flow
        self.add(Main.endogroup)
        if self.direction == VERTICAL :
            self.image = pygame.transform.rotate(Eukaryote.imgs[1],90)
            self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.centerx = self.pos[0]
            self.rect.centery = self.pos[1]

    def set_vessel(self, vessel) :
        """
        vessel : Vessel, the vessel this endothelium is in part of
        """
        self.vessel = vessel

    def update_size(self):
        pass

    def eat_glucose(self):
        glutouched = pygame.sprite.spritecollide(self, Main.glucosegroup, False)
        for glu in glutouched :
            if self.energy < self.max_energy - self.glucose_energy :
                glu.kill()
                self.energy += self.glucose_energy
            else :
                if self.direction == VERTICAL:
                    if glu.rect.centerx <= self.rect.centerx :
                        glu.set_position(x = self.rect.left - glu.rect.width)
                    else :
                        glu.set_position(x = self.rect.right + glu.rect.width)
                    glu.bounce(VERTICAL)
                else :
                    if glu.rect.centery <= self.rect.centery :
                        glu.set_position(y = self.rect.top - glu.rect.height)
                    else :
                        glu.set_position(y = self.rect.bottom + glu.rect.height)
                    glu.bounce(HORIZONTAL)
            
class EnergyGauge(pygame.sprite.Sprite) :
    def __init__(self, target: pygame.sprite.Sprite) :
        """
        shows energy bar over the target
        needs 'energy' and 'max_energy'
        if energy > energy_max, just fills until maximum.
        """
        self._layer = target._layer
        self.groups = Main.allgroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target
        self.image = pygame.Surface((self.target.rect.width, 7))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.target.pos[0]
        self.rect.centery = self.target.pos[1]
        pygame.draw.rect(self.image, (0, 255, 0), self.rect , 1)
        self.image.convert_alpha()
        self.oldpercent = 0
        
    def update(self) :
        self.percent = self.target.energy / self.target.max_energy
        if self.percent > 1 :
            self.percent = 1
        if self.percent != self.oldpercent :
            pygame.draw.rect(self.image, (0, 0, 0), (1, 1, self.rect.width-2, 5))
            pygame.draw.rect(self.image, (0, 255, 0), (1, 1, round((self.rect.width-2) * self.percent), 5))
        self.oldpercent = self.percent
        self.rect.centerx = self.target.rect.centerx
        self.rect.y = self.target.rect.y - 7

        if not self.target.alive() :
            self.kill()


class Saver() :

    def __init__(self, savefile : str) :
        """
        savefile : name of the savefile
        """
        self.root = os.path.join(SAVEDIR, savefile)

    def save(self) :
        vessel_list = []
        for v in Main.vesselgroup :
            vessel_list.append(v.save_list())
        with shelve.open(self.root) as sv :
            sv['vessel'] = vessel_list

    def load(self) :
        try :
            sv = shelve.open(self.root)
        except :
            raise UserWarning('loading failed')
        else :
            for v in sv['vessel'] :
                Vessel(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8])
        finally :
            sv.close()


class Main() :
    ## add EVERY sprites to 'allgroup'
    allgroup = pygame.sprite.LayeredUpdates()
    flowgroup = pygame.sprite.Group()   
    ##flow group needs dx, dy, add_speed function######

    eukgroup = pygame.sprite.Group()
    glucosegroup = pygame.sprite.Group()
    vesselgroup = pygame.sprite.Group()
    endogroup = pygame.sprite.Group()

    def __init__(self, width = 1600, height = 900, fps = 60) :
        pygame.init()
        self.saver = Saver('map')
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill((255,255,255))
        self.background = self.background.convert()
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.glucose_constant = 3          #per second(frame-based, though)
        self.rect = self.screen.get_rect()
        self.speed_limit = Endothelium.width/2 - 2  #speed limit that won't go through the endothelium

    def run(self) :
        #a = input('start?')
        mainloop = True
        self.screen.blit(self.background,(0,0))
        #right_vessel =  Artery(100,900,RIGHT,(0,100), self.speed_limit, 0.5,self.rect)
        #down_vessel = Vein(100, 100, DOWN, (850,150), self.speed_limit, 0.5,self.rect, 50)
        self.saver.load()
        loopcounter = 0
        while mainloop :
            if loopcounter >= self.fps :   ### counts 'frames-passed' ; it's frame-based program
                loopcounter = 0
            loopcounter += 1
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds/1000.0

            ##escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 
             ########
                    if event.key == pygame.K_s :
                        self.saver.save()
             ########
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    #down_vessel.grow_length(1)
                    #right_vessel.grow_length(1)
                    #Eukaryote(pygame.mouse.get_pos(), self.screen.get_rect())
            #if len(Main.eukgroup.sprites()) == 0 :
            #    Eukaryote(area = self.rect)
            #    Endothelium(area = self.rect, direction=VERTICAL)
                    pass

            if self.glucose_constant == 0 :
                pass
            elif loopcounter%(self.fps / self.glucose_constant) < 1 :
                self.glucose_creater(0, 30, 50 + Endothelium.width, 150 - Endothelium.width, self.speed_limit)

            Main.allgroup.clear(self.screen, self.background)
            Main.allgroup.update()
            Main.allgroup.draw(self.screen)

            pygame.display.set_caption("[FPS] : {0:.1f}, Eukaryotes : {1}, loop:{2}, Total sprites: {3}".format(self.clock.get_fps(), len(Main.eukgroup.sprites()), loopcounter, len(Main.allgroup.sprites())))
            pygame.display.flip()

    def glucose_creater(self, left, right, top, bottom, speedconstant) :
        """
        creates glucose in random point in between left,right,top,bottom
        random speed (random.random * speedconstant)
        """
        Glucose((random.randint(left,right),random.randint(top,bottom)),self.rect).set_speed((random.random()*speedconstant,random.random()*speedconstant))
            

if __name__ == '__main__':
    Main(1600, 900,60).run()