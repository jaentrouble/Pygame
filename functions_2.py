import pygame
import random
import math
import multiprocessing
import json
import os
import time
import rapidjson

THREAD = 2
SAVEDIR = 'savefile'
#CRASHTIME = 0.0


def rand_2D (multi : float = 1, direction = 0) :
    """
    returns random direction, vector size = multi
    0: normal
    1: only to upward
    2: only to downward
    3: only to leftward
    4: only to rightward
    """
    x = random.choice([-1,1])*random.random()
    y = random.choice([-1,1])*random.random()
    vec = [(x*multi)/math.sqrt(x**2 + y**2),(y*multi)/math.sqrt(x**2 + y**2)]
    if direction == 0 :
        return vec
    elif direction == 1 :
        vec[1] = -abs(vec[1])
        return vec
    elif direction == 2 :
        vec[1] = abs(vec[1])
        return vec
    elif direction == 3 :
        vec[0] = -abs(vec[0])
        return vec
    elif direction == 4 :
        vec[0] = abs(vec[0])
        return vec

def turn_vector (original : list, direction : list) :
    """
    turns 2D-vector
    keeps original speed and spins to make it parallel to the direction vector
    """
    if len(original) != 2 or len(direction) != 2 :
        raise UserWarning('wrong vector handed to turn_vector')
    orgmag = math.sqrt(original[0]**2 + original[1]**2)
    dirmag = math.sqrt(direction[0]**2 + direction[1]**2)
    ratio = orgmag/dirmag
    return [direction[0]*ratio, direction[1]*ratio]

def filler (cls, arg: list, indx : int, area : pygame.Rect, group : list = None):
    """
    fills the area with the cls object
    need rect as a global value in class
    arg: list WITHOUT position value
    indx : what index should the position value insert into
    group : list of groups to add this particle into (if needed)
    """
    if type(group).__name__ != 'list' :
        raise UserWarning('pass a group of list')
    argum= arg.copy()
    index = indx
    argum.insert(index, (0,0))
    width = cls.rect.width
    height = cls.rect.height
    x = area.left + width/2
    y = area.top + height/2
    while y < area.bottom :
        while x < area.right :
            argum = arg.copy()
            argum.insert(index,(x,y))
            if group != None :
                cls(*argum).add(*group)
            else :
                cls(*argum)
            x += width
        y += height
        x = area.left + width/2

def multi_collide(rect_list : list, check : pygame.Rect) :
    """
    returns a list of collided rect index
    """
    if len(rect_list) > 0 :
        manager = multiprocessing.Manager()
        rtrn = manager.list()
        l = int(len(rect_list)/THREAD)
        idx = 0
        procs = []
        for i in range(THREAD-1):
            proc = multiprocessing.Process(target=sub_collide, args = (rtrn, rect_list[i:i+l], check))
            procs.append(proc)
            proc.start()
            i += l
        proc = multiprocessing.Process(target=sub_collide, args = (rtrn, rect_list[i:], check))
        procs.append(proc)
        proc.start()

        for proc in procs :
            proc.join()

        return list(rtrn)
    else :
        return []
    
def sub_collide (rtrn : list, rect_list : list, chck : pygame.Rect):
    rtrn.extend(chck.collidelistall(rect_list))

def rand_point (area : pygame.Rect) :
    """
    return a random int point inside area
    """
    return [random.randint(area.left, area.right), random.randint(area.top, area.bottom)]

class Boundary() :
    def __init__ (self, area : pygame.Rect) :
        """
        controling with area
        """
        self.rect = area


    def bounce (self, particles : pygame.sprite.Group) :
        """
        checks if particles are getting off the area and bounces them
        particles : Group (or any 'group' of sprites)
        """
        for prt in particles :
            rct = prt.get_rect()
            if rct.left < self.rect.left or rct.right > self.rect.right :
                prt.bounce(vertical = True)
                if rct.left < self.rect.left :
                    prt.set_pos((self.rect.left + rct.width/2, rct.centery))
                else :
                    prt.set_pos((self.rect.right - rct.width/2, rct.centery))
            elif rct.top < self.rect.top or rct.bottom > self.rect.bottom :
                prt.bounce(vertical = False)
                if rct.top <= self.rect.top :
                    prt.set_pos((rct.centerx, self.rect.top + rct.height/2))
                else :
                    prt.set_pos((rct.centerx, self.rect.bottom - rct.height/2))

class Saver() :
    def __init__(self, filename : str) :
        """
        saves list of a dictionary of 'class name' : 'list of pos'
        """
        self.root = os.path.join(SAVEDIR, filename)
        self.sequel = []

    def clear_savefile (self) :
        with open(self.root, 'w') as sf :
            pass

    def append(self, items : pygame.sprite.Group) :
        snapshot = {}
        for item in items :
            if not type(item).__name__ in snapshot :
                snapshot[type(item).__name__] = []
            pos = item.get_pos()
            snapshot[type(item).__name__].append([int(pos[0]),int(pos[1])])
        self.sequel.append(snapshot)

    def saverapid(self) :
        stime = time.time()
        if len(self.sequel) > 0 :
            with open(self.root, 'a') as sf :
                for snst in self.sequel :
                    rapidjson.dump(snst, sf)
                    b = sf.write('\n')
            print('rapidjson :', time.time() - stime)
        self.sequel = []

class Grid() :
    def __init__(self) :
        self.grid = []

    def initialize(self, width : int, height : int) :
        for i in range(width) :
            self.grid.append([])
            for j in range(height) :
                self.grid[i].append([])

    def register_group (self, group : pygame.sprite.Group) :
        for spt in group :
            for i in range(spt.rect.left-1,spt.rect.right-1) :
                for j in range(spt.rect.top-1, spt.rect.bottom-1) :
                    self.grid[i][j].append(spt)

    def register(self, spt) :
        for i in range(spt.rect.left-1,spt.rect.right-1) :
            for j in range(spt.rect.top-1, spt.rect.bottom-1) :
                self.grid[i][j].append(spt)

    def kill(self, spt) :
        for i in range(spt.rect.left-1,spt.rect.right-1) :
            for j in range(spt.rect.top-1, spt.rect.bottom-1) :
                self.grid[i][j].remove(spt)

    def update(self, spt: pygame.sprite.Sprite, clean = True, before : pygame.Rect = None ) :
        """
        delete sprt in all areas in 'before' and adds sprt to sprt.rect area
        call this 'after' updating sprt rect
        if not moved, clean = False
        """
        #t=time.time()
        crash = []
        if not clean :
            for i in range(before.left-1, before.right-1) :
                for j in range(before.top-1, before.bottom-1) :
                    self.grid[i][j].remove(spt)
            for i in range(spt.rect.left-1, spt.rect.right-1):
                for j in range(spt.rect.top-1, spt.rect.bottom-1) :
                    for crsh in self.grid[i][j] :
                        if not crsh in crash :
                            crash.append(crsh)
                    self.grid[i][j].append(spt)
        else :
            for i in range(spt.rect.left-1, spt.rect.right-1):
                for j in range(spt.rect.top-1, spt.rect.bottom-1) :
                    for crsh in self.grid[i][j] :
                        if not crsh in crash :
                            crash.append(crsh)
        # global CRASHTIME 
        #CRASHTIME += time.time()-t
        return crash

totalgrid = Grid()