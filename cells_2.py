import pygame
import random
import os
import math
import particles_2 as particle
import cytokines_2 as cytokine
import functions_2 as tool

IMAGE = 'image'
DEFAULTLAYER = 0

class Cell(pygame.sprite.DirtySprite) :
    """
    Any thing that has receptors and genes
    Genes should not have any other parameters than self
    """
    imgs = []
    cell_list = []
    try :
        imgs.append(pygame.image.load(os.path.join(IMAGE, "eukaryote.png"))) #0
        imgs.append(pygame.image.load(os.path.join(IMAGE, "virus.png")))     #1
        imgs.append(pygame.image.load(os.path.join(IMAGE, "Th2.png")))       #2
        imgs.append(pygame.image.load(os.path.join(IMAGE, "macrophage.png")))#3
        imgs.append(pygame.image.load(os.path.join(IMAGE, "epithelium.png")))#4
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
        self.receptor = [] #anything that's on the surface
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
        self.mitochondria = Mitochondria()
        self.glycolysis_rate = 1
        self.replicate_now = False
        self.gene.extend([Eukaryote.update_metabolism, Eukaryote.eat_glucose, Eukaryote.replicate, Eukaryote.update_ribosome,\
            Eukaryote.release_cytokine])
        self.ribosome = Ribosome(self.cytosol)
        self.cytokine = []  #cytokines that should be released / list of cytokine classes

    def release_cytokine(self) :
        """
        releases cytokine and resets the list
        """
        for cy in self.cytokine :
            if self.cytosol.get(cy, False) and self.cytosol[cy] > 0:
                cy(self.pos, tool.rand_2D(0.7))
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
        self.kill()

    def necrosis(self) :
        for _ in range(5) :
            particle.NecroticBody(self.pos, tool.rand_2D(0.03))
        self.kill()


class Mitochondria() :
    def __init__ (self, adp = 800, atp = 200) :
        self.adp = adp
        self.atp = atp
        self.pyruvate = 0
        self.intramem_h = 10000
        self.intracell_h = 10000
        self.nadh = 100
        self.nad = 10000
        self.fadh = 100
        self.fad = 10000
        self.tca_rate = 2
        self.etc_rate = 2
        self.atp_rate = 28  #default : tca:etc:atp = 2:2:28
        self.mashuttle_rate = 2
        self.g3pshuttle_rate = 2

    def set_mashuttle_rate (self, rate : int) :
        """
        set how many nadh tossed per frame by mashuttle
        """
        self.mashuttle_rate = rate

    def set_g3pshuttle_rate (self, rate: int) :
        """
        set how many fadh tossed per frame by g3pshuttle
        """
        self.g3pshuttle_rate = rate

    def set_total_rate(self, rate: int) :
        """
        set mitochondrial metabolism rate as a whole,
        keeping ratio at 1:1:14 for tca/etc/atp
        """
        self.tca_rate = rate
        self.etc_rate = rate
        self.atp_rate = 14 * rate

    def set_tca_rate(self, rate : int) :
        """
        set rate of TCA cycle
        """
        self.tca_rate = rate

    def set_etc_rate(self, rate : int) :
        """
        set rate of ETC, 5*rate for nadh
        """
        self.etc_rate = rate

    def set_atp_rate(self, rate : int) :
        """
        set rate of atp synthase
        default is 28 per a glucose
        """
        self.atp_rate = rate

    def get_pyruvate (self) :
        """
        returns self.pyruvate
        """
        return self.pyruvate

    def get_atp (self) :
        return self.atp

    def get_adp (self) :
        return self.adp

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

    def fad_to_fadh (self, num) :
        """
        fad -= num
        fadh += num
        can be negative
        DOES NOT CHECK SUFFICIENCY
        """
        self.fad -= num
        self.fadh += num

    def h_to_intramem (self, num) :
        """
        intracell_h -= num
        intramem_h += num
        can be negative
        DOES NOT CHECK SUFFICIENCY
        """
        self.intracell_h -= num
        self.intramem_h += num

    def atp_translocase(self, num) :
        """
        num of adp/atp transported, adp to mitochondria and vice versa
        if number is negative, atp to mitochondria and vice versa
        if num exceeds mitochondrial atp/adp available, transports only until the maximum
        returns actually transported adenine number
        SHOULD ONLY BE USED BY HOST CELL
        """
        if num > self.atp :
            transported = self.atp
            self.adp += self.atp
            self.atp = 0
            return transported
        elif num < -self.adp :
            transported = self.adp
            self.atp += self.adp
            self.adp = 0
            return transported
        else :
            self.adp_to_atp(-num)
            return num

    def g3pshuttle (self) :
        """
        cell nadh to mitochondria fadh,
        if fad is not enough, returns how many transfered
        rate is determined by g3pshuttle_rate
        """
        if self.g3pshuttle_rate > self.fad :
            transported = self.fad
            self.fad_to_fadh(self.fad)
            return transported
        else :
            self.fad_to_fadh(self.g3pshuttle_rate)
            return self.g3pshuttle_rate

    def mashuttle (self) :
        """
        cell nadh to mitochondria nadh,
        if nad is not enough, returns how many transfered
        ratio is determined by mashuttle_rate
        """
        remnant = int((self.nad + self.nadh)/700)
        if self.mashuttle_rate + remnant > self.nad :
            transported = self.nad - remnant
            self.nad_to_nadh(self.nad - remnant)
            return transported
        else :
            self.nad_to_nadh(self.mashuttle_rate)
            return self.mashuttle_rate

    def pyruvate_translocase (self, num) :
        """
        add num of pyruvate to the mitochondria
        returns transfered number
        SHOULD BE USED BY HOST CELL
        """
        self.pyruvate += num
        return num

    def tca_cycle (self, num) :
        """
        num of cycle done;
        if any substrates are insufficient, it stops
        this includes oxidative decarboxylation of pyruvate -> nadh
        """
        for _ in range(num) :
            if self.pyruvate >= 1 and self.adp >= 1 and self.nad >=3 and self.fad >= 1 :
                self.pyruvate -= 1
                self.adp_to_atp(1)
                self.nad_to_nadh(4)
                self.fad_to_fadh(1)
            else :
                break

    def etc (self, nadh, fadh) :
        """
        consumes num of nadh/fadh respectively
        stops when nadh or fadh or intracell_h are insufficient
        """
        remnant_n = int((self.nad + self.nadh)/700)
        remnant_f = int((self.fad + self.fadh)/700)
        if self.nadh > 0 and self.nadh - remnant_n < nadh and self.intracell_h > 10*self.nadh :
            self.h_to_intramem(10*(self.nadh-remnant_n))
            self.nad_to_nadh(-self.nadh+remnant_n)
        elif nadh <= self.nadh and self.intracell_h > 10*nadh:
            self.h_to_intramem(10*nadh)
            self.nad_to_nadh(-nadh)

        if self.fadh > 0  and self.fadh - remnant_f < fadh and self.intracell_h > 6*self.fadh:
            self.h_to_intramem(6*(self.fadh-remnant_f))
            self.fad_to_fadh(-self.fadh+remnant_f)
        elif fadh <= self.fadh and self.intracell_h > 6*fadh :
            self.h_to_intramem(6*fadh)
            self.fad_to_fadh(-fadh)
               
    def atp_synthase (self, num) :
        """
        Makes num of ATPs, consuming 4 protons per ATP
        if no proton gradient or ADP available, stops
        """
        for _ in range(num) :
            if self.adp >= 1 and self.intramem_h >= 4 + self.intracell_h :
                self.adp_to_atp(1)
                self.h_to_intramem(-4)
            else :
                break

    def update(self) :
        self.tca_cycle(self.tca_rate)
        self.etc(5*self.etc_rate,self.etc_rate)
        self.atp_synthase(self.atp_rate)

class Ribosome() :
    def __init__(self, host : dict) :
        """
        host: a dictionary to return complete products
        host dict should be { (protein name) : (num of protein)}
        """
        self.recipe_dict = {}
        self.wait_list = {}
        self.host_dict = host
        self.atp_total = 0

    def give_atp(self, num) :
        """
        transfer num of atp to this ribosome
        only receives when there is anything left in the waiting list
        returns received atp num
        """
        if len(self.wait_list) :
            self.atp_total += num
            return num
        else :
            return 0

    def mrna(self, name : 'class', atp_consume : int) :
        """
        adds a 'name' to the waiting list
        if the same protein with different atp value is added,
        the atp needed to make the protein will be overwritten in the dictionary
        will not append if the same protein is already in the waiting list
        """
        self.recipe_dict[name] = atp_consume
        if not name in self.wait_list :
            self.wait_list[name] = 0

    def get_waitlist(self) :
        """
        returns a copy of the waiting list
        """
        return self.wait_list.copy()

    def update(self) :
        l = len(self.wait_list)
        made = []
        if l :
            for pt in self.wait_list :
                self.wait_list[pt] += self.atp_total/l
                if self.wait_list[pt] > self.recipe_dict[pt] :
                    if self.host_dict.get(pt, False) :
                        self.host_dict[pt] += 1
                    else :
                        self.host_dict[pt] = 1
                    made.append(pt)
            for pt in made:
                self.wait_list.pop(pt)
            self.atp_total = 0


